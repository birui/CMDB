#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import os,sys
import getopt
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from  subprocess import *
reload(sys)
sys.setdefaultencoding( "utf-8" )


def sendgmail(username,password,mailfrom,mailto,subject,content):
    gserver = 'smtp.gmail.com'
    gport = 587

    msg = MIMEText(unicode(content).encode('utf-8'))
    msg['from'] = mailfrom
    msg['to'] = mailto
    msg['Reply-To'] = mailfrom
    msg['Subject'] = subject

    smtp = smtplib.SMTP(gserver, gport)
    smtp.set_debuglevel(0)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username,password)

    smtp.sendmail(mailfrom, mailto, msg.as_string())
    smtp.close()
    
def sendqqmail(username,password,mailfrom,mailto,subject,content):
    gserver = 'smtp.exmail.qq.com'
    gport = 25
    
    try:
        msg = MIMEText(unicode(content).encode('utf-8'))
        msg['from'] = mailfrom
        msg['to'] = mailto
        msg['Reply-To'] = mailfrom
        msg['Subject'] = subject
        
        smtp = smtplib.SMTP(gserver, gport)
        smtp.set_debuglevel(0)
        smtp.ehlo()
        smtp.login(username,password)
        
        smtp.sendmail(mailfrom, mailto, msg.as_string())
        smtp.close()
    except Exception,err:
        print "Send mail failed. Error: %s" % err
    
    
def main():
    to=sys.argv[1]
    subject=sys.argv[2]
    content=sys.argv[3]
    sendqqmail('test@22.com','ssss','##@11.com',to,subject,content)

if __name__ == "__main__":
    main()
