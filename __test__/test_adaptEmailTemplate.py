__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

import adaptEmailTemplate
import difflib
import unittest

result = []

class init_notifyOwnerToSetSchedule(unittest.TestCase):

    def testObjectInitialization(self):
        # Test normal case
        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            self.assertEqual(templ.contenturl, "./content", "content url not initiated properly")
        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)


with open('./content/ownernotificationemail', 'r') as file:
    outputemail=file.read()
with open('./content/ownernotification-email-template', 'r') as file:
    template=file.read()
outputemail_words=outputemail.split()
template_words=template.split()
d = difflib.Differ()

class adaptNotifyOwnerEmailTemplate(unittest.TestCase):

    def testHappyFlowUsername(self):
        # Test normal case
        # (username, unitaddress, eventdescription, eventdate, setschedulelink):

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[0][2:], 'Jef,', "username not replaced with Jef")

    def testHappyFlowUnitaddress(self):
        # Test normal case

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[1][2:], 'Testaddress1', "unit address not replaced with Test address1")

    def testHappyFlowParkingStart(self):
        # Test normal case

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[5][2:], '30/5/2016-17:00', "parking start date not replaced with 30/5/2016-17:00")

    def testHappyFlowParkingEnd(self):
        # Test normal case

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[6][2:], '20:00', "parking start date not replaced with 20:00")

    def testHappyFlowEventdescription(self):
        # Test normal case

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[2][2:], 'Test123', "eventdescription not replaced with Test123 - 30/5/2016")
        self.assertEqual(result[3][2:], '-', "eventdescription not replaced with Test123 - 30/5/2016")
        self.assertEqual(result[4][2:], '30/5/2016', "eventdescription not replaced with Test123 - 30/5/2016")

    def testHappyFlowUrl(self):
        # Test normal case

        try:
            templ = adaptEmailTemplate.adaptEmailTemplate("./content")
            templ.adaptNotifyOwnerEmailTemplate('Jef', 'Testaddress1', 'Test123 - 30/5/2016', '30/5/2016-17:00', '20:00', 'http://url:port')
            for word in list(d.compare(template_words,outputemail_words)):
                if '+' in word:
                    result.append(word)

        except Exception, e:
            print('test_adaptEmailTemplate / verifyObjectInitialization error: ', e)

        self.assertEqual(result[len(result)-1][2:], 'http://url:port', "url not replaced with 'http://url:port'")

if __name__ == '__main__':
    unittest.main()
