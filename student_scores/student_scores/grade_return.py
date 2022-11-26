
 #Function takes in the message from SNS and returns the message in cloud watch logs

def lambda_handler(event, context):    
    message = event['Records'][0]['Sns']['Message']
    print(message)