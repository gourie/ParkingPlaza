__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime
from decimal import Decimal
import sys, unittest
import db_logic
import pytz
import sys
import unittest
#sys.path.append('~/pycharm/parking-plaza')
import utilities

util = utilities.utilities()
parkingDb = db_logic.db_logic("Benares-dev", "localhost", "5432", "ParkingPlaza", "BENARES")
parkingDb.ConnectToDb()

class convert_timedeltaTestCases(unittest.TestCase):

    def testDaysOfDifference(self):
        # Test normal case with day of difference

        slot = {'startTime': datetime(2016, 2, 25, 10, 0, 0, tzinfo=pytz.utc), 'endTime':datetime(2016, 2, 26, 10, 0, 0, tzinfo=pytz.utc)}
        result = util.convert_timedelta(slot['endTime'] - slot['startTime'])
        self.assertEqual(result['days'], 1, "difference in days is not 1")
        self.assertEqual(result['hours'], 24, "difference in hours is not 24")
        self.assertEqual(result['minutes'], 0, "difference in minutes is not 0")
        self.assertEqual(result['seconds'], 0, "difference in seconds is not 0")

    def testHoursOfDifference(self):
        # Test normal case with hours of difference

        slot = {'startTime': datetime(2016, 2, 25, 10, 0, 0, tzinfo=pytz.utc), 'endTime':datetime(2016, 2, 25, 13, 0, 0, tzinfo=pytz.utc)}
        result = util.convert_timedelta(slot['endTime'] - slot['startTime'])
        self.assertEqual(result['days'], 0, "difference in days is not 0")
        self.assertEqual(result['hours'], 3, "difference in hours is not 3")
        self.assertEqual(result['minutes'], 0, "difference in minutes is not 0")
        self.assertEqual(result['seconds'], 0, "difference in seconds is not 0")

    def testHoursMinutesOfDifference(self):
        # Test normal case with hours & minutes of difference

        slot = {'startTime': datetime(2016, 2, 25, 10, 30, 0, tzinfo=pytz.utc), 'endTime':datetime(2016, 2, 25, 13, 0, 0, tzinfo=pytz.utc)}
        result = util.convert_timedelta(slot['endTime'] - slot['startTime'])
        self.assertEqual(result['days'], 0, "difference in days is not 0")
        self.assertEqual(result['hours'], 2, "difference in hours is not 2")
        self.assertEqual(result['minutes'], 30, "difference in minutes is not 30")
        self.assertEqual(result['seconds'], 0, "difference in seconds is not 0")

    def testDaysHoursMinutesSecondsOfDifference(self):
        # Test normal case with day, hours, minutes and seconds of difference

        slot = {'startTime': datetime(2016, 2, 24, 10, 30, 0, tzinfo=pytz.utc), 'endTime':datetime(2016, 2, 25, 13, 0, 20, tzinfo=pytz.utc)}
        result = util.convert_timedelta(slot['endTime'] - slot['startTime'])
        self.assertEqual(result['days'], 1, "difference in days is not 1")
        self.assertEqual(result['hours'], 26, "difference in hours is not 26")
        self.assertEqual(result['minutes'], 30, "difference in minutes is not 30")
        self.assertEqual(result['seconds'], 20, "difference in seconds is not 20")


    def testprepListOfTuplesAccountInfoUser(self):
        input = parkingDb.QueryUserByUserUUID("5a2867c0-8f8a-46bd-b09d-e9e28766a317")
        result = util.prepListOfTuplesAccountInfoUser(input)
        self.assertFalse('userid' in result.keys(), "UserID is not returned to UI")
        self.assertEqual(result['fullname'], "test user6", "Fullname is not test user6")
        self.assertEqual(result['email'], "test6@parking-plaza.com", 'Email is not test6@parking-plaza.com')
        self.assertFalse('toscheckdone' in result.keys(), "TosCheckDone is not returned to UI")

    def testprepListOfTuplesAccountInfoOwner(self):
        #input = (25, 'Jeroen Machiels', 'jeroenmachiels@gmail.com', {u'kind': u'plus#person', u'verified': False, u'name': {u'givenName': u'Jeroen', u'familyName': u'Machiels'}, u'language': u'en_GB', u'isPlusUser': True, u'url': u'https://plus.google.com/104944001666965103847', u'gender': u'male', u'image': {u'url': u'https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg?sz=50', u'isDefault': True}, u'toscheckdone': u'2016-05-25T21:46:15.770293', u'emails': [{u'type': u'account', u'value': u'jeroenmachiels@gmail.com'}], u'token': u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYmI3NzY1Mi1jMzllLTQ4ZTAtOWZmZC0wMjViOTk1ZjU0OGMiLCJleHAiOjE0NjUyMTg5Mzl9.78tCPrEIptxn2GOtIBHXmR-dZ7GO_HiFEY27PN3NUGI', u'etag': u'"9RfJHQrviqM_fwiLNk11QGzyCj0/e1oxCY22zyFFZ4QkcEcYqr3la_I"', u'urls': [{u'type': u'otherProfile', u'value': u'http://picasaweb.google.com/jeroenmachiels', u'label': u'Picasa Web Albums'}], u'displayName': u'Jeroen Machiels', u'circledByCount': 29, u'id': u'104944001666965103847', u'objectType': u'person'}, 'abb77652-c39e-48e0-9ffd-025b995f548c', 25, 'BE9876567890', {u'ownermobile': u'+32478222391', u'toscheckdone': u'2016-05-29T21:30:01.354055'}, 12)
        usr = parkingDb.QueryOwnerandUserInfo("test6@parking-plaza.com")
        result = util.prepListOfTuplesAccountInfoOwner(usr)
        self.assertFalse('userid' in result.keys(), "UserID is not returned to UI")
        self.assertEqual(result['fullname'], "test user6", "Fullname is not test user6")
        self.assertEqual(result['email'], "test6@parking-plaza.com", 'Email is not test6@parking-plaza.com')
        self.assertFalse('toscheckdone' in result.keys(), "TosCheckDone is not returned to UI")
        self.assertFalse('ownermobile' in result.keys(), "ownermobile is not returned to UI")
        self.assertFalse('bankaccount' in result.keys(), "bankaccount is not returned to UI")

    def testprepListOfTuplesForMyParkings(self):
        """
        Test whether schedules list gets well prepared for /schedules API to sent to client without providing EventDescription argument
        """
        userid = parkingDb.QueryUserIDByUUID("5a2867c0-8f8a-46bd-b09d-e9e28766a317")
        self.assertEqual(userid, 6, "testprepListOfTuplesForMyParkings doesn't find userID equal to 6")
        parkings = parkingDb.QueryUnitsForgivenuserid(userid)
        self.assertIsNotNone(parkings, "testprepListOfTuplesForMyParkings: QueryUnitsForgivenuserid method finds parkings value different from None")
        result = util.prepListOfTuplesForMyParkings(parkings)
        self.assertEqual(result[0]['UnitFriendlyName'],"L1", "UnitFriendlyName not equal to L1")
        self.assertEqual(result[0]['CityName'], "Lennik", "CityName not equal to Lennik")
        self.assertEqual(result[0]['FullAddress'], "Negenbunderstraat 10, Lennik, Belgium", "FullAddress not equal to Negenbunderstraat 10, Lennik, Belgium")
        self.assertEqual(result[0]['ParkingType'], "parking lot", "ParkingType not equal to parking lot")
        self.assertEqual(result[0]['Latitude'], 50.805764, "Latitude not equal to 50.805764")
        self.assertEqual(result[0]['Longitude'], 4.1373328, "Longitude not equal to 4.1373328")

class prepDataforAPI(unittest.TestCase):

    def testPrepSchedulesListForParkingListAppNoEventDescriptionProvidedHappyFlowKeysPresentAndTimeConverted(self):
        """
        Test whether schedules list gets well prepared for /schedules API to sent to client without providing EventDescription argument
        """
        res = util.prepSchedulesListForParkingListApp(parkingDb.QueryFutureSchedulesbyUnitname('A1', unittest=True))
        self.assertEqual('schedulestatus' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain status key")
        self.assertEqual('eventstart' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain eventstart key")
        self.assertEqual('eventdescription' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain eventdescription key")
        self.assertEqual('changed' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain changed key")
        self.assertEqual(res[0]['eventstart'], "2016-06-10T19:00:00+02:00", "QuerySchedulesbyUnitId doesn't return right eventstart date for unitid 1")
        self.assertEqual(res[0]['changed'], "false", "QuerySchedulesbyUnitId doesn't return changed = false when no eventdescription is provided")

    def testPrepSchedulesListForParkingListAppEventDescriptionProvidedHappyFlowKeysPresentAndTimeConverted(self):
        """
        Test whether schedules list gets well prepared for /schedules API to sent to client when EventDescription argument is provided
        """
        res = util.prepSchedulesListForParkingListApp(parkingDb.QueryFutureSchedulesbyUnitname('A1', unittest=True), "R.S.C. Anderlecht - Test3")
        self.assertEqual('schedulestatus' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain status key")
        self.assertEqual('eventstart' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain eventstart key")
        self.assertEqual('eventdescription' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain eventdescription key")
        self.assertEqual('changed' in res[0].keys(), True, "QuerySchedulesbyUnitId doesn't contain changed key")
        self.assertEqual(res[0]['eventstart'], "2016-06-10T19:00:00+02:00", "QuerySchedulesbyUnitId doesn't return right eventstart date for unitid 1")
        self.assertEqual(res[0]['changed'], "true", "QuerySchedulesbyUnitId doesn't return changed = false when no eventdescription is provided")

    def testcheckIfValidDatetime(self):
        """
        Test whether a Python Datetime object yields True
        """
        self.assertTrue(util.checkIfValidDatetime(datetime.now()), "checkIfValidDatetime doesn't return True for Python datetime object")

if __name__ == '__main__':
    unittest.main()
