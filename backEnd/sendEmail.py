from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import webbrowser

class sendEmail():
    
    #server
    HOST = 'smtp.gmail.com'
    PORT = '587'

    #sender email and password
    fromEmail = "mf.mindfreaks99@gmail.com"  # any email with 2-step verification
    password = "klffdzkaeugwsgrs"  # 16 character app password created from Google's 2-step verification page

    def hyperLink(self, linkText, destination):
        
        link_text = linkText
        url = destination

        # Creating a hyperlink in HTML
        hyperlink = '<a href="{}">{}</a>'.format(url, link_text)
        
        return hyperlink
    
    # def emailFormat(self, sender, resiver, subject, body):
        
    #Server connection process
    def connectToServer(self):
        smtp = smtplib.SMTP(self.HOST, self.PORT)

        #show status
        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")
        

        return smtp
    
    def pinRecovery(self, email):

        # Creating a hyperlink in HTML
        hyperlink = self.hyperLink("Click here", "https://www.linkedin.com/in/mohamed-kaid-moe1996/")


        sender = self.fromEmail
        email_pass = self.password

        resiver = email

        subject = "docTracker Pin Recovery"
        body_html = f"""
            <html>
            <body>
                <p>Hi there,</p>
                <p>This email was sent to help you recover your pin for your account. {hyperlink} and follow the steps.</p>
                <p>Thank you and have a nice day!!!</p>
            </body>
            </html>
            """
        
        
        em = MIMEMultipart('alternative')
        em['From'] = sender
        em['To'] = resiver
        em['Subject'] = subject
        em.attach(MIMEText(body_html, 'html'))
        
        context = ssl.create_default_context()
        try:
            smtp = self.connectToServer()
            smtp.login(sender, email_pass)
            smtp.sendmail(sender, resiver, em.as_string())
        
        except Exception as e:
            print("An error occurred:", str(e))
            raise
        
        finally:
            smtp.quit()
