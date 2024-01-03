from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from services.EmailAdapter import *

"""
    Creates the email content based on the type of email being sent and passes to an email adapter.
        - Recovery email: passing link to reset pin
        - Notification email: displaying documents expiring within a month
"""

class EmailService:

    def __init__(self):
        # Instantiate email adapter
        self.adapter = EmailAdapter()

    def sendEmail(self, receiver, data, type):
        # Create email content
        if type == 'reset':
            subject, body = EmailService.createResetEmailContent(data)
        elif type == 'notification':
            subject, body = EmailService.createNotificationEmailContent(data)
        else:
            raise Exception    
        
        # Set email attributes
        content = MIMEMultipart('alternative')
        content['From'] = EmailAdapter.fromEmail
        content['To'] = receiver
        content['Subject'] = subject
        content.attach(MIMEText(body, 'html'))

        # Send email
        self.adapter.sendEmail(receiver, content.as_string())


    def createResetEmailContent(link):
        # Hyperlink
        text = "Click here"
        hyperlink = '<a href="{}">{}</a>'.format(link, text)

        # Subject
        subject = "docTracker Pin Recovery"

        # Body
        body_html = f"""
            <html>
            <body>
                <p>Hi there,</p>
                <p>This email was sent to help you recover your pin for your account. { hyperlink } and follow the steps.</p>
                <p>Thank you and have a nice day!!!</p>
            </body>
            </html>
            """
        
        return subject, body_html
    
    
    def createNotificationEmailContent(documents):
        # Subject
        subject = "Weekly Notification"

        # Body
        body_html = f"""
            <html>
            <body>
                <p>Documents expiring soon:</p>
        """

        # Loop documents
        for document in documents:
            body_html += f"<p>{ document.driverName } { document.name } { document.date }</p>"

        body_html += """
            </body>
            </html>
        """
                            
        return subject, body_html
        

    # Close adapter
    def close(self):
        self.adapter.closeConnection()