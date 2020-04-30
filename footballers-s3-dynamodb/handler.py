import boto3

client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('footballers')

def uploadCSVDynamo(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    resp = client.get_object(Bucket=bucket, Key=filename)
    data = resp['Body'].read().decode('utf-8')
    footballers = data.split('\n')
    
    for f in footballers:
        f = f.split(',')
        table.put_item(
            Item={
                'id': f[0],
                'first_name': f[1],
                'last_name': f[2],
            }
        )
