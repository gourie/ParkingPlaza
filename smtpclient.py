__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.parser import Parser
from email.mime.text import MIMEText

class smtpclient:
    '''
    Class smtpclient sets up connection to the Google SMPT server using admin@parking-plaza.com
    @params: server
    '''

    def __init__(self, email, pw):
        """Constructor to load emailclient
        :return: none
        """
        self.MYEMAIL = email
        self.MYPW = pw
        self.headers = ""

    def __del__(self):
        """
        Destructor
        :return: none
        """
        try:
            status = self.server.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1

        if status == 250:
            self.server.quit()

    def enableLogging(self, level):
        """
        Initiate server to GMAIL SMTP and login
        :param level: debuglevel
        :return:
        """
        self.server.set_debuglevel(level)

    def connectToGMailServer(self, debuglevel):
        """
        Initiate server to GMAIL SMTP and login
        :return:
        """
        self.server = smtplib.SMTP_SSL("smtp.gmail.com:465")
        self.enableLogging(debuglevel)
        self.server.ehlo()
        self.server.login(self.MYEMAIL, self.MYPW)

    def sendEmail(self, toaddr, messagefile, fromaddr, subject="none", attachmentlink="none"):
        """
        Send email with plain text using Google SMTP
        :param toaddr: to address, list of email addresses
        :param messagefile: message header + body as plain text
        :param fromaddr: from address, default to admin@parking-plaza.com user
        :return: result message received from GMAIL
        """
        try:
            msg = MIMEMultipart()

            msg['Subject'] = subject
            msg['From'] = fromaddr
            msg['Reply-to'] = fromaddr
            temp = ""
            for index, addr in enumerate(toaddr):
                if index == (len(toaddr) - 1):
                    temp += addr
                else:
                    temp += addr + ','
            msg['To'] = temp
            msg.preamble = 'Multipart message.\n'

            with open(messagefile, 'r') as file:
                part = MIMEText(Parser().parse(file).as_string())
                msg.attach(part)

            # This is the binary part(The Attachment):
            if attachmentlink!="none":
                partAttachment = MIMEApplication(open(attachmentlink,"rb").read())
                partAttachment.add_header('Content-Disposition', 'attachment', filename=attachmentlink)
                msg.attach(partAttachment)

            self.connectToGMailServer(0)
            #self.server.sendmail(fromaddr, toaddr, self.headers.as_string())
            res = self.server.sendmail(msg['From'], toaddr, msg.as_string())
            self.server.quit()
            return res

        except smtplib.SMTPAuthenticationError as e:
            print("Authentication Error: ",e)
            return e

        except smtplib.SMTPConnectError as e:
            print("SMTP Connect Error: ",e)
            return e

        except smtplib.SMTPServerDisconnected as e:
            print("SMTP Server Disconnected Error: ",e)
            return e

        except smtplib.SMTPRecipientsRefused as e:
            print("SMTP Recipients Refused: ",e)
            return e

        except smtplib.SMTPException as e:
            print("SMTP General Exception: ",e)
            return e
