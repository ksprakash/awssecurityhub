import boto3
import logging
import os
#from datetime import datetime
import csv
from  utilities import *
from secutityhub import SecutityHub
from send_email import send_email_to_recipients
from push_to_s3_bucket import upload_file

#Set these variables in Lambda Environments Section
FILENAME=os.environ.get("FILENAME")
SMTP_HOST=os.environ.get("SMTP_HOST")
EMAIL_TO=os.environ.get("EMAIL_TO")
EMAIL_FROM=os.environ.get("EMAIL_FROM")
PORT=os.environ.get("PORT",465)
PASSWORD=os.environ.get("PASSWORD")

#Lambda has option to store temporarily in /tmp file system
DIRECTORY='/tmp'
#Initialize security hub client
client = boto3.client('securityhub',region_name="us-east-1")
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

def lambda_handler(event,context):
    def get_findings():
        """Fetch All the Findings in Security Hub"""
        response = client.get_findings(MaxResults=100)
        data = response.get("Findings")
        while 'NextToken' in response and response.get('NextToken'):
            token = response.get('NextToken')
            response = client.get_findings(MaxResults=100,NextToken=token)
            data += response.get("Findings")
        return data
        
    def get_info_by_company_name(self,companyname='AWS'): 
        #Allowed Values are AWS and Personal
        with open(file=f'/tmp/{FILENAME}',mode='w+',newline='')  as csvfile: 
            fieldnames=["ProductName","CompanyName","Severity","WorkflowState","RecordState","Compliance","Region","Types","ResourceId","ResourceType","Title","Description","UpdatedAt"]
            csv_writer = csv.DictWriter(csvfile,fieldnames=fieldnames) 
            csv_writer.writeheader()
            entire_response  = get_findings()
            for items in entire_response:
                security_hub_object = SecutityHub(**items)
                if security_hub_object.CompanyName == "AWS":
                    csv_writer.writerow({
                    "ProductName":security_hub_object.ProductName,
                    "CompanyName":security_hub_object.CompanyName,
                    "Severity": security_hub_object.Severity.get("Label"),
                    "WorkflowState":security_hub_object.WorkflowState,
                    "RecordState":security_hub_object.RecordState,
                    "Compliance": security_hub_object.Compliance.get("Status"),
                    "Region":security_hub_object.Region,
                    "Types":security_hub_object.Types,
                    "ResourceId":security_hub_object.Resources['Id'],
                    "ResourceType":security_hub_object.Resources['Type'],
                    "Title":security_hub_object.Title,
                    "Description":security_hub_object.Description,
                    "UpdatedAt":convert_from_str_date(security_hub_object.UpdatedAt) })
            send_email_to_recipients(DIRECTORY,EMAIL_TO, SMTP_HOST, PORT, EMAIL_FROM, PASSWORD)
            #upload_file(filename,bucket_name,object)
    get_info_by_company_name(companyname='AWS')       
