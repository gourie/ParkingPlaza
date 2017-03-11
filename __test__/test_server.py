__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime
import db_logic
import json
import pytz
import readdocument
import requests
import server
import sys
import tokenize
import unittest


parkingDb = db_logic.db_logic("Benares-dev", "localhost", "5432", "ParkingPlaza", "BENARES")
parkingDb.ConnectToDb()

# hard-coded variables:
destination = dict(lat=51.021631, lon=4.478939)
userID = '2577527d-f2b7-4469-91d2-f91663906577'
TEST_USER = "joerinicolaes@gmail.com"
TEST_VALIDUNITNAME = "A1"
TEST_VALIDEVENTDESCRIPTION = "R.S.C. Anderlecht - Test3"

with open('./config.json', 'r') as file:
    conf = json.loads(file.read())
CONTENTFOLDER = conf['content']
HMAC_SECRET = conf['secret']
SERVER_URL = conf['dev-server']
SERVER_PORT = int(conf['dev-port'])
TIMEZONE = str(conf['timezone'])
token = tokenize.tokenize(HMAC_SECRET, TIMEZONE)
TOS_CONTENT = CONTENTFOLDER + conf['tos-doc']

class readConfigFileTestCases(unittest.TestCase):

    def testOpenConfigFileNormalCase(self):
        """
        Open config file and read two entries
        """
        with open('./config.json', 'r') as file:
            conf = json.loads(file.read())
        SERVER_URL = conf['dev-server']
        SERVER_PORT = int(conf['dev-port'])
        HMAC_SECRET = conf['secret']
        token = tokenize.tokenize(HMAC_SECRET, TIMEZONE)
        self.assertEqual(SERVER_URL, "http://localhost", "testOpenConfigFileNormalCase doesn't find correct SERVER_URL")
        self.assertEqual(SERVER_PORT, 8888, "testOpenConfigFileNormalCase doesn't find correct SERVER_PORT")

    def testOpenConfigFileExceptionCaseNoEntry(self):
        """
        Open config file and read entry that doesn't exist
        """
        with open('./config.json', 'r') as file:
            conf = json.loads(file.read())
        try:
            dummy = conf['dummy']
        except KeyError, e:
            self.assertEqual(e[0], "dummy", "testOpenConfigFileExceptionCaseNoEntry doesn't detect keyerror for argument dummy")


class reservationsAPITestCases(unittest.TestCase):

    def testreservationsAPIHandlerExceptionCaseNoCookieProvided(self):
        """
        Try to get reservations for user 1 and compare whether DB call and API yield the same result
        """

        # TODO: @JeroenMachiels to add unit-test for QueryUser in test_db_logic.py to test that function in detail
        usr = parkingDb.QueryUser(TEST_USER)
        req_uri = "%s:%d/reservations" % (SERVER_URL, SERVER_PORT)
        r = requests.get(req_uri)
        self.assertEqual(r.history[0].headers._store['location'][1], "/auth/google-login", "testreservationsAPIHandlerExceptionCaseNoCookieProvided doesn't detect redirect to auth/login")


class scheduleAPITestCases(unittest.TestCase):

    def testscheduleAPIHandlerHappyFlowUnitnameprovided(self):
        """
        Try to call /schedule endpoint with valid unitname and verify if API yields correct data
        """
        req_uri = "%s:%d/schedule" % (SERVER_URL, SERVER_PORT)
        data = { 'unit': TEST_VALIDUNITNAME }
        cookie = {'token': token.createUUIDToken("2577527d-f2b7-4469-91d2-f91663906571")}
        r = requests.post(req_uri, data=data, cookies=cookie)
        # TODO: temp test that just checks if no error is thrown but the given user is not found given that the APIHandler looks in the Benares DB (not Benares-Dev) so doesn't exist
        # workaround to manually test full flow in APIHandler = set ParkingDb to connect to Benares-Dev in server.py (done 10/6 and result positive)
        self.assertEqual(r.status_code, 200, "scheduleAPIHandler doesn't return 200 OK when valid unitname has been provided")

    def testscheduleAPIHandlerHappyFlowSetscheduletokenprovided(self):
        """
        Try to call /schedule endpoint with valid unitname and verify if API yields correct data
        """
        req_uri = "%s:%d/schedule?setscheduletoken=%s" % (SERVER_URL, SERVER_PORT, token.createScheduleToken(TEST_VALIDEVENTDESCRIPTION, TEST_VALIDUNITNAME))
        cookie = {'token': token.createUUIDToken("2577527d-f2b7-4469-91d2-f91663906571")}
        r = requests.get(req_uri, cookies=cookie)
        # TODO: temp test that just checks if no error is thrown but the given user is not found given that the APIHandler looks in the Benares DB (not Benares-Dev) so doesn't exist
        # workaround to manually test full flow in APIHandler = set ParkingDb to connect to Benares-Dev in server.py (done 10/6 and result positive)
        self.assertEqual(r.status_code, 200, "scheduleAPIHandler doesn't return 200 OK when valid setscheduletoken has been provided")

    def testscheduleAPIHandlerHappyFlowNoargumentprovided(self):
        """
        Try to call /schedule endpoint with valid unitname and verify if API yields correct data
        """
        req_uri = "%s:%d/schedule" % (SERVER_URL, SERVER_PORT)
        cookie = {'token': token.createUUIDToken("2577527d-f2b7-4469-91d2-f91663906571")}
        r = requests.get(req_uri, cookies=cookie)
        # TODO: temp test that just checks if no error is thrown but the given user is not found given that the APIHandler looks in the Benares DB (not Benares-Dev) so doesn't exist
        # workaround to manually test full flow in APIHandler = set ParkingDb to connect to Benares-Dev in server.py (done 10/6 and result positive)
        self.assertEqual(r.status_code, 200, "scheduleAPIHandler doesn't return 200 OK when no argument has been provided")

class awshealthTestCases(unittest.TestCase):

    def testawshealthHandlerHappyFlowUnitnameprovided(self):
        """
        Try to call AWS health API endpoint and get 200 OK
        """
        req_uri = "%s:%d/health" % (SERVER_URL, SERVER_PORT)
        r = requests.get(req_uri)
        self.assertEqual(r.status_code, 200, "awshealthHandler doesn't return 200 OK for health check")

class tosPageTestCases(unittest.TestCase):

    def testLoadTosDoc(self):
        """
        Test whether Tos Doc can be loaded
        """
        parags = readdocument.readdocument().readParagraph(TOS_CONTENT)
        self.assertTrue(parags, "cannot load Tos document from content folder")

class scheduleTestCases(unittest.TestCase):

    def __init__(self):
        print("init scheduleTestCases - TEMP")

    # TODO: re-write after changes to DB
    # def testGetAvailableUnitsNormalCases(self):
    #     # Test normal cases for finding getAvailableUnits
    #
    #     # generate random set of start,end datetime-objects on Jan, 9
    #     lst = []
    #
    #     # test ranges
    #     s1=1
    #     s2=24
    #     e1=2
    #     e2=24
    #
    #     # hard-coded schedule values in test_schedule.json
    #     scheduleStart = 7
    #     scheduleEnd = 21
    #     # Rekenkundige rij van getallen 1, 2, 3, ..., 8 (combinaties van start-end met start<end); https://nl.wikipedia.org/wiki/Rekenkundige_rij
    #     nbOfMatches = 0.5 * (scheduleEnd - scheduleStart) * (1 + scheduleEnd - scheduleStart)
    #
    #     errorCounter = 0
    #     testCounter = 0
    #
    #     keys = ['startTime', 'endTime']
    #     for start in range(s1, s2):
    #         for end in range(e1, e2):
    #             if start < end:
    #                 entry = [datetime(2016, 2, 26, start, 0, 0, tzinfo=pytz.utc), datetime(2016, 2, 26, end, 0, 0, tzinfo=pytz.utc)]
    #                 lst.append(dict(zip(keys, entry)))
    #                 if (start < scheduleStart) | (end > scheduleEnd):
    #                     errorCounter += 1
    #             testCounter += 1
    #
    #     # init result to same length as list of desiredTimeSlots
    #     result = range(len(lst))
    #     # test GetAvailableParkingUnitsNormalCases(self)
    #     matchCounter = 0
    #     for i in range(len(lst)):
    #         # result[i] = server.sMechelen.getAvailableUnits(lst[i])
    #         result[i] = server.sMechelen.findAvailableParkingUnit(destination, lst[i], userID)
    #         if result[i]:
    #             matchCounter += 1
    #         # print(lst[i])
    #
    #     print("\nNormal cases:\nnb of slots tested is %d \nnb of errors is %d \nnb of matches is %d \nmathematical nb of matches is %d." % (len(lst), errorCounter, matchCounter, nbOfMatches))
    #
    #     self.assertEqual(matchCounter, len(lst) - errorCounter, "Each __test__ is not an error or match")
    #     self.assertEqual(matchCounter, nbOfMatches, "Nb of matches doesn't equal mathematical nb")
    #
    # def testGetAvailableUnitsExceptionCaseListProvided(self):
    #     # Test exception case 'timeslot list provided --not dictionary' for finding getAvailableUnits
    #
    #     print("\nException cases:")
    #     slot = [datetime(2016, 2, 26, 10, 0, 0, tzinfo=pytz.utc), datetime(2016, 2, 26, 9, 0, 0, tzinfo=pytz.utc)]
    #     # result = server.sMechelen.getAvailableUnits(slot)
    #     result = server.sMechelen.findAvailableParkingUnit(destination, slot, userID)
    #     self.assertEqual(result, None, "timeslot as list doesn't result in None and TypeError")
    #     # print("timeslot provided as list: ", result)
    #
    # def testGetAvailableUnitsExceptionCaseWrongDateType(self):
    #     # Test exception case 'wrong date type' for finding getAvailableUnits
    #     # Check for TypeError (str provided instead of Datetime) and correct to make sure the method continues
    #
    #     slot = {'startTime':"2016-01-09T09:00:00.000Z", 'endTime':"2016-01-09T10:00:00.000Z"}
    #     # result = server.sMechelen.getAvailableUnits(slot)
    #     result = server.sMechelen.findAvailableParkingUnit(destination, slot, userID)
    #     self.assertEqual(result[0], unicode('Mech1'), "Date as UTC string isn't corrected and result returned")
    #     # print("date as string: ", result)
    #
    # def testGetAvailableUnitsExceptionCaseWrongKeys(self):
    #     # Test exception case 'timeslot list provided --not dictionary' for finding getAvailableUnits
    #
    #     slot = {'start': datetime(2016, 2, 26, 10, 0, 0, tzinfo=pytz.utc), 'end':datetime(2016, 2, 26, 9, 0, 0, tzinfo=pytz.utc)}
    #     # result = server.sMechelen.getAvailableUnits(slot)
    #     result = server.sMechelen.findAvailableParkingUnit(destination, slot, userID)
    #     self.assertEqual(result, None, "timeslot with wrong keys doesn't result in None and KeyError")
    #     # print("wrong keys: ", result)
    #
    # def testGetAvailableUnitsExceptionCaseStartBiggerThenEnd(self):
    #     # Test exception case 'start > end' for finding getAvailableUnits
    #
    #     slot = {'startTime': datetime(2016, 2, 26, 10, 0, 0, tzinfo=pytz.utc), 'endTime':datetime(2016, 2, 26, 9, 0, 0, tzinfo=pytz.utc)}
    #     # result = server.sMechelen.getAvailableUnits(slot)
    #     result = server.sMechelen.findAvailableParkingUnit(destination, slot, userID)
    #     self.assertEqual(result, None, "timeslot with start > end doesn't result in None and ValueError")
    #     # print("start > end: ", result)
    #
    # def testGetAvailableUnitsExceptionCaseOnlyOneDateProvidedAsArgument(self):
    #     # Test testGetAvailableUnitsExceptionCaseOnlyOneDateProvidedAsArgument(self):
    #
    #     slot = datetime(2016, 2, 26, 10, 0, 0, tzinfo=pytz.utc)
    #     # result = server.sMechelen.getAvailableUnits(slot)
    #     result = server.sMechelen.findAvailableParkingUnit(destination, slot, userID)
    #     self.assertEqual(result, None, "timeslot with only one datetime argument doesn't result in None and TypeError")
    #     # print("Only one date object provided: ", result)

if __name__ == '__main__':
    unittest.main()