import boto3
import simplejson as json    #importing all dependancies
import os
import logging

logger = logging.getLogger('gradecalculator')   #logging helps print log messages
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
sns_client = boto3.client('sns')   #retreiving resources from boto3


def lambda_handler(event, context): #retreiving values from the message
    topic = os.environ.get('STUDENT_SCORE_TOPIC')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    logger.info('The {} is being read to get the objects from it'.format(bucket_name))

    obj = s3.get_object(Bucket= bucket_name, Key=file_key)   #get the particular bucket from s3
    file_content = obj['Body'].read().decode('utf-8') #turning the object data from s3 into readable format
    student_scores = json.loads(file_content)  #turning the json into dictionary text to loop through it    

    logger.info('Checking each student in the list and grading them')

    for each_student in student_scores: #loops through each item in the score pairs and grades it

        print(each_student) 

        if each_student['score'] > 70:
            each_student['grade'] = 'A'

        if  60 > each_student['score'] < 70:
            each_student['grade'] = 'B'
        
        if each_student['score'] < 60 :
            each_student['grade'] = 'C'

            
        sns_client.publish(  #publish our message to SNS
            TopicArn =topic,
            Message= json.dumps({'default': json.dumps(each_student)}),   #turns the message into json format to publish to SNS
            MessageStructure= 'json',
        )

