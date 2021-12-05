import json
import urllib.parse
import boto3
from botocore.exceptions import ClientError

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    uri = 's3://' + bucket + '/' + key
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        send_email('arthur@viz.ai', 'arthur@viz.ai', 'eu-west-1', response['ContentType'], uri)
        return {
            'StatusCode': 200,
            'Message': 'SUCCESS'
        }
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

def send_email(sender, recipient, aws_region, file_type, uri):
  # This address must be verified with Amazon SES.
  SENDER = sender

  # If your account is still in the sandbox, this address must be verified.
  RECIPIENT = recipient

  # The AWS Region you're using for Amazon SES.
  AWS_REGION = aws_region

  # The subject line for the email.
  SUBJECT = "New file uploaded to s3 bucket!"

  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = "File type: " + file_type + "/n" + "URI: " + uri

  # The HTML body of the email.
  BODY_HTML = f"""<html> <head></head> <body> <p>File type: {file_type}</p> <p>URI: {uri}</p> </body> </html>"""

  # The character encoding for the email.
  CHARSET = "UTF-8"

  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name=AWS_REGION)

  # Try to send the email.
  try:
      #Provide the contents of the email.
      response = client.send_email(
          Destination={
              'ToAddresses': [
                  RECIPIENT,
              ],
          },
          Message={
              'Body': {
                  'Html': {
                      'Charset': CHARSET,
                      'Data': BODY_HTML,
                  },
                  'Text': {
                      'Charset': CHARSET,
                      'Data': BODY_TEXT,
                  },
              },
              'Subject': {
                  'Charset': CHARSET,
                  'Data': SUBJECT,
              },
          },
          Source=SENDER,
     )
  # Display an error if something goes wrong.
  except ClientError as e:
      return(e.response['Error']['Message'])
  else:
      print('Email Sent!')
      return("Message ID:" + response['MessageId'] )
