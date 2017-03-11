__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime
import json
import smtpclient
import smtplib
import unittest

# application config settings
with open('./config.json', 'r') as file:
    conf = json.loads(file.read())

TESTEMAIL = "gourie53@gmail.com"
WRONGTESTEMAIL = "[gourie53@gmail.com"

class testInitEmail(unittest.TestCase):

    def testObjectInitialization(self):
        # Test normal case

        try:
            emailclient = smtpclient.smtpclient(conf['support-email'], conf['support-pw'])
        except Exception, e:
            print('test_smptclient / testObjectInitialization error: ', e)

        self.assertEqual(emailclient.MYEMAIL, conf['support-email'], "support email not initiated properly")
        self.assertEqual(emailclient.MYPW, conf['support-pw'], "support pw not initiated properly")

    def testConnectToMailserverHappyFlow(self):
        # Test normal case

        try:
            emailclient = smtpclient.smtpclient(conf['support-email'], conf['support-pw'])
            r = emailclient.connectToGMailServer(3)
            self.assertEqual(r, None, "connection to GMAIL succeed - see log messages for 250 OK message")
        except Exception, e:
            print('test_smptclient / testConnectToMailserver error: ', e)

    def testConnectToMailserverWrongUsername(self):
        # Test exception case

        try:
            emailclient = smtpclient.smtpclient('blabla', "bal")
            r = emailclient.connectToGMailServer(3)
        except smtplib.SMTPAuthenticationError, e:
            self.assertEqual(e[0], 535 , "connection to GMAIL did not fail with username error - see log messages")

    def testConnectToMailserverWrongPW(self):
        # Test exception case

        try:
            emailclient = smtpclient.smtpclient(conf['support-email'], "bal")
            r = emailclient.connectToGMailServer(3)
        except smtplib.SMTPAuthenticationError, e:
            self.assertEqual(e[0], 535 , "connection to GMAIL did not fail with pw error - see log messages")

class testSendEmail(unittest.TestCase):

    def testSendEmailHappyFlow(self):
        # Test normal case

        try:
            emailclient = smtpclient.smtpclient(conf['support-email'], conf['support-pw'])
            r = emailclient.sendEmail([TESTEMAIL], "./content/testemail", conf['support-email'], "Unit-test" + datetime.now().isoformat())
            self.assertEqual(r, None, "send email not ok - see log messages")
        except Exception, e:
            print(e)

    def testSendEmailWrongTo(self):
        # Test exception case

        emailclient = smtpclient.smtpclient(conf['support-email'], conf['support-pw'])
        err = emailclient.sendEmail([WRONGTESTEMAIL], "./content/testemail", conf['support-email'], "Unit-test" + datetime.now().isoformat())
        print(err)
        self.assertEqual(err[0][WRONGTESTEMAIL][0], 555 , "connection to GMAIL did not fail with username error - see log messages")

if __name__ == '__main__':
    unittest.main()
