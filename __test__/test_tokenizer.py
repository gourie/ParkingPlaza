__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime, timedelta
from pytz import timezone
import json
import jwt
import tokenize
import unittest

# application config settings
with open('./config.json', 'r') as file:
    conf = json.loads(file.read())

TIMEZONE = str(conf['timezone'])
tokenizer = tokenize.tokenize(conf['secret'], TIMEZONE)
testUUID = 'test123'
testpoieventid = 10
testunitid = 5
testpoieventdescription = 'R.S.C.A. Test'
testunitname = 'A1'
tokentamper = "ABC"


class getToken(unittest.TestCase):

    def testGetTokenCorrectUUID(self):
        # Test normal case

        try:
            token = tokenizer.createUUIDToken(testUUID)
        except Exception, e:
            print('exception in testGetToken' + e)
        self.assertEqual(tokenizer.getClaims(token)['sub'], testUUID, "token doesn't contain the correct test uuid")

    def testGetTokenCorrectPoiEventid(self):
        # Test normal case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        except Exception, e:
            print('exception in testGetToken' + e)
        self.assertEqual(tokenizer.getClaims(token)['poieventid'], testpoieventid, "token doesn't contain the correct test poieventid")

    def testGetTokenCorrectUnitid(self):
        # Test normal case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        except Exception, e:
            print('exception in testGetToken' + e)
        self.assertEqual(tokenizer.getClaims(token)['unitid'], testunitid, "token doesn't contain the correct test unitid")

    def testGetTokenNotPossibleAfterTampering(self):
        # Test exception case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
            token += tokentamper
            err = tokenizer.getClaims(token)['unitid']
            print('bal')
        except Exception, e:
            self.assertIsInstance(e, jwt.DecodeError, "trying to get claims from tampered token doesn't return jwt.DecodeError")

class checkTokenHealth(unittest.TestCase):

    def testisValidTokenUUIDToken(self):
        # Test normal case

        try:
            token = tokenizer.createUUIDToken(testUUID)
        except Exception, e:
            print('exception in testisValidTokenUUIDToken' + e)
        self.assertEqual(tokenizer.isValidToken(token), True, "UUID token is not detected as valid")

    def testisValidTokenSetScheduleToken(self):
        # Test normal case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        except Exception, e:
            print('exception in testisValidTokenSetScheduleToken' + e)
        self.assertEqual(tokenizer.isValidToken(token), True, "SetSchedule token is not detected as valid")

    def testStillvalidTokenAfterTampering(self):
        # Test exception case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
            token += tokentamper
            err = tokenizer.isValidToken(token)
            print('')
        except jwt.DecodeError, e:
            self.assertEqual(e, err, "Tampered token is not detected as valid")


class createToken(unittest.TestCase):

    def testCreateSetScheduleTokenCorrectPoiEventid(self):
        # Test normal case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        except Exception, e:
            print('exception in testCreateSetScheduleTokenCorrectPoiEventid' + e)
        self.assertEqual(testpoieventid, tokenizer.getClaims(token)['poieventid'], "createSetScheduleToken doesn't contain the correct test poieventid")

    def testCreateSetScheduleTokenCorrectUnitid(self):
        # Test normal case

        try:
            token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        except Exception, e:
            print('exception in testCreateSetScheduleTokenCorrectUnitid' + e)
        self.assertEqual(testunitid, tokenizer.getClaims(token)['unitid'], "createSetScheduleToken doesn't contain the correct test unitid")

    def testCreateSetScheduleTokenCorrectExpDate(self):
        # Test normal case

        token = tokenizer.createSetScheduleToken(testpoieventid, testunitid)
        self.assertLess(tokenizer.getClaims(token)['exp'], (timezone(TIMEZONE).localize(datetime.now()) + timedelta(days=1, seconds=5) - (timezone(TIMEZONE).localize(datetime(1970,1,1)))).total_seconds(), "createSetScheduleToken doesn't contain the correct expiration date")

    def testCreateScheduleTokenCorrectPoiEventdescription(self):
        # Test normal case

        try:
            token = tokenizer.createScheduleToken(testpoieventdescription, testunitname)
        except Exception, e:
            print('exception in testCreateScheduleTokenCorrectPoiEventdescription' + e)
        self.assertEqual(testpoieventdescription, tokenizer.getClaims(token)['eventdescription'], "createScheduleToken doesn't contain the correct test poieventdescription")

    def testCreateScheduleTokenCorrectUnitname(self):
        # Test normal case

        try:
            token = tokenizer.createScheduleToken(testpoieventdescription, testunitname)
        except Exception, e:
            print('exception in testCreateScheduleTokenCorrectUnitname' + e)
        self.assertEqual(testunitname, tokenizer.getClaims(token)['unitname'], "createScheduleToken doesn't contain the correct test unitname")

    def testCreateScheduleTokenCorrectExpDate(self):
        # Test normal case

        token = tokenizer.createScheduleToken(testpoieventdescription, testunitname)
        self.assertLess(tokenizer.getClaims(token)['exp'], (timezone(TIMEZONE).localize(datetime.now()) + timedelta(days=8, seconds=5) - (timezone(TIMEZONE).localize(datetime(1970,1,1)))).total_seconds(), "createScheduleToken doesn't contain the correct expiration date")

    def testcreateEmailConfirmationTokenHappyFlow(self):
        """
        Test whether correct email confirmation token has been created and all arguments can be fetched properly.
        """
        token = tokenizer.createEmailConfirmationToken("test@google.be")
        self.assertEqual(tokenizer.getClaims(token)['emailaddress'], "test@google.be", "createEmailConfirmationToken doesn't contain the correct email address")
        self.assertLess(tokenizer.getClaims(token)['exp'], (timezone(TIMEZONE).localize(datetime.now()) + timedelta(days=7, seconds=5) - (timezone(TIMEZONE).localize(datetime(1970,1,1)))).total_seconds(), "createEmailConfirmationToken doesn't contain the correct expiration date")

if __name__ == '__main__':
    unittest.main()
