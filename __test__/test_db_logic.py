__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime, timedelta
import db_logic
from decimal import *
import json
from pytz import timezone
import sys
import unittest
sys.path.append('~/pycharm/parking-plaza')
sys.path.append('..')

with open('./config.json', 'r') as file:
    conf = json.loads(file.read())
TIMEZONE = str(conf['timezone'])

parkingDb = db_logic.db_logic("Benares-dev", "localhost", "5432", "ParkingPlaza", "BENARES")
parkingDb.ConnectToDb()

class UserTests(unittest.TestCase):

    def testCheckIfUserAlreadyExistsNormalCase1(self):
        user = parkingDb.CheckIfUserAlreadyExists('test1@parking-plaza.com')
        self.assertEqual(user, True, "CheckIfUserAlreadyExists doesn't find correct username with single quotes")

    def testCheckIfUserAlreadyExistsNormalCase2(self):
        user = parkingDb.CheckIfUserAlreadyExists("test1@parking-plaza.com")
        self.assertEqual(user, True, "CheckIfUserAlreadyExists doesn't find correct username with double quotes")

    def testQueryUserByUserUUIDNormalCase1(self):
        user = parkingDb.QueryUserByUserUUID('2577527d-f2b7-4469-91d2-f91663906571')
        self.assertEqual(user[1], 'test user1', "QueryUserByUserUUID doesn't find correct username with single quotes")
        self.assertEqual(user[2], 'test1@parking-plaza.com', "QueryUserByUserUUID doesn't find correct email address with single quotes")

    def testQueryUserByUserUUIDNormalCase2(self):
        user = parkingDb.QueryUserByUserUUID("2577527d-f2b7-4469-91d2-f91663906571")
        self.assertEqual(user[1], 'test user1', "QueryUserByUserUUID doesn't find correct username with double quotes")
        self.assertEqual(user[2], 'test1@parking-plaza.com', "QueryUserByUserUUID doesn't find correct email address with double quotes")

    def testQueryOwnerandUserInfo(self):
        userJeroen = "test6@parking-plaza.com"
        user = parkingDb.QueryOwnerandUserInfo(userJeroen)

        # self.assertNotEqual(user, False, "QueryUserByUserUUID returns false with double quotes")
        self.assertEqual(user[1], "test user6", "Fullname is not equal to test user6")
        self.assertEqual(user[2], "test6@parking-plaza.com", "Email address is not test6@parking-plaza.com")
        self.assertEqual(user[7]['ownermobile'],"+32478222391", "Ownermobile is not +32478222391")

    def testQueryUserIDbyUserUUIDHappyFlow(self):
        """
        Test whether the correct useris is returned for a given useruuid 2577527d-f2b7-4469-91d2-f91663906574
        """
        res = parkingDb.QueryUserIDbyUserUUID('2577527d-f2b7-4469-91d2-f91663906574')
        self.assertEqual(res, 4, "QueryUserIDbyUserUUID doesn't return the correct userid for given useruuid 2577527d-f2b7-4469-91d2-f91663906574")

    def testQueryUserIDbyUserUUIDArgumentnotindb(self):
        """
        Test whether the correct useris is returned for a useruuid that doesn't exist in our DB (2577527d-f2b7-4469-91d2-f91663906500)
        """
        res = parkingDb.QueryUserIDbyUserUUID('2577527d-f2b7-4469-91d2-f91663906500')
        self.assertEqual(res, None, "QueryUserIDbyUserUUID doesn't return None for given useruuid 2577527d-f2b7-4469-91d2-f91663906500 that doens't exist in our db")

    def testQueryUserIDbyUserUUIDWrongargumenttype(self):
        """
        Test whether the correct useris is returned for false argument (not uuid type)
        """
        res = parkingDb.QueryUserIDbyUserUUID('false argument')
        self.assertEqual(res, None, "QueryUserIDbyUserUUID doesn't return None for false argument 'false argument'")

    def testAddUserHappyFlow(self):
        """
        Test whether a user is added, queried and deleted properly to the USERS table
        """
        parkingDb.AddUser(email="test-user@pp.com", fullname="test AddUser", useruuid="2577527d-f2b7-4469-91d2-f91663906590", properties=dict(id="1234"))
        result = parkingDb.QueryUser("test-user@pp.com")
        # don't check user id (first item of array returned)
        try:
            self.assertEqual(result[1], "test AddUser", "AddUser & QueryUser don't deliver correct fullname")
            self.assertEqual(result[2], "test-user@pp.com", "AddUser & QueryUser don't deliver correct email address")
            self.assertTrue('id' in result[3].keys(), "AddUser & QueryUser don't deliver correct key 'id' in properties")
            self.assertEqual(result[3]['id'], "1234", "AddUser & QueryUser don't deliver correct properties id value")
            self.assertEqual(result[4], "2577527d-f2b7-4469-91d2-f91663906590", "AddUser & QueryUser don't deliver correct uuid")
            # clean-up
            res = parkingDb.DeleteUser(result[0])
            self.assertTrue(res, "User record for userid %s has been deleted" % result[0])
        except AssertionError, e:
            # clean-up
            res = parkingDb.DeleteUser(result[0])
            self.assertTrue(res, "User record for userid %s has been deleted" % result[0])


    def testAddUserHappyFlowCannotAddUserWithSameEmailTwice(self):
        """
        Test that a user with given email address cannot be added twice
        """
        parkingDb.AddUser(email="test-user@pp.com", fullname="test AddUser", useruuid="2577527d-f2b7-4469-91d2-f91663906590", properties=dict(id="1234"))
        result = parkingDb.QueryUser("test-user@pp.com")
        res1 = parkingDb.AddUser(email="test-user@pp.com", fullname="test AddUser", useruuid="2577527d-f2b7-4469-91d2-f91663906590", properties=dict(id="1234"))
        try:
            self.assertEqual(res1, "user already exists", "AddUser can add user with same email twice!")
            # clean-up
            res2 = parkingDb.DeleteUser(result[0])
            self.assertTrue(res2, "User record for userid %s has not been deleted" % result[0])
        except AssertionError, e:
            # clean-up
            res2 = parkingDb.DeleteUser(result[0])
            self.assertTrue(res2, "User record for userid %s has been deleted" % result[0])

    def testUpdateUserPropsBasedOnUserUUIDHappyFlow(self):
        """
        Test whether the user properties are correctly updated for the given UUID
        """
        parkingDb.AddUser(email="test-user@pp.com", fullname="test AddUser", useruuid="2577527d-f2b7-4469-91d2-f91663906590", properties=dict(id="1234"))
        user = parkingDb.QueryUser("test-user@pp.com")
        user[3]['test-tag'] = "new property value set for key test-tag"
        res = parkingDb.UpdateUserPropsBasedOnUserUUID("2577527d-f2b7-4469-91d2-f91663906590", user[3])
        user2 = parkingDb.QueryUser("test-user@pp.com")
        try:
            self.assertEqual(res, True, "UpdateUserPropsBasedOnUserUUID doesn't update the user")
            self.assertTrue('test-tag' in user2[3].keys(), "UpdateUserPropsBasedOnUserUUID doesn't update the user properties with correct arguments")
            self.assertEqual(user2[3]['test-tag'], "new property value set for key test-tag", "UpdateUserPropsBasedOnUserUUID doesn't deliver user properties with correct arguments")
            parkingDb.DeleteUser(user[0])
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteUser(user[0])

    def testUpdateUserPropsBasedOnUserUUIDWrongUUIDargumenttype(self):
        """
        Test whether wrong UUID argument type doesn't kill application and no UPDATE is done (false returned)
        """
        res = parkingDb.UpdateUserPropsBasedOnUserUUID('false argument', dict(test=1))
        self.assertFalse(res, "UpdateUserPropsBasedOnUserUUID doesn't return False for wrong uuid argument 'false argument'")

    def testUpdateUserPropsBasedOnUserUUIDWrongPropertiesargumenttype(self):
        """
        Test whether wrong Properties argument type (must be dict) doesn't create dirty data in table (no update done --> false returned)
        """
        res = parkingDb.UpdateUserPropsBasedOnUserUUID("2577527d-f2b7-4469-91d2-f91663906590", "false argument")
        self.assertFalse(res, "UpdateUserPropsBasedOnUserUUID doesn't return False for wrong properties argument 'false argument'")

    def testQueryUserPropertiesForEmailconfirmationWithGivenuseridandtokenHappyFlow(self):
        """
        Test whether the correct user properties field for key email-confirmation for given userid 7 and associated confirmationtoken are returned
        """
        conftoken= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbGFkZHJlc3MiOiJwcGxhemF0ZXN0MkBnbWFpbC5jb20iLCJleHAiOjE0NjcyNzU5OTl9.6dBBG4I7L2NDF6Ut71EVTTT3g4gwfOqmYYf4rylhjCc"
        self.assertEqual(parkingDb.QueryUserPropertiesForEmailconfirmationWithGivenuseridandtoken(7, conftoken), "pending", "QueryUserPropertiesForEmailconfirmationWithGivenuseridandtoken doesn't return the correct properties email-confirmation value for given userid 7 and confirmationtoken")


class PoiTests(unittest.TestCase):

    def testQueryPoiFriendlynameByUnitidNormalCase(self):
        result = parkingDb.QueryPoiFriendlynameByUnitid(1)
        poifname = parkingDb.QueryPoiFriendlyname(3)
        self.assertEqual(result, poifname, "QueryPoiFriendlynameByUnitid doesn't find correct poifriendlyname if valid unit id has been provided")

    def testQueryPoiFriendlynameByUnitidExceptionCase(self):
        print("\nException case QueryPoiFriendlynameByUnitid - invalid unit id argument provided")
        result = parkingDb.QueryPoiFriendlynameByUnitid(567)
        self.assertEqual(result, None, "QueryPoiFriendlynameByUnitid doesn't return None if invalid unit id has been provided")

    def testQueryPoiPricepertimeunitHappyFlow(self):
        """
        Test whether right pricepertimeunit is returned for valid poiid
        """
        self.assertEqual(parkingDb.QueryPoiPricepertimeunit(1), 2, "QueryPoiPricepertimeunit doesn't return the correct pricepertimeunit for poiid 1")

    def testQueryPoiPricepertimeunitFalseargument(self):
        """
        Test whether right pricepertimeunit is returned for invalid poiid
        """
        self.assertEqual(parkingDb.QueryPoiPricepertimeunit(-1), None, "QueryPoiPricepertimeunit doesn't return None for false argument")

    def testQueryPoiCenterByUnitidHappyFlow(self):
        """
        Test whether the correct poicenter is returned for unit id 1
        """
        result = parkingDb.QueryPoiCenterByUnitid(1)
        self.assertEqual(result['lat'], 50.834295, "QueryPoiCenterByUnitid doesn't return correct lat if unit id 1 has been provided")
        self.assertEqual(result['lon'], 4.298057, "QueryPoiCenterByUnitid doesn't return correct lon if unit id 1 has been provided")

    def testQueryPoiCenterByUnitidFalseargument(self):
        """
        Test whether the correct poicenter is returned for unit id -1
        """
        result = parkingDb.QueryPoiCenterByUnitid(-1)
        self.assertEqual(result, None, "QueryPoiCenterByUnitid doesn't return None if false unit id -1 has been provided")

class PaymentTests(unittest.TestCase):

    def testAddPaymentandQueryPaymentDetailsandDeletePaymentForgivenordernrHappyflow(self):
        """
        Test whether a payment is added, queried and deleted properly to the paymentgwstatus table
        """
        parkingDb.AddPayment('2577527d-f2b7-4469-91d2-f91663906571', 12345, "test payment for unit-test", timezone(TIMEZONE).localize(datetime.now()).isoformat(), 20, 16.53, 3.47, 1, '2016-06-10 18:00:00+02', '2016-06-10 22:00:00+02')
        result = parkingDb.QueryPaymentDetails(12345)
        #users.email, paymentgwstatus.ordernr, paymentgwstatus.description, paymentgwstatus.amountinclbtw, paymentgwstatus.amountexclbtw, paymentgwstatus.btwamount "
        self.assertEqual(result[1], 12345, "AddPayment doesn't find correct payment ordernr")
        self.assertEqual(result[2], "test payment for unit-test", "AddPayment doesn't find correct payment description")
        self.assertEqual(result[3], 20, "AddPayment doesn't find correct payment amount iBTW")
        self.assertEqual(result[4], 16.53, "AddPayment doesn't find correct payment amount eBTW")
        self.assertEqual(result[5], 3.47, "AddPayment doesn't find correct payment BTW amount")
        # clean-up
        res = parkingDb.DeletePaymentForgivenordernr(12345)
        self.assertEqual(res, "Payment record for ordernr 12345 has been deleted")

    def testQueryPaymentHappyflow(self):
        """
        Test whether QueryPayment returns all entries for first record
        """
        result = parkingDb.QueryPayment()
        self.assertEqual(result[0][1], 123, "QueryPaymentDetails doesn't find correct payment ordernr")
        self.assertEqual(result[0][2], "test payment for unit-test", "QueryPaymentDetails doesn't find correct payment description")
        self.assertEqual(result[0][6], 20, "QueryPaymentDetails doesn't find correct payment amount iBTW")
        self.assertEqual(result[0][10], '2577527d-f2b7-4469-91d2-f91663906571', "QueryPaymentDetails doesn't find correct uuid")
        self.assertEqual(result[0][11], 1, "QueryPaymentDetails doesn't find correct unit id")
        self.assertEqual(result[0][12].isoformat(), '2016-06-10T18:00:00+02:00', "QueryPaymentDetails doesn't find correct starttime")
        self.assertEqual(result[0][13].isoformat(), '2016-06-10T22:00:00+02:00', "QueryPaymentDetails doesn't find correct endtime")
        self.assertEqual(result[0][14], 16.53, "QueryPaymentDetails doesn't find correct amount eBTW")
        self.assertEqual(result[0][15], 3.47, "QueryPaymentDetails doesn't find correct BTW amount")

    def testQueryScheduleByPaymentOrdernrNormalCase(self):
        """
        Take first element from paymenttable and compare result to function call
        """
        paymentTable = parkingDb.QueryPayment()
        result = parkingDb.QueryScheduleByPaymentOrdernr(paymentTable[0][1])
        # [useruuid, starttime, endtime, description, unitid]
        self.assertEqual(result[0], paymentTable[0][10], "QueryScheduleByPaymentOrdernr doesn't find uuid if valid payment ordernr has been provided")
        self.assertEqual(result[1], paymentTable[0][12], "QueryScheduleByPaymentOrdernr doesn't find starttime if valid payment ordernr has been provided")
        self.assertEqual(result[2], paymentTable[0][13], "QueryScheduleByPaymentOrdernr doesn't find endtime if valid payment ordernr has been provided")
        self.assertEqual(result[3], paymentTable[0][2], "QueryScheduleByPaymentOrdernr doesn't find description if valid payment ordernr has been provided")
        self.assertEqual(result[4], paymentTable[0][11], "QueryScheduleByPaymentOrdernr doesn't find unitid if valid payment ordernr has been provided")


class PoieventsTests(unittest.TestCase):

    def testQueryAvailablePoiEventsWithinGivenAmountofdaysCorrectNbofItemsFoundHappyFlow(self):
        """
        Query and return the poievents that will occur within the given amount of days (from tonight)
        """
        res = parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(timezone(TIMEZONE).localize(datetime(2016, 6, 7, 20, 0, 0)), 5, unittest=True)
        self.assertEqual(len(res), 6, "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct number of items")

    def testQueryAvailablePoiEventsWithinGivenAmountofdaysCorrectFirstItemFoundHappyFlow(self):
        """
        Query and return the poievents that will occur within the given amount of days (from tonight)
        """
        res = parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(timezone(TIMEZONE).localize(datetime(2016, 6, 7, 20, 0, 0)), 5, unittest=True)
        # [poieventid, eventdescription, eventdate, unitid, unitaddress, ownername, ownermail]
        self.assertEqual(res[0]['poieventid'], 6, "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct poieventid")
        self.assertEqual(res[0]['eventdescription'], 'R.S.C. Anderlecht - Test3', "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct poieventdescr")
        self.assertEqual(res[0]['eventdate'].isoformat(), '2016-06-10T19:00:00+02:00', "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct event date")
        self.assertEqual(res[0]['unitid'], 1, "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct unitid")
        self.assertEqual(res[0]['unitaddress'], 'Teststraatt 1, Anderlecht, Belgium', "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct unit address")
        self.assertEqual(res[0]['ownername'], 'test user1', "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct ownername")
        self.assertEqual(res[0]['owneremail'], 'test1@parking-plaza.com', "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't find correct the correct owneremail")

    def testQueryAvailablePoiEventsWithinGivenAmountofdaysPaststartdate(self):
        """
        Test whether [] is returned when passing startdate in the past ('relative to DB test records')
        """
        res = parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(timezone(TIMEZONE).localize(datetime(2015, 6, 7, 20, 0, 0)), 5, unittest=True)
        self.assertEqual(res, [], "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't return [] when passing startdate in the past")

    def testQueryAvailablePoiEventsWithinGivenAmountofdaysNegativeAmountofdays(self):
        """
        Test whether [] is returned when passing negative amount of days
        """
        res = parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(timezone(TIMEZONE).localize(datetime(2016, 6, 7, 20, 0, 0)), -2, unittest=True)
        self.assertEqual(res, [], "QueryAvailablePoiEventsWithinGivenAmountofdays doesn't return [] when passing negative amount of days")

    def testCheckIfUnitHasScheduleForGivenPoieventidHappyFlowMatch(self):
        """
        Check if positive match for query
        """
        result = parkingDb.CheckIfUnitHasScheduleForGivenPoieventid(1, 6)
        self.assertEqual(result, True, "CheckIfUnitHasScheduleForGivenPoieventid doesn't return positive check")

    def testCheckIfUnitHasScheduleForGivenPoieventidHappyFlowDoesnotMatch(self):
        """
        Check if negative match for query
        """
        result = parkingDb.CheckIfUnitHasScheduleForGivenPoieventid(1, 4)
        self.assertEqual(result, False, "CheckIfUnitHasScheduleForGivenPoieventid doesn't return positive check")

    def testQueryPoieventHappyFlow(self):
        """
        Test if poievent is returned with all records field for existing poieventid
        """
        result = parkingDb.QueryPoievent(1)
        # dict ('poieventid', 'eventdescription', 'eventstart', 'properties', 'poiid')
        self.assertEqual(result['poieventid'], 1, "QueryPoievent doesn't find correct the correct poieventid")
        self.assertEqual(result['eventdescription'], "R.S.C. Anderlecht - K.A.A Gent", "QueryPoievent doesn't find correct the correct eventdescription")
        self.assertEqual(result['eventstart'].isoformat(), "2016-05-01T14:30:00+02:00", "QueryPoievent doesn't find correct the correct eventstart")
        self.assertEqual(result['properties'], None, "QueryPoievent doesn't find correct the correct properties")
        self.assertEqual(result['poiid'], 3, "QueryPoievent doesn't find correct the correct poiid")

    def testQueryPoilatlonForgivenpoieeventdescriptionHappyFlow(self):
        """
        Test whether the correct poi center (lat,lon) are returned for given eventdescription
        """
        res = parkingDb.QueryPoilatlonForgivenpoieeventdescription('R.S.C. Anderlecht - Test3')
        self.assertEqual(res['lat'], 50.834295, "QueryPoilatlonForgivenpoieeventdescription doesn't find correct the correct latlon for eventdescription R.S.C. Anderlecht - Test3")
        self.assertEqual(res['lon'], 4.298057, "QueryPoilatlonForgivenpoieeventdescription doesn't find correct the correct latlon for eventdescription R.S.C. Anderlecht - Test3")

    def testQueryPoilatlonForgivenpoieeventdescriptionFalseargument(self):
        """
        Test whether the correct poi center (lat,lon) are returned for given eventdescription
        """
        res = parkingDb.QueryPoilatlonForgivenpoieeventdescription('false argument')
        self.assertEqual(res, None, "QueryPoilatlonForgivenpoieeventdescription doesn't return None for eventdescription false entry")

    def testQueryPoieventIDByEventdescriptionHappyFlow(self):
        """
        Test whether the correct poieventid is returned for the given eventdescription
        """
        res = parkingDb.QueryPoieventIDByEventdescription('R.S.C. Anderlecht - Test2')
        self.assertEqual(res, 5, "QueryPoieventIDByEventdescription doesn't find return the correct poieventid for eventdescription R.S.C. Anderlecht - Test2")

    def testQueryPoieventIDByEventdescriptionFalseargument(self):
        """
        Test whether None is returned for a false eventdescription
        """
        res = parkingDb.QueryPoieventIDByEventdescription('false argument')
        self.assertEqual(res, None, "QueryPoieventIDByEventdescription doesn't None for a false eventdescription")


class UnitTests(unittest.TestCase):

    def testQueryUnitHappyFlow(self):
        """
        Test if unit is returned with all records field for existing unit id
        """
        result = parkingDb.QueryUnit(3)
        # columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        self.assertEqual(result['unitname'], 'A3', "QueryUnit doesn't find correct the correct unitname")
        self.assertEqual(result['latlon']['lat'], 50.83, "QueryUnit doesn't find correct the correct latlon")
        self.assertEqual(result['latlon']['lon'], 4.275, "QueryUnit doesn't find correct the correct latlon")
        self.assertEqual(result['userid'], 3, "QueryUnit doesn't find correct the correct userid")
        self.assertEqual(result['typeid'], 1, "QueryUnit doesn't find correct the correct typeid")
        self.assertEqual(result['poiid'], 3, "QueryUnit doesn't find correct the correct poiid")
        self.assertEqual(result['ownerid'], 3, "QueryUnit doesn't find correct the correct ownerid")
        self.assertEqual('fulladdress' in result['properties'].keys(), True, "QueryUnit doesn't find correct the correct properties")
        self.assertEqual(result['unitid'], 3, "QueryUnit doesn't find correct the correct unitid")
        self.assertEqual(result['cityname'], "Anderlecht", "QueryUnit doesn't find correct the correct cityname")

    def testUpdateUnitPropertiesHappyFlow(self):
        """
        Test whether Unit properties as updated with provided props dictionary
        """
        props = {"setschedule": {"poieventid": 10, "timestamp": "3/6"}}
        parkingDb.UpdateUnitProperties(2, props)
        test = parkingDb.QueryUnit(2)
        self.assertTrue('fulladdress' in test['properties'].keys(), "UpdateUnitProperties doesn't leave the existing fulladdress key in the properties field")
        self.assertTrue('setschedule' in test['properties'].keys(), "UpdateUnitProperties doesn't add the new setschedule key to the properties field")
        self.assertTrue('poieventid' in test['properties']['setschedule'].keys(), "UpdateUnitProperties doesn't add the key poieventid in the new setschedule key to the properties field")
        self.assertTrue('timestamp' in test['properties']['setschedule'].keys(), "UpdateUnitProperties doesn't add the key timestamp in the new setschedule key to the properties field")
        self.assertEqual(test['properties']['setschedule']['poieventid'], 10, "UpdateUnitProperties doesn't add the right value for key poieventid in the new setschedule key to the properties field")
        self.assertEqual(test['properties']['setschedule']['timestamp'], "3/6", "UpdateUnitProperties doesn't add the right value for key timestamp in the new setschedule key to the properties field")
        # reset testDB unit properties field for unitid 2
        oldprops = {"fulladdress": "Teststraatt 2, Anderlecht, Belgium"}
        parkingDb.OverwriteUnitProperties(2, oldprops)

    def testQueryUnitPropertiesForSetScheduleWithGivenPoieventidHappyFlow(self):
        """
        Test whether Unit properties contain specific poieventid value in the properties setschedule tag
        """
        self.assertEqual(str(parkingDb.QueryUnitPropertiesForSetScheduleWithGivenPoieventid(1,10)), "26/2", "QueryUnitPropertiesForSetScheduleWithGivenPoieventid doesn't return the correct properties timestamp value for given poieventid and unitid")

    def testQueryUnitByUserIdHappyFlow(self):
        """
        Test whether Unit is returned with all records for existing user id 3
        """
        result = parkingDb.QueryUnitByUserId(3)
        # columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        self.assertEqual(result['unitname'], 'A3', "QueryUnitByUserId doesn't find correct the correct unitname for userid 3")
        self.assertEqual(result['latlon']['lat'], 50.83, "QueryUnitByUserId doesn't find correct the correct latlon for userid 3")
        self.assertEqual(result['latlon']['lon'], 4.275, "QueryUnitByUserId doesn't find correct the correct latlon for userid 3")
        self.assertEqual(result['userid'], 3, "QueryUnitByUserId doesn't find correct the correct userid for userid 3")
        self.assertEqual(result['typeid'], 1, "QueryUnitByUserId doesn't find correct the correct typeid for userid 3")
        self.assertEqual(result['poiid'], 3, "QueryUnitByUserId doesn't find correct the correct poiid for userid 3")
        self.assertEqual(result['ownerid'], 3, "QueryUnitByUserId doesn't find correct the correct ownerid for userid 3")
        self.assertEqual('fulladdress' in result['properties'].keys(), True, "QueryUnitByUserId doesn't find correct the correct properties for userid 3")
        self.assertEqual(result['unitid'], 3, "QueryUnitByUserId doesn't find correct the correct unitid for userid 3")
        self.assertEqual(result['cityname'], "Anderlecht", "QueryUnitByUserId doesn't find correct the correct cityname for userid 3")

    def testQueryUnitByUserIdHappyFlowUserIdNotFound(self):
        """
        Test whether Unit is returned with all records for user id -1 not found in UNIT table
        """
        result = parkingDb.QueryUnitByUserId(-1)
        # columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        self.assertEqual(result, None, "QueryUnitByUserId doesn't return None for userid -1 ")

    def testQueryUnitByUserUUIDHappyFlow(self):
        """
        Test whether Unit is returned with all records for existing user uuid "2577527d-f2b7-4469-91d2-f91663906573"
        """
        result = parkingDb.QueryUnitsByUserUUID("2577527d-f2b7-4469-91d2-f91663906573")[0]
        # columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        self.assertEqual(result['unitname'], 'A3', "QueryUnitsByUserUUID doesn't find correct the correct unitname for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['latlon']['lat'], 50.83, "QueryUnitsByUserUUID doesn't find correct the correct latlon for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['latlon']['lon'], 4.275, "QueryUnitsByUserUUID doesn't find correct the correct latlon for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['userid'], 3, "QueryUnitsByUserUUID doesn't find correct the correct userid for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['typeid'], 1, "QueryUnitsByUserUUID doesn't find correct the correct typeid for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['poiid'], 3, "QueryUnitsByUserUUID doesn't find correct the correct poiid for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['ownerid'], 3, "QueryUnitsByUserUUID doesn't find correct the correct ownerid for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual('fulladdress' in result['properties'].keys(), True, "QueryUnitsByUserUUID doesn't find correct the correct properties for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['unitid'], 3, "QueryUnitsByUserUUID doesn't find correct the correct unitid for user uuid 2577527d-f2b7-4469-91d2-f91663906573")
        self.assertEqual(result['cityname'], "Anderlecht", "QueryUnitsByUserUUID doesn't find correct the correct cityname for user uuid 2577527d-f2b7-4469-91d2-f91663906573")

    def testQueryUnitByUserUUIDHappyFlowUserIdNotFound(self):
        """
        Test whether Unit is returned with all records for user uuid "-1" not found in USERS table
        """
        result = parkingDb.QueryUnitsByUserUUID("2577527d-f2b7-4469-91d2-f91663906593")
        # columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        self.assertEqual(result, None, "QueryUnitsByUserUUID doesn't return None for useruuid -1 ")

    def testQueryUnitsForgivenuseridHappyFlow(self):
        """
        Test whether unit is returned with correct attributes for existing user id
        :return: list [unit.friendlyname, unit.latitudelongitude, type.type, unit.cityname, unit.properties]
        """
        result = parkingDb.QueryUnitsForgivenuserid(5)
        self.assertEqual(len(result), 2, "QueryUnitsForgivenuserid doesn't find two units for user id 5")
        self.assertEqual(result[0][0], "G2", "QueryUnitsForgivenuserid doesn't find correct unitname for first entry")
        self.assertEqual(result[0][1]['lat'], 51.01 , "QueryUnitsForgivenuserid doesn't find correct lat for first entry")
        self.assertEqual(result[0][1]['lon'], 5.54 , "QueryUnitsForgivenuserid doesn't find correct lon for first entry")
        self.assertEqual(result[0][2], "parking lot" , "QueryUnitsForgivenuserid doesn't find correct type parking lot for first entry")
        self.assertEqual(result[0][3], "Genk" , "QueryUnitsForgivenuserid doesn't find correct city name for first entry")
        self.assertEqual('fulladdress' in result[0][4].keys(), True, "QueryUnitsForgivenuserid doesn't find properties to be None  for first entry")

    def testQueryUnitAddressHappyFlow(self):
        """
        Test whether unit address is correcly returned for given unit id
        """
        result = parkingDb.QueryUnitAddress(3)
        self.assertEqual(result, "Teststraatt 3, Anderlecht, Belgium", "QueryUnitAddress doesn't return the correct unit address for unit with id 3")

    def testQueryUnitAddressFalseArgument(self):
        """
        Test whether unit address is correcly returned for false unit id
        """
        result = parkingDb.QueryUnitAddress(-1)
        self.assertEqual(result, None, "QueryUnitAddress doesn't return None for unit with id -1")

class ScheduleTests(unittest.TestCase):

    def testQuerySchedulesbyUnitnameHappyFlow(self):
        """
        Test whether the right schedule is returned for unitid 1 with right fields
        """
        res = parkingDb.QueryFutureSchedulesbyUnitname('A1', unittest=True)
        self.assertEqual(res[0]['eventstart'].isoformat(), "2016-06-10T19:00:00+02:00", "testQuerySchedulesbyUnitnameHappyFlow doesn't return right eventstart for unitid 1")
        self.assertEqual(res[0]['eventdescription'], "R.S.C. Anderlecht - Test3", "testQuerySchedulesbyUnitnameHappyFlow doesn't return right eventdescription for unitid 1")
        self.assertEqual(res[0]['schedulestatus'], "available", "testQuerySchedulesbyUnitnameHappyFlow doesn't return right schedule status for unitid 1")

    def testQuerySchedulesbyUnitnameHappyFlowNoScheduleFound(self):
        """
        Test whether the right schedules are returned with right fields
        """
        res = parkingDb.QueryFutureSchedulesbyUnitname('A3', unittest=True)
        self.assertEqual(res, [], "QuerySchedulesbyUnitname doesn't return an empty result array for unitid 3")

    def testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow(self):
        """
        Test whether right schedule with right fields is returned for eventdescription and user 5
        """
        res = parkingDb.QueryScheduleinstatusprocessingByUserUUIDandEventdescription('2577527d-f2b7-4469-91d2-f91663906575', 'R.S.C. Anderlecht - Test1')
        # scheduleid not tested as this is auto-generated
        self.assertEqual(res['scheduleStart'].isoformat(), '2016-07-08T17:00:00+02:00', "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right schedule starttime for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")
        self.assertEqual(res['scheduleEnd'].isoformat(), '2016-07-08T21:00:00+02:00', "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right schedule endtime for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")
        self.assertEqual(res['status'], 'processing', "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right status processing for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")
        self.assertEqual(res['userID'], 5, "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right userid for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")
        self.assertEqual(res['pricepertimeunit'], 15, "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right pricepertimeunit for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")
        self.assertEqual(res['timeunitid'], 1, "testQueryScheduleinstatusprocessingByUserUUIDandEventdescriptionHappyFlow doesn't return right timeunitid for user 5 and eventdescription 'R.S.C. Anderlecht - Test1'")

    def testQueryAvailableScheduleForGivenEventHappyFlow(self):
        """
        Test whether the right schedule with correct fields is returned for given eventdescription
        """
        res = parkingDb.QueryAvailableScheduleForGivenEvent('R.S.C. Anderlecht - Test3')
        # [scheduleID, unitid, schedulePricePerTimeUnit, currency, unitaddress, unitdistancetopoi]
        # scheduleid not tested as this is auto-generated
        self.assertEqual(res['unitid'], 1, "QueryAvailableScheduleForGivenEvent doesn't return right unitid for eventdescription 'R.S.C. Anderlecht - Test3'")
        self.assertEqual(res['schedulePricePerTimeUnit'], 15, "QueryAvailableScheduleForGivenEvent doesn't return right schedulePricePerTimeUnit for eventdescription 'R.S.C. Anderlecht - Test3'")
        self.assertEqual(res['currency'], 'EUR', "QueryAvailableScheduleForGivenEvent doesn't return right currency for eventdescription 'R.S.C. Anderlecht - Test3'")
        self.assertEqual(res['unitaddress'], "Teststraatt 1, Anderlecht, Belgium", "QueryAvailableScheduleForGivenEvent doesn't return right unitaddress for eventdescription 'R.S.C. Anderlecht - Test3'")
        self.assertEqual(res['unitdistancetopoi'], Decimal('0.078'), "QueryAvailableScheduleForGivenEvent doesn't return right unitdistancetopoi for eventdescription 'R.S.C. Anderlecht - Test3'")

    def testQueryAvailableScheduleForGivenEventFalseEntry(self):
        """
        Test whether None is returned for false eventdescription
        """
        res = parkingDb.QueryAvailableScheduleForGivenEvent('false entry')
        self.assertEqual(res, None, "QueryAvailableScheduleForGivenEvent doesn't return None for eventdescription 'false entry'")

    def testQueryScheduleHappyFlow(self):
        """
        Test whether query returns the schedule details for given existing schedule id
        """
        res = parkingDb.QuerySchedule(1)
        # [unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,userid,properties,scheduleid,poieventid]
        self.assertEqual(res[0], 1, "QuerySchedule doesn't return correct unitid for given scheduleid 1")
        self.assertEqual(res[1], 1, "QuerySchedule doesn't return correct ownerid for given scheduleid 1")
        self.assertEqual(res[2].isoformat(), '2016-06-24T13:30:00+02:00', "QuerySchedule doesn't return correct starttime for given scheduleid 1")
        self.assertEqual(res[3].isoformat(), '2016-06-24T17:30:00+02:00', "QuerySchedule doesn't return correct endtime for given scheduleid 1")
        self.assertEqual(res[4], 15, "QuerySchedule doesn't return correct pricepertimeunit for given scheduleid 1")
        self.assertEqual(res[5], 1, "QuerySchedule doesn't return correct timeunitid for given scheduleid 1")
        self.assertEqual(res[6], 1, "QuerySchedule doesn't return correct currencyid for given scheduleid 1")
        self.assertEqual(res[7], 1, "QuerySchedule doesn't return correct statusid for given scheduleid 1")
        self.assertEqual(res[8], None, "QuerySchedule doesn't return correct userid for given scheduleid 1")
        self.assertEqual(res[10], 1, "QuerySchedule doesn't return correct scheduleid for given scheduleid 1")
        self.assertEqual(res[11], None, "QuerySchedule doesn't return correct poieventid for given scheduleid 1")

    def testQueryScheduleFalseargument(self):
        """
        Test whether query returns None for given false schedule id
        """
        res = parkingDb.QuerySchedule(-1)
        self.assertEqual(res, None, "QuerySchedule doesn't return None for false scheduleid -1")

    def testQueryScheduleByTimeslotHappFlow(self):
        """
        Test whether query returns the schedule properly if valid timeslot has been provided
        """
        res = parkingDb.QueryScheduleByTimeslot('2016-06-24 13:30:00+02', '2016-06-24 17:30:00+02')
        # [scheduleID, scheduleStart, scheduleEnd, status, userID, poieventid]
        self.assertEqual(res[0], 1, "QuerySchedule doesn't return correct scheduleid for given timeslot")
        self.assertEqual(res[1].isoformat(), '2016-06-24T13:30:00+02:00', "QuerySchedule doesn't return correct starttime for given timeslot")
        self.assertEqual(res[2].isoformat(), '2016-06-24T17:30:00+02:00', "QuerySchedule doesn't return correct endtime for given timeslot")
        self.assertEqual(res[3], 'available', "QuerySchedule doesn't return correct statusid for given timeslot")
        self.assertEqual(res[4], None, "QuerySchedule doesn't return correct statusid for given timeslot")
        self.assertEqual(res[5], None, "QuerySchedule doesn't return correct poieventid for given timeslot")

    def testQueryScheduleByTimeslotNonexistingtimeslot(self):
        """
        Test whether query returns None if non-existing timeslot has been provided
        """
        res = parkingDb.QueryScheduleByTimeslot('2015-06-24 13:30:00+02', '2015-06-24 17:30:00+02')
        self.assertEqual(res, None, "QuerySchedule doesn't return None for non-existing timeslot")

    def testQueryScheduleByTimeslotFalseargument(self):
        """
        Test whether query returns None if false timeslot (string and int instead of datetime or time string) has been provided
        """
        res = parkingDb.QueryScheduleByTimeslot('test1', 2)
        self.assertEqual(res, None, "QuerySchedule doesn't return None for false timeslot arguments")

    def testAddScheduleHappyFlow(self):
        """
        Test whether adding a schedule works properly when all arguments are correctly provided
        """
        sch = parkingDb.AddSchedule(1, 1, '2016-06-24 19:00:00+02', '2016-06-24 23:00:00+02', 15, 1, 1, 1, None, None)
        schid = parkingDb.QueryScheduleByTimeslot('2016-06-24 19:00:00+02', '2016-06-24 23:00:00+02')[0]
        res = parkingDb.QuerySchedule(schid)
        try:
            self.assertEqual(sch, True, "UpdateSchedule doesn't update the schedule properly with correct arguments")
            self.assertEqual(res[0], 1, "QuerySchedule doesn't return correct unitid after AddSchedule")
            self.assertEqual(res[1], 1, "QuerySchedule doesn't return correct ownerid after AddSchedule")
            self.assertEqual(res[2].isoformat(), '2016-06-24T19:00:00+02:00', "QuerySchedule doesn't return correct starttime after AddSchedule")
            self.assertEqual(res[3].isoformat(), '2016-06-24T23:00:00+02:00', "QuerySchedule doesn't return correct endtime after AddSchedule")
            self.assertEqual(res[4], 15, "QuerySchedule doesn't return correct pricepertimeunit after AddSchedule")
            self.assertEqual(res[5], 1, "QuerySchedule doesn't return correct timeunitid after AddSchedule")
            self.assertEqual(res[6], 1, "QuerySchedule doesn't return correct currencyid after AddSchedule")
            self.assertEqual(res[7], 1, "QuerySchedule doesn't return correct statusid after AddSchedule")
            self.assertEqual(res[8], None, "QuerySchedule doesn't return correct userid after AddSchedule")
            self.assertEqual(res[10], schid, "QuerySchedule doesn't return correct scheduleid after AddSchedule")
            self.assertEqual(res[11], None, "QuerySchedule doesn't return correct poieventid after AddSchedule")
            parkingDb.DeleteSchedule(res[10])
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteSchedule(res[10])

    def testUpdateScheduleHappyFlow(self):
        """
        Test whether updating of schedule works properly when all arguments are correctly provided
        """
        parkingDb.AddSchedule(1, 1, '2016-06-24 19:00:00+02', '2016-06-24 23:00:00+02', 15, 1, 1, 1, None, None)
        schid = parkingDb.QueryScheduleByTimeslot('2016-06-24 19:00:00+02', '2016-06-24 23:00:00+02')[0]
        res1 = parkingDb.QuerySchedule(schid)
        result = parkingDb.UpdateSchedule(res1[10], res1[2], res1[3], 4, 10)    # scheduleID, scheduleStartTime, scheduleEndTime, stid, userid):
        res = parkingDb.QuerySchedule(schid)
        try:
            self.assertEqual(result, True, "UpdateSchedule doesn't update the schedule properly with correct arguments")
            self.assertEqual(res[0], 1, "QuerySchedule doesn't return correct unitid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[1], 1, "QuerySchedule doesn't return correct ownerid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[2].isoformat(), '2016-06-24T19:00:00+02:00', "QuerySchedule doesn't return correct starttime for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[3].isoformat(), '2016-06-24T23:00:00+02:00', "QuerySchedule doesn't return correct endtime for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[4], 15, "QuerySchedule doesn't return correct pricepertimeunit for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[5], 1, "QuerySchedule doesn't return correct timeunitid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[6], 1, "QuerySchedule doesn't return correct currencyid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[7], 4, "QuerySchedule doesn't return correct statusid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[8], 10, "QuerySchedule doesn't return correct userid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[10], schid, "QuerySchedule doesn't return correct scheduleid for given scheduleid 1 after UpdateSchedule")
            self.assertEqual(res[11], None, "QuerySchedule doesn't return correct poieventid for given scheduleid 1 after UpdateSchedule")
            parkingDb.DeleteSchedule(res[10])
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteSchedule(res[10])

    def testResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescriptionHappyFlow(self):
        """
        Test whether the schedule status is reset properly from processing to available and userid (4) reset to NULL
        """
        parkingDb.AddSchedule(unitid=1, ownerid=1, startdatetime='2016-06-15 17:00:00+02', enddatetime='2016-06-15 21:00:00+02', pricepertimeunit=15, timeunitid=1, currencyid=1, statusid=4, userid=4, poieventid=10)
        schid = parkingDb.QueryScheduleByTimeslot(startTimeSlot='2016-06-15 17:00:00+02', endTimeSlot='2016-06-15 21:00:00+02')[0]
        res1 = parkingDb.QuerySchedule(schid)
        result = parkingDb.ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription('2577527d-f2b7-4469-91d2-f91663906574', 'K.R.C. Genk - Test3')
        res = parkingDb.QuerySchedule(schid)
        try:
            self.assertEqual(res1[7], 4, "Incorrect statusid before ResetSchedule")
            self.assertEqual(res1[8], 4, "Incorrect userid before ResetSchedule")
            self.assertTrue(result, "ResetSchedule doesn't return True for HappyFlow")
            self.assertEqual(res[7], 1, "Incorrect statusid after ResetSchedule")
            self.assertEqual(res[8], None, "Incorrect userid after ResetSchedule")
            parkingDb.DeleteSchedule(schid)
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteSchedule(schid)

    def testResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescriptionNoscheduleinstateprocessingfound(self):
        """
        Test whether the schedule status is not changed if not in state processing for given user
        """
        parkingDb.AddSchedule(unitid=1, ownerid=1, startdatetime='2016-06-15 17:00:00+02', enddatetime='2016-06-15 21:00:00+02', pricepertimeunit=15, timeunitid=1, currencyid=1, statusid=1, userid=4, poieventid=10)
        schid = parkingDb.QueryScheduleByTimeslot(startTimeSlot='2016-06-15 17:00:00+02', endTimeSlot='2016-06-15 21:00:00+02')[0]
        res1 = parkingDb.QuerySchedule(schid)
        result = parkingDb.ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription('2577527d-f2b7-4469-91d2-f91663906574', 'K.R.C. Genk - Test3')
        res = parkingDb.QuerySchedule(schid)
        try:
            self.assertEqual(res1[7], 1, "Incorrect statusid before ResetSchedule")
            self.assertEqual(res1[8], 4, "Incorrect userid before ResetSchedule")
            self.assertFalse(result, "ResetSchedule doesn't return False if Noscheduleinstateprocessingfound")
            self.assertEqual(res[7], 1, "Incorrect statusid after ResetSchedule")
            self.assertEqual(res[8], 4, "Incorrect userid after ResetSchedule")
            parkingDb.DeleteSchedule(schid)
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteSchedule(schid)

    def testResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescriptionFalseargumentNoUserID(self):
        """
        Test whether the schedule status is not changed if false argument (no user)
        """
        parkingDb.AddSchedule(unitid=1, ownerid=1, startdatetime='2016-06-15 17:00:00+02', enddatetime='2016-06-15 21:00:00+02', pricepertimeunit=15, timeunitid=1, currencyid=1, statusid=1, userid=None, poieventid=10)
        schid = parkingDb.QueryScheduleByTimeslot(startTimeSlot='2016-06-15 17:00:00+02', endTimeSlot='2016-06-15 21:00:00+02')[0]
        res1 = parkingDb.QuerySchedule(schid)
        result = parkingDb.ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription('2577527d-f2b7-4469-91d2-f91663906574', 'K.R.C. Genk - Test3')
        res = parkingDb.QuerySchedule(schid)
        try:
            self.assertEqual(res1[7], 1, "Incorrect statusid before ResetSchedule")
            self.assertEqual(res1[8], 4, "Incorrect userid before ResetSchedule")
            self.assertFalse(result, "ResetSchedule doesn't return False if FalseargumentNoUserID")
            self.assertEqual(res[7], 1, "Incorrect statusid after ResetSchedule")
            self.assertEqual(res[8], 4, "Incorrect userid after ResetSchedule")
            parkingDb.DeleteSchedule(schid)
        except AssertionError, e:
            # clean-up DB
            parkingDb.DeleteSchedule(schid)

if __name__ == '__main__':
    unittest.main()