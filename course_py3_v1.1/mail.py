import smtplib
import getpass
from email.mime.text import MIMEText

def sendMail(sender,password,to,subject,body):

    server='smtp.qq.com'
    port=587

    tolist=to.split(',')
    mBody=MIMEText(body)

    header='To:'+to+'\n'
    header=header+'From:'+sender+'\n'
    header=header+'Subject:'+subject+'\n'
    message=header+mBody.as_string()
 
    try:
        smtpserver=smtplib.SMTP(server,port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(sender,password)
        smtpserver.sendmail(sender,tolist,message)
        print('succeeded to send a mail')
    except smtplib.SMTPException:
        print('failed to send a mail')
    smtpserver.quit()

def main():

    sender=input('Please enter your e-mail address: ')
    password=getpass.getpass('Please enter the password: ')
    to=input('Please enter the account you want to send to: ')
    subject=input('Please enter the subject: ')
    body=input('Please enter the message: ')

    sendMail(sender,password,to,str(subject),str(body))

if __name__=='__main__':
    main()
