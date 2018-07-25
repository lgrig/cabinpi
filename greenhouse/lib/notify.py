from tools.connection import Connection
from email import mime
from datetime import datetime
import smtplib

class Notify():
    def __init__(self, notification_type):
        pass

    def generate_email(self, to_address=None):
        # Create the container (outer) email message.
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = mime.multipart.MIMEMultipart()
        msg['Subject'] = 'greenhouse update: {}'.format(now)
        msg['From'] = 'leegrignon@gmail.com'
        msg['To'] = to_address or msg['From']



