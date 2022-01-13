import boto3
from dateutil.tz import tzutc
import datetime


accounts_list = {
	'account1': 'arn:aws:iam::<account_id1>:role/<role_name>',
	'account2': 'arn:aws:iam::<account_id2>:role/<role_name>',
	}


bot_token = 'bot_token'
chatID = 'chatID'

def get_keys(arn):
	session = boto3.Session() 
	#aws cross-account
	sts = session.client('sts')
	role_arn = arn

	assumed_role_object = sts.assume_role( RoleArn=role_arn, RoleSessionName="AssumeRoleSession" )
	#print assumed_role_object
	access_key = assumed_role_object['Credentials']['AccessKeyId']
	session_key = assumed_role_object['Credentials']['SecretAccessKey']
	session_token = assumed_role_object['Credentials']['SessionToken']
	keys = [access_key, session_key, session_token]
	return keys



def check_events(event, context):
	for key in accounts_list.keys(): 
		print key
		keys = get_keys(accounts_list[key])
		session = boto3.Session(
		    aws_access_key_id=keys[0],
		    aws_secret_access_key=keys[1],
		    aws_session_token=keys[2],
		)


		regions = ['us-east-1', 'us-west-2', 'us-west-1', 'eu-west-1', 'eu-central-1', 'ap-southeast-1', 'ap-northeast-1', 'ap-southeast-2', 'ap-northeast-2', 'ap-south-1', 'sa-east-1']

		for region in regions:
			ec2 = session.resource('ec2', region_name=region)

			for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
				try:

					if ec2.Instance(status['InstanceId']).tags:
						instance = ec2.Instance(status['InstanceId']).tags[0]['Value']
					else:
						instance = ''

					message = ("Account: %s\n Instance: %s (%s, %s)\n Event: %s\n Time: %s - %s")%(key, instance, status['InstanceId'], status['AvailabilityZone'], status['Events'][0]['Description'], status['Events'][0]['NotBefore'].strftime('%H:%M, %d %b, %Y'), status['Events'][0]['NotAfter'].strftime('%H:%M, %d %b, %Y'))
					
					send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatID + '&parse_mode=Markdown&text=' + message

					response = requests.get(send_text)
				except Exception as e:
					pass
					#print("get events error:", str(e))

