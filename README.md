### AWS Lambda container deploy CI/CD

A CI/CD pipeline triggerd by any push to master branch, that build and push new AWS lambda docker image to AWS ECR registry, and update AWS lambda image uri.
The AWS Lambda function triggerd by every S3 upload file action, and email the file's type and S3 URI to specefied mail address.

## Getting Started

### Installation


1. Clone the repo    
   ```sh
   git clone https://github.com/omerharush93/Viz.aiTask.git
   ```
3. Install docker

4. Install aws-cli

5. Configure aws credentials using "aws configure"


### Build the container for AWS Lambda

```
docker build -t lambda_test . 
```

### Run the AWS Lambda container for local test

Let's start the container to test the lambda locally :

```
docker run -d -p 9000:8080 lambda_test:latest
```

### Test the Lambda locally

To test the application locally post an event to the following endpoint using a curl command:

```
{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "eu-west-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "omer-test-bucket",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::example-bucket"
        },
        "object": {
          "key": "1.txt",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}'
```

See the container logs :
```
(fastapi-lambda-container) gbdevw@gbdevw-dev:~/python-fastapi-aws-lambda-container$ docker run -p 9000:8080 hello-world:latest
time="2021-12-03T01:31:13.892" level=info msg="exec '/var/runtime/bootstrap' (cwd=/var/task, handler=)"
time="2021-12-03T01:31:18.345" level=info msg="extensionsDisabledByLayer(/opt/disable-extensions-jwigqn8j) -> stat /opt/disable-extensions-jwigqn8j: no such file or directory"
time="2021-12-03T01:31:18.345" level=warning msg="Cannot list external agents" error="open /opt/extensions: no such file or directory"
START RequestId: 763c6861-fff4-4576-8661-5f2a15e088fd Version: $LATEST
CONTENT TYPE: text/plain
Email Sent!
END RequestId: 763c6861-fff4-4576-8661-5f2a15e088fd
REPORT RequestId: 763c6861-fff4-4576-8661-5f2a15e088fd	Duration: 712.26 ms	Billed Duration: 713 ms	Memory Size: 128 MB	Max Memory Used: 75 MB	
```

And the lambda output :

```json
{
  "StatusCode": 200,
  "Message": "SUCCESS"
}
```
