from mail import Mail

login = 'login@gmail.com'
password = 'qwerty'
subject = 'Subject'
recipients = ['vasya@email.com', 'petya@email.com']
message = 'Message'

if __name__ == '__main__':
    mail = Mail(login, password)
    mail.send()
    mail.receive()
