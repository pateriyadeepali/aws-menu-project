from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# Initialize Boto3 clients
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')
ses_client = boto3.client('ses')

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/aws_operations', methods=['POST'])
def aws_operations():
    operation = request.form['operation']
    
    if operation == 'launch_ec2':
        launch_ec2_instance()
    elif operation == 'list_s3':
        list_s3_buckets()
    elif operation == 'create_lambda':
        create_lambda_function()
    elif operation == 'send_email':
        send_email_via_ses()
    
    return 'Operation completed successfully.'

# AWS operations functions (similar to previous example)

def launch_ec2_instance():
    print("Launching EC2 Instance...")
    # Modify the parameters as per your requirements
    response = ec2_client.run_instances(
        ImageId='ami-12345678',  # Example AMI ID
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 Instance {instance_id} launched successfully!")

def list_s3_buckets():
    print("Listing S3 Buckets...")
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(f"Bucket Name: {bucket['Name']}")

def create_lambda_function():
    print("Creating Lambda Function...")
    # Modify the parameters as per your requirements
    response = lambda_client.create_function(
        FunctionName='MyLambdaFunction',
        Runtime='python3.8',
        Role='arn:aws:iam::123456789012:role/lambda-execution-role',  # Example IAM Role ARN
        Handler='lambda_function.lambda_handler',
        Code={
            'S3Bucket': 'my-lambda-code-bucket',
            'S3Key': 'lambda_function.zip'
        },
        Description='My first Lambda function',
        Timeout=30,
        MemorySize=128
    )
    print(f"Lambda Function {response['FunctionName']} created successfully!")

def send_email_via_ses():
    print("Sending Email via SES...")
    # Modify the parameters as per your requirements
    response = ses_client.send_email(
        Source='sender@example.com',
        Destination={
            'ToAddresses': ['recipient1@example.com', 'recipient2@example.com']
        },
        Message={
            'Subject': {
                'Data': 'Test email'
            },
            'Body': {
                'Text': {
                    'Data': 'This is a test email sent via SES'
                }
            }
        }
    )
    print("Email sent successfully!")

if __name__ == '__main__':
    app.run(debug=True)
