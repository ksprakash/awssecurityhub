import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email.mime.image import MIMEImage
#from email.mime.application import MIMEApplication
import os
import mimetypes
#Create a directory and keep all files in that location that will attach all files.
def send_email_to_recipients(directory,to_email, server, port,from_email, password):
    
    # Create the message
    subject = 'AWS Security Hub Findings'
    body = '''Lambda Generated CSV File for Security Hub Findings'''
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
    # Open communication and send
    server = smtplib.SMTP_SSL(server, port)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

