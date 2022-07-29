import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class NotificationManager:
    """Configures and sends the email"""

    def __init__(self):
        """Configures the email addresses and password"""

        self.sender_address = "mihaila.adrian.and.joanne@gmail.com"
        self.sender_pass = "oebxjqjkuolumvlf"

    def send_email(self, mail_content, receiver_address_list):
        """Sends the email"""

        receiver_address = receiver_address_list

        # Setup the MIME
        message = MIMEMultipart()
        message["From"] = self.sender_address
        message["To"] = ", ".join(receiver_address)  # receiver_address Needs to be a STRING
        message["Subject"] = "Low price alert"  # The subject line

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, "html"))

        # Create SMTP session for sending the mail
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # enable security
            connection.login(self.sender_address, self.sender_pass)  # login with mail_id and password
            text = message.as_string()
            connection.sendmail(self.sender_address, receiver_address, text)  # receiver_address Needs to be a LIST
        print("Mail Sent")
