import smtplib

"""
    Establishes connection to SMTP google server
    Writes/sends email with passed in information
"""

class EmailAdapter:

    # Server
    HOST = 'smtp.gmail.com'
    PORT = '587'

    # Sender email and password
    fromEmail = 'aymohamed4@gmail.com'  # any email with 2-step verification
    password = 'egmzxzfjxrhhktib'   # 16 character app password created from Google's 2-step verification page

    def __init__(self):
        self.connectToServer()

    # Server connection process
    def connectToServer(self):
        smtp = self.smtp = smtplib.SMTP(EmailAdapter.HOST, EmailAdapter.PORT)

        # Attempt connection and show status
        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")
        
        # Attempt login and show status
        status_code, response = smtp.login(EmailAdapter.fromEmail, EmailAdapter.password)
        print(f"[*] Logging in: {status_code} {response}")


    # Pass email data
    def sendEmail(self, receiver, message):
        # Send email
        print(f"[*] Sending email: {receiver}")
        self.smtp.sendmail(EmailAdapter.fromEmail, receiver, message)
        
    
    # Close connection to server
    def closeConnection(self):
        self.smtp.quit()
