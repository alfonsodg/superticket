EMAIL_SERVER="smtp.gmail.com:587"
EMAIL_SENDER="registro@maccticket.com"
EMAIL_PASSWORD="654321" ## your assword

def email(sender,to,subject,message):
   import smtplib
   fromaddr=sender
   if type(to)==type([]): toaddrs=to
   else: toaddrs=[to]
   msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,\
       ", ".join(toaddrs),subject,message)
   server = smtplib.SMTP(EMAIL_SERVER)
   server.ehlo()
   server.starttls()
   server.ehlo()
   username=EMAIL_SENDER
   password=EMAIL_PASSWORD
   server.login(username, password)
   server.sendmail(fromaddr, toaddrs, msg)
   server.quit()
