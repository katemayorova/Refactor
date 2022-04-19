import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    __GMAIL_SMTP = "smtp.gmail.com"
    __GMAIL_IMAP = "imap.gmail.com"
    __SMTP_PORT = 587
    __EMAIL_HEADER = 'ALL'

    def __int__(self, login: str, password: str):
        self.login = login
        self.password = password

    def send(self, recipients: list, subject: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        ms = smtplib.SMTP(self.__GMAIL_SMTP, self.__SMTP_PORT)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, recipients, msg.as_string())

        ms.quit()

    def receive(self):
        mail = imaplib.IMAP4_SSL(self.__GMAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % self.__EMAIL_HEADER

        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = mail.message_from_string(raw_email)
        mail.logout()
        return email_message
