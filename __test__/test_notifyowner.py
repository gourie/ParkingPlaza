__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime
import db_logic
import json
import notifyOwner
from pytz import timezone
import requests
import tokenize
import unittest

testpoieventid = 10
testunitid = 1

# application config settings
with open('./config.json', 'r') as file:
    conf = json.loads(file.read())
SERVER_URL = conf['dev-server']
SERVER_PORT = int(conf['dev-port'])
TIMEZONE = str(conf['timezone'])
tokenizer = tokenize.tokenize(conf['secret'], TIMEZONE)
serverparkingsetscheduleurl = "/parkings/setSchedule"
parkingDb = db_logic.db_logic("Benares-dev", "localhost", "5432", "ParkingPlaza", "BENARES")
parkingDb.ConnectToDb()

ownerNotification = notifyOwner.notifyOwnerToSetSchedule(SERVER_URL + ":" + str(SERVER_PORT), serverparkingsetscheduleurl, "email", "support@parking-plaza.com", "./content", "/ownernotificationemail", "Unit-test NotifyOwnerToSetSchedule", 5, tokenizer, parkingDb)

class notifyOwnerToSetSchedule(unittest.TestCase):

    def testObjectInitialization(self):
        # Test normal case

        # try:
        #
        # except Exception, e:
        #     print('test_notifyowner / verifyObjectInitialization error: ', e)
        ownerNotiftest = notifyOwner.notifyOwnerToSetSchedule(SERVER_URL + ":" + str(SERVER_PORT), serverparkingsetscheduleurl, "email", "support@parking-plaza.com", "./content", "/ownernotificationemail", "Unit-test NotifyOwnerToSetSchedule", 5, tokenizer, parkingDb)
        self.assertEqual(ownerNotiftest.serverurl, "http://localhost:8888", "server url not initiated properly")
        self.assertEqual(ownerNotiftest.notification, "email", "notification type not initiated properly")
        self.assertEqual(ownerNotiftest.supportemail, "support@parking-plaza.com", "support email not initiated properly")

    def testGenerateOwnerSetScheduleUrlReturnsString(self):
        # Test normal case

        url = ownerNotification.generateOwnerSetScheduleUrl(testpoieventid, testunitid)
        self.assertIsInstance(url, basestring, "GenerateOwnerSetScheduleUrl doesn't return a string")

    def testGenerateOwnerSetScheduleUrlFullUrlOK(self):
        # Test normal case

        url = ownerNotification.generateOwnerSetScheduleUrl(testpoieventid, testunitid)
        token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        self.assertEqual(url, "%s:%d" % (SERVER_URL, SERVER_PORT) + "/parkings/setSchedule?token=" + token, "GenerateOwnerSetScheduleUrl - url string not correct")

    def testgenerateDatetimeStringHappyFlow(self):
        """
        Check whether correct time string is returned for 'Europe/Brussels'
        """
        for i in range(12):
            testdate = timezone(TIMEZONE).localize(datetime(year=2016, month=8, day=10, hour=i+10, minute=0))
            result = ownerNotification.generateDatetimeString(testdate, TIMEZONE)
            self.assertEqual(result, "Wednesday 10 August 2016 %d:00" % (i+10), "generateDatetimeString doesn't return the right datetime string for Europe/Brussels")
            i=i+1

    def testgenerateDatetimeStringExceptionWrongTz(self):
        """
        Check whether empty time string is returned for 'Europe/Amsterdam'
        """
        tz = 'Europe/Amsterdam'
        testdate = timezone(tz).localize(datetime(year=2016, month=8, day=10, hour=10, minute=0))
        result = ownerNotification.generateDatetimeString(testdate, tz)
        self.assertEqual(result, "", "generateDatetimeString doesn't return an empty datetime string for Europe/Amsterdam")

    def testfindOwnersWhoNeedToSetScheduleHappyFlowTotalItems(self):
        # Happy flow : test whether number of items returned is 4
        # startdate & daysbeforeevent chosen explicitly to return these results

        list = ownerNotification.findOwnersWhoNeedToSetSchedule(timezone(TIMEZONE).localize(datetime(2016, 6, 7, 20, 0, 0)), 5, unittest=True)
        self.assertEqual(len(list), 4, "findOwnersWhoNeedToSetSchedule doesn't return correct number of items")

    def testfindOwnersWhoNeedToSetScheduleHappyFlowFirstItem(self):
        # Happy flow : test content of first item
        # startdate & daysbeforeevent chosen explicitly to return these results
        # REMARK: not possible to test 'setscheduleurl' (contains timestamp so different when re-created for test at later timestamp) but already test before in separate unit-test!!

        list = ownerNotification.findOwnersWhoNeedToSetSchedule(timezone(TIMEZONE).localize(datetime(2016, 6, 7, 20, 0, 0)), 5, unittest=True)
        self.assertEqual(list[0]['eventdescription'], 'R.S.C. Anderlecht - Test3', "findOwnersWhoNeedToSetSchedule doesn't return correct eventdescription for first item")
        self.assertEqual(list[0]['eventstart'], 'Friday 10 June 2016 18:00', "findOwnersWhoNeedToSetSchedule doesn't return correct parking start for first item")
        self.assertEqual(list[0]['eventendhour'], '22:00', "findOwnersWhoNeedToSetSchedule doesn't return correct parking end for first item")
        self.assertEqual(list[0]['unitaddress'], 'Teststraatt 2, Anderlecht, Belgium', "findOwnersWhoNeedToSetSchedule doesn't return correct unit address for first item")
        self.assertEqual(list[0]['ownername'], 'test user2', "findOwnersWhoNeedToSetSchedule doesn't return correct ownername for first item")
        self.assertEqual(list[0]['owneremail'], 'test2@parking-plaza.com', "findOwnersWhoNeedToSetSchedule doesn't return correct owneremail for first item")

class setScheduleAPITestCases(unittest.TestCase):

    def testsetscheduleAPIHandlerHappyflow(self):
        """
        Normal case
        """
        ownerNotification = notifyOwner.notifyOwnerToSetSchedule(SERVER_URL + ":" + str(SERVER_PORT), serverparkingsetscheduleurl, "email", "support@parking-plaza.com", "./content", "/ownernotificationemail", "Unit-test NotifyOwnerToSetSchedule", 5, tokenizer, parkingDb)
        url = ownerNotification.generateOwnerSetScheduleUrl(testpoieventid, testunitid)
        r = requests.get(url)
        self.assertEqual(r.status_code, 200, "testsetscheduleAPIHandlerHappyflow doesn't reply with 200 OK")


if __name__ == '__main__':
    unittest.main()
