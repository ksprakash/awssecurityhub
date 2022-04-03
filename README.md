STEPS TO FOLLOW
1. In lambda_function.py: create below as environment variables in Lambda Service in Environment Section; Ex: SMTP_HOST=smtp.gmail.com
<<< 
FILENAME=os.environ.get("FILENAME")
SMTP_HOST=os.environ.get("SMTP_HOST")
EMAIL_TO=os.environ.get("EMAIL_TO")
EMAIL_FROM=os.environ.get("EMAIL_FROM")
PORT=os.environ.get("PORT",465)
PASSWORD=os.environ.get("PASSWORD")
>>>

2. 
mkdir -p lambda_project
cd lambda_project 
create virtual environment in local computer 
python -m venv venv
source venv/bin/activate
#paste  requirements.txt here
pip install --no-cache-dir -r requirements.txt
cd venv/lib/python3.10/site-packages
#Paste other python file here and make zip file, make sure lambda_function.py is immediate file in zip #Make sure try unzipping to see direct python files not folder.

finally upload to s3 bucket and use s3 location in lambda .


