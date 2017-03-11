__author__ = 'Jeroen Machiels'
__author_email__ = 'jeroenmachiels@gmail.com'
__version__ = '0.4'

# !/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta    # work with Python datetime functions (e.g. now())
from decimal import Decimal
import iso8601
import json
import psycopg2
import psycopg2.extensions
from psycopg2.extras import LoggingCursor
from pytz import timezone
import re   # regular expression for typecasting
import sys
import utilities

with open('./config.json', 'r') as file:
    conf = json.loads(file.read())
TIMEZONE = str(conf['timezone'])

pplazautils = utilities.utilities()

class db_logic:

    con = None
    cur = None
    DBname = None
    Host = None
    Port = None
    Username = None
    Password = None

    # Constructor - will connect to the db based on the supplied parameters
    def __init__(self, DBname, Host, Port, Username, Password):
        self.DBname = DBname
        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password

        try:
            self.con = psycopg2.connect(database=self.DBname,user=self.Username,password=self.Password,host=self.Host,port=self.Port)
            self.cur = self.con.cursor()
            self.cur.execute('SELECT version()')
            ver = self.cur.fetchone()
            print ver

            # type-cast for point
            self.cur.execute("SELECT NULL::point")
            point_oid = self.cur.description[0][1]
            POINT = psycopg2.extensions.new_type((point_oid,), "POINT", self.cast_point)
            psycopg2.extensions.register_type(POINT)

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)

    # Destructor - check if db is still connected, if yes, then disconnect and put all variables to none
    def __del__(self):
        if self.con:
            self.con.close()
            self.DBname = None
            self.Host = None
            self.Port = None
            self.Username = None
            self.Password = None
            self.con = None
            self.cur = None

    # Will connect to the dB. Even though the connection is established in constructor method. Before calling this, call first disconnect method.
    def ConnectToDb(self):
        # Below code will open a connection to the Database
        # If there is an existing open connection it will not reconnect.
        if not self.con:

            try:
                self.con = psycopg2.connect(database=self.DBname,user=self.Username,password=self.Password,host=self.Host,port=self.Port)
                self.cur = self.con.cursor()
                self.cur.execute('SELECT version()')
                ver = self.cur.fetchone()
                print ver

            except psycopg2.DatabaseError, e:
                print 'Error %s' % e
            sys.exit(1)


    # Will close the connection to the Database.
    def CloseConnection(self):
        if self.con:
            self.con.close()
            print 'connection closed'

    def CheckIfUserAlreadyExists(self,email,*therest):
        # Before adding a user this function should be called becuase this will check if email is already used in the DB.
        # returns true if email already exists and false if email is still available
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from users where email=%(em)s",{'em':email})
        #t=self.cur.mogrify("select * from users where email=%(em)s",{'em':email})
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return True

    def AddUser(self, email, fullname, useruuid, properties):
        # Call this method to add a new user to the usertable.

        # Before adding a user this function should be called becuase this will check if email is already used in the DB.
        # returns true if email already exists and false if email is still available
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from users where email=%(em)s", {'em': email})
        rows = self.cur.fetchall()
        if not rows:
            self.cur.execute("INSERT INTO users(fullname, email, useruuid, properties) VALUES (%s, %s, %s, %s)",(fullname, email, useruuid, json.dumps(properties)))
            self.con.commit()
        else:
            return "user already exists"


    #UpdateUserBasedOnUserID will update the user specified by its userid with the fields that have been passed.
    def UpdateUserBasedOnUserID(self,userid, email,fullname,useruuid,properties):
        if not self.con:
            self.ConnectToDb()
        #First check will be done to be sure that the userid is existing in the db. If non existing, then update will not be performed.
        self.cur.execute("select * from users where userid=%(usrid)s", {'usrid': userid})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE users SET fullname=%(fname)s,email=%(mail)s,useruuid=%(usruuid)s,properties=%(props)s WHERE userid=%(usrid)s", {'fname': fullname,'mail':email,'usruuid':useruuid,'props':json.dumps(properties),'usrid':userid})
            self.con.commit()
        else:
            return "userid doesn't exist, so not possible to update user"

    #UpdateUserBasedOnUserUUID will update the user specified by its useruuid with the fields that have been passed.
    def UpdateUserBasedOnUserUUID(self, email, fullname, useruuid, properties):
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the userid is existing in the db. If non existing, then update will not be performed.
        self.cur.execute("select * from users where useruuid=%(usruuid)s", {'usruuid': useruuid})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE users SET fullname=%(fname)s,email=%(mail)s,properties=%(props)s WHERE useruuid=%(usruuid)s", {'fname': fullname,'mail':email,'props':json.dumps(properties),'usruuid':useruuid})
            self.con.commit()
        else:
            return "useruuid doesn't exist, so not possible to update user"

    def UpdateUserPropsBasedOnUserUUID(self, useruuid, properties):
        """
        Update User Props field by overwriting with provided new value
        :param useruuid: uuid of user who needs to be updated
        :param properties: dictionary {} containing multiple, free attributes
        :return: true if success, else false
        """
        if not self.con:
            self.ConnectToDb()

        # data validation: make sure the properties is a dict
        if not (type(properties) == dict):
            return False
        else:
            try:
                # First check will be done to be sure that the userid is existing in the db. If non existing, then update will not be performed.
                self.cur.execute("select * from users where useruuid=%(usruuid)s", {'usruuid': useruuid})
                rows = self.cur.fetchall()
                if rows:
                    self.cur.execute("UPDATE users SET properties=%(props)s WHERE useruuid=%(usruuid)s", {'props': json.dumps(properties), 'usruuid': useruuid})
                    self.con.commit()
                    return True
                else:
                    return False
            except:
                # capture false argument (not of type uuid)
                # roll back transaction to avoid staying stuck after catching SQL error: see http://stackoverflow.com/questions/10399727/psqlexception-current-transaction-is-aborted-commands-ignored-until-end-of-tra
                self.con.rollback()
                return False

    # Method QueryUser will return all users found in the db based on an email address
    def QueryUser(self, email):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from users where email=%(em)s", {'em': email})
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return rows[0]

    def QueryUserbyUserID(self, userid):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from users where userid=%(uid)s", {'uid': userid})
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return rows[0]

    # Method QueryUUID will return UUID based on email
    def queryUUID(self, email):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select useruuid from users where email=%(em)s", {'em': email})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows[0]

    def QueryEmail(self, uuid):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select email from users where useruuid=%(usruuid)s", {'usruuid': uuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows[0]

    # Method QueryFullname will return fullname based on uuid
    def QueryFullname(self, uuid):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select fullname from users where useruuid=%(usruuid)s", {'usruuid': uuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows[0]

    # Method QueryJSONBlob will return Jsonblob based on uuid
    def QueryUserJSONBlob(self, uuid):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select properties from users where useruuid=%(usruuid)s", {'usruuid': uuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows[0]

    # Method QueryUserByUserUUID will return all users found in the db based on an useruuid
    def QueryUserByUserUUID(self, usruuid):
        """
        Query user by UUID
        :param usruuid: UUID
        :return: user if exists in our DB, else False
        """
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select * from users where useruuid=%(uuid)s",{'uuid':usruuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows
        #except:
            # no entry found (user not existing -anymore- in DB)
        #    return False

    def QueryUserIDbyUserUUID(self,usruuid):
        """
        Query userid for given useruuid
        :param usruuid: useruuid, as uuid
        :return: userid as int if useruuid exists in DB, else return None
        """
        if not self.con:
            self.ConnectToDb()
        try:
            self.cur.execute("select userid from users where useruuid=%(uuid)s",{'uuid': usruuid})
            rows = self.cur.fetchone()
            if not rows:
                return None
            else:
                return rows[0]
        except:
            # capture false argument (not of type uuid)
            # roll back transaction to avoid staying stuck after catching SQL error: see http://stackoverflow.com/questions/10399727/psqlexception-current-transaction-is-aborted-commands-ignored-until-end-of-tra
            self.con.rollback()
            return None


    #Method QueryUserID will return the userid based on an email address
    def QueryUserID(self,email):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select userid from users where email=%(em)s",{'em':email})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows

    def QueryUserIDByUUID(self, usruuid):
        """
        :param usruuid: user's UUID
        :return: userID in table
        """
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select userid from users where useruuid=%(uid)s",{'uid':usruuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            return rows[0]

    def QueryUserPropertiesForEmailconfirmationWithGivenuseridandtoken(self, userid, confirmationtoken):
        """
        Query USERS table properties field filter on given userid for keys confirmation-token and email-confirmation
        :param userid: userid as int
        :param confirmation: token as string
        :return: value behind 'email-confirmation' tag in properties if found, else None
        """

        if not self.con:
            self.ConnectToDb()
        # SELECT properties -> 'email-confirmation' FROM users WHERE userid=52 AND properties @> '{"confirmation-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbGFkZHJlc3MiOiJwcGxhemF0ZXN0MkBnbWFpbC5jb20iLCJleHAiOjE0NjcyNzU5OTl9.6dBBG4I7L2NDF6Ut71EVTTT3g4gwfOqmYYf4rylhjCc"}'
        self.cur.execute("select properties -> 'email-confirmation' FROM users WHERE userid=%(userid)s AND properties @> %(expr)s",{'userid': userid, 'expr': '{"confirmation-token": "' + str(confirmationtoken) + '"}'})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def VerifyUserPassword(self, usruuid, pw):
        """
        :param usruuid: user's UUID
        :param pw: user's password
        :return: true if match, "not email user" if Google login/signup, else False
        """
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select properties from users where useruuid=%(uid)s",{'uid':usruuid})
        rows = self.cur.fetchone()
        if not rows:
            return False
        else:
            try:
                return rows[0]['password'] == pw
            except (KeyError), e:
                # print("server.py/schedule/findAvailableParkingUnit: ", e)
                return "no " + e.message

    def DeleteUser(self, userid):
        """
        Delete User with given userid
        :param userid: userid of user who needs to be deleted
        :return: true if success, else false
        """
        if not self.con:
            self.ConnectToDb()

        # First check will be done to be sure that the userid is existing in the db. If non existing, then delete will not be performed.
        self.cur.execute("select * from users where userid=%(userid)s", {'userid': userid})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("delete from users where userid=%(userid)s", {'userid': userid})
            self.con.commit()
            return True
        else:
            return False

    #Method AddOwner will ad an owner based on the email address.
    def AddOwner(self,email,bankaccount,properties):
        #when adding owner, we need to have the user ID.
        # This user ID we will receive via the email address of the user
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select userid from users where email=%(em)s",{'em':email})
        userid = self.cur.fetchall()
        if not userid:
            #user doesn't exists in DB, so not possible to add him as owner
            return "User doesn't exits in DB, first add as a user before making an owner"
        else:
            #UserID is in userid[0]
            #print userid[0]
            self.cur.execute("INSERT INTO owner(userid, bankaccount, properties) VALUES (%s, %s, %s)",(userid[0],bankaccount,json.dumps(properties)))
            self.con.commit()
            return "user has been added as owner"

    def AddOwnerWithUUID(self, usruuid, bankaccount, properties):
        """
        Add owner with existing user UUID, bankaccount and additional properties
        :param usruuid: user UUID (existing in users table)
        :param bankaccount: new bankaccount in IBAN format (BEXX XXXX XXXX XX)
        :param properties: additional data, e.g. Terms Of Service check timestamp
        :return: ownerID if success, else Error message
        """
        # self.cur.execute("select userid from users where email=%(em)s",{'em':email})
        userid = self.QueryUserIDbyUserUUID(usruuid)
        if not userid:
            # user doesn't exists in DB, so not possible to add him as owner
            return "Error: no existing user in DB"
        else:
            if not self.con:
                self.ConnectToDb()
            self.cur.execute("INSERT INTO owner(userid, bankaccount, properties) VALUES (%s, %s, %s)", (userid, bankaccount, json.dumps(properties)))
            self.con.commit()
            # fetch new ownerid and return this
            self.cur.execute("select ownerid from users,owner where (users.userid = owner.userid and users.useruuid=%(id)s)", {'id': usruuid})
            result = self.cur.fetchone()
            return result[0]

    def QueryOwnerIDWithUUID(self, usruuid):
        """
        Query ownerID based on user's UUID
        :param usruuid: user's UUID
        :return: owner ID if available, 0 if no owner available yet
        """
        userid = self.QueryUserIDbyUserUUID(usruuid)
        if not userid:
            # user doesn't exists in DB, so not possible to find him as owner
            return 0
        else:
            if not self.con:
                self.ConnectToDb()
            self.cur.execute("select ownerid from users,owner where (users.userid = owner.userid and users.useruuid=%(id)s)", {'id': usruuid})
            result = self.cur.fetchone()
            if result is None:
                return 0
            else:
                return result[0]

    #This method will return all fields from users & owner table. in sequential column order.
    #Maybe afterwards include some joins to have more meaningfull text istead of a lot of ID's.
    def QueryOwnerandUserInfo(self, email):
        #eerst via email the userid krijgen, dan via user id query uitoefenen of users&owners
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select userid from users where email=%(em)s",{'em':email})
        userid = self.cur.fetchall()

        self.cur.execute("select * from users,owner where (users.userid = owner.userid and users.userid=%(id)s)",{'id':userid[0]})
        result = self.cur.fetchone()
        return result

    #This method will return the owner ID based on the email address.
    def QueryOwnerID(self, email):
        if not self.con:
            self.ConnectToDb()
        #eerst via email the userid krijgen, dan via user id query uitoefenen of users&owners
        self.cur.execute("select userid from users where email=%(em)s",{'em':email})
        userid = self.cur.fetchone()

        self.cur.execute("select ownerid from users,owner where (users.userid = owner.userid and users.userid=%(id)s)",{'id':userid[0]})
        result = self.cur.fetchone()
        return result

    def QueryOwnerBankAccount(self, ownerid):
        """
        :param ownerid: owner ID
        :return: Owner Bank account
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select bankaccount from owner where ownerid=%(id)s", {'id': ownerid})
        result = self.cur.fetchone()
        return result[0]

    #This method will add a POI to the POI table.
    def AddPoi(self,poifriendlyname,country,city,properties):
        if not self.con:
            self.ConnectToDb()
        #Add POI
        self.cur.execute("INSERT INTO poi(poifriendlyname, country, city, properties) VALUES (%s, %s, %s, %s)",(poifriendlyname,country,city,json.dumps(properties)))
        self.con.commit()
        return "POI has been added"

    # Method GetAllPoiFriendlyNames will return poifriendlyname for all Poi's found in the db
    def GetAllPoiFriendlyNames(self):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select poifriendlyname from poi;")
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return [element for (element,) in rows]

    def GetAllPois(self):
        """
        Return list of all Pois order alphabetically by poiname
        :return: [(name, poicountry, poitcity, center{lat,lon}, poiTypeName)]
        """
        if not self.con:
            self.ConnectToDb()

        # select poi.poifriendlyname, poi.country, poi.city, poi.center, poitype.poitype from public.poi, public.poitype where poi.poitypeid=poitype.poitypeid order by poi.poifriendlyname
        self.cur.execute("select poi.poifriendlyname, poi.country, poi.city, poi.center, poitype.poitype from public.poi, public.poitype where poi.poitypeid=poitype.poitypeid order by poi.poifriendlyname")
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            columns = ('poiname', 'poicountry', 'poicity', 'poicenter', 'poitype')
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results

    def GetPoisOfGivenType(self, poiTypeName):
        """
        Return list of all Pois of given PoiTypeName order alphabetically by poiname
        -- NOT USED TODAY--
        :param poiTypeName: name of poitype
        :return: [(poiname, poicenter{lat,lon})]
        """
        if not self.con:
            self.ConnectToDb()

        # select poi.poifriendlyname, poi.center from public.poi, public.poitype where poitype.poitype='eventparking' AND poi.poitypeid=poitype.poitypeid order by poi.poifriendlyname
        self.cur.execute("select poi.poifriendlyname, poi.center from public.poi, public.poitype where poitype.poitype=%(tp)s AND poi.poitypeid=poitype.poitypeid order by poi.poifriendlyname", {'tp': poiTypeName})
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            columns = ('poiname', 'poicenter')
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results

    # This method will return poifriendlyname, country, city, properties & poiid based on the poifriendlyname
    def GetPoiInfoViaFriendlyName(self, poiFriendlyname):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select * from poi where poiFriendlyname=%(poifr)s",{'poifr':poiFriendlyname})
        result = self.cur.fetchall()
        return result

    # This method will return poifriendlyname, country, city, properties & poiid based on country
    def GetPoiInfoViaCountry(self, Country):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from poi where country=%(cntry)s",{'cntry':Country})
        result = self.cur.fetchall()
        return result

    #This method will return poifriendlyname, country, city, properties & poiid based on city
    def GetPoiInfoViaCity(self, City):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from poi where city=%(cit)s",{'cit':City})
        result = self.cur.fetchall()
        return result

    def GetPoiCityViaID(self, poid):
        """
        :param poid: POI ID
        :return: city
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select city from poi where poiid=%(id)s", {'id': poid})
        result = self.cur.fetchone()
        return result[0]

    def GetAllPoiTypes(self):
        """
        Return list of all PoiTypes
        :return: [(poiTypeName)]
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select poitype from poitype")
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            results = []
            for row in rows:
                results.append(row[0])
            return results

    #This method will return POIID based on poifriendlyname
    def QueryPoiID(self, poiFriendlyname):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select poiid from poi where poiFriendlyname=%(poifr)s",{'poifr':poiFriendlyname})
        result = self.cur.fetchone()
        return result

    def QueryPoiFriendlyname(self, poiid):
        """
        :param poiid: POI ID as int
        :return: POI friendlyname
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select poiFriendlyname from poi where poiid=%(poid)s",{'poid':poiid})
        result = self.cur.fetchone()
        return result[0]

    def QueryPoiFriendlynameByUnitid(self, unitid):
        """
        :param poiid: Unit ID
        :return: POI friendlyname, None if none found
        """
        if not self.con:
            self.ConnectToDb()

        # select poi.poiFriendlyname from public.poi, public.unit where unit.poiid=poi.poiid and unit.unitid=1
        self.cur.execute("select poi.poiFriendlyname from public.poi, public.unit where unit.poiid=poi.poiid and unit.unitid=%(unid)s", {'unid': unitid})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def QueryPoiCenterByUnitid(self, unitid):
        """
        :param poiid: Unit ID
        :return: POI center, None if none found
        """
        if not self.con:
            self.ConnectToDb()

        # select poi.center from public.poi, public.unit where unit.poiid=poi.poiid and unit.unitid=245
        self.cur.execute("select poi.center from public.poi, public.unit where unit.poiid=poi.poiid and unit.unitid=%(unid)s", {'unid': unitid})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def QueryPoiPricepertimeunit(self, poiid):
        """
        :param poiid: POI ID as int
        :return: POI pricepertimeunit as int, None if none found
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select pricepertimeunit from poi where poiid=%(poid)s",{'poid':poiid})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    #This method will ad a type with properties to the type table
    def AddType(self, type, properties):
        #Add Type
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("INSERT INTO type(type, properties) VALUES (%s, %s)",(type,json.dumps(properties)))
        self.con.commit()
        return "Type has been added"

    #This method will return type, properties & typeid based on the type
    def QueryType(self,type):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from type where type=%(tp)s",{'tp':type})
        result = self.cur.fetchall()
        return result

    def GetAllUnitTypes(self):
        """
        Return list of all UnitTypes
        :return: [(UnitTypeName)]
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select type from type")
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            results = []
            for row in rows:
                results.append(row[0])
            return results

    #this method will rertun the typeid base don the type
    def QueryTypeID(self,type):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select typeid from type where type=%(tp)s",{'tp':type})
        result = self.cur.fetchone()
        return result[0]


    #This method will add a currency and properties to the currency table
    def AddCurrency(self,currency,properties):
        if not self.con:
            self.ConnectToDb()

        #Add Currency
        self.cur.execute("INSERT INTO currency(currency, properties) VALUES (%s, %s)",(currency,json.dumps(properties)))
        self.con.commit()
        return "Currency has been added"

    #this method will return all info (currency & currencyid) from the currency table based on the supplied currency parameter
    def QueryCurrency(self,currency):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from currency where currency=%(cur)s",{'cur':currency})
        result = self.cur.fetchall()
        return result

    #This method will return the currency ID based on the supplied currency
    def QueryCurrencyID(self,currency):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select currencyid from currency where currency=%(cur)s",{'cur':currency})
        result = self.cur.fetchone()
        return result

    #this method will add a status & properties to the db. (status can be eg. reserved, booked, ... )
    def AddStatus(self,status,properties):
        #Add Status
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("INSERT INTO status(status, properties) VALUES (%s, %s)",(status,json.dumps(properties)))
        self.con.commit()
        return "Status has been added"

    #This method will query all information available about a certain status in the db
    def QueryStatus(self,status):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from status where status=%(sts)s",{'sts':status})
        result = self.cur.fetchall()
        return result

    #This method will query the statusid based on the supplied status
    def QueryStatusID(self,status):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select statusid from status where status=%(sts)s",{'sts':status})
        result = self.cur.fetchone()
        return result[0]

    def AddUnit(self, unitfriendlyname, latlong, userid, typeid, poiid, ownerid, cityname, properties):
        """
        This method will add a unit to the unittable -- a lot of crossreferences needed for this!
        :param unitfriendlyname:
        :param latlong:
        :param userid:
        :param typeid:
        :param poiid:
        :param ownerid:
        :param cityname:
        :param properties:
        :return: "Unit has been added"
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("INSERT INTO unit(friendlyname,latitudelongitude, userid,typeid,poiid,ownerid,cityname,properties) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)",(unitfriendlyname,latlong,userid,typeid,poiid,ownerid,cityname,json.dumps(properties)))
        self.con.commit()
        return "Unit has been added"

    def UpdateUnitProperties(self, unitid, props):
        """
        Update or add (if key not yet existing) the properties field in the UNIT table with given props
        :param unitid: unitid, as int
        :param props: properties field added to table, as Python dictionary
        :return: existing properties dictionary is extended or updated (not overwritten!!)
        """
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the id is existing in the db. If non existing, then update will not be performed.
        # select * from unit where unitid=1
        self.cur.execute("select * from unit where unitid=%(unid)s", {'unid': unitid})
        rows = self.cur.fetchall()
        if rows:
            # old: UPDATE unit SET properties='{"setschedule": {"poieventid": 10, "timestamp":"26/2"}}' WHERE unitid=1
            # bugfix: UPDATE unit SET properties = JSONB_SET(properties, '{setschedule}', (SELECT '{"poieventid": 10, "timestamp":"26/2"}'::jsonb), true) WHERE unitid=247;
            for item in props.keys():
                #iterate over the top-level keys provide in the props parameter and add / update each
                print item
                print props[item]
                self.cur.execute("UPDATE unit SET properties = JSONB_SET(properties, %(item)s, (SELECT %(propsitem)s::jsonb), true) WHERE unitid=%(unid)s", {'propsitem': json.dumps(props[item]), 'item': '{'+item+'}', 'unid': unitid})
            self.con.commit()
        else:
            return "id not found"

    def OverwriteUnitProperties(self, unitid, props):
        """
        Overwrite the properties field in the UNIT table with given props
        :param unitid: unitid, as int
        :param props: properties field added to table, as Python dictionary
        :return: overwrite properties field of given unitid
        """
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the id is existing in the db. If non existing, then update will not be performed.
        # select * from unit where unitid=1
        self.cur.execute("select * from unit where unitid=%(unid)s", {'unid': unitid})
        rows = self.cur.fetchall()
        if rows:
            # old: UPDATE unit SET properties='{"setschedule": {"poieventid": 10, "timestamp":"26/2"}}' WHERE unitid=1
            self.cur.execute("UPDATE unit SET properties = %(props)s WHERE unitid=%(unid)s", {'props': json.dumps(props), 'unid': unitid})
            self.con.commit()
        else:
            return "id not found"

    def QueryUnitPropertiesForSetScheduleWithGivenPoieventid(self, unitid, poieventid):
        """
        Query UNIT table properties field filter on given unitid and poieventid tag within setschedule tag
        :param unitid: unitid as int
        :param poieventid: poieventid as int
        :return: timestamp encoded in that properties setschedule tag or None
        """

        if not self.con:
            self.ConnectToDb()
        # SELECT properties FROM unit WHERE unitid=1 AND properties->'setschedule' @> '{"poieventid":10}';   ""
        self.cur.execute("select properties FROM unit WHERE unitid=%(uid)s AND properties->%(tag)s @> %(expr)s",{'uid': unitid, 'tag': 'setschedule','expr': '{"poieventid":' + str(poieventid) + '}'})
        result = self.cur.fetchone()
        if result:
            return result[0]['setschedule']['timestamp']
        else:
            return None

    def GetUniqueUnitFriendlyName(self, cityName):
        """
        Generate a unique unit friendlyName based on the provided cityName
        :param cityName: unit cityname as text
        :return: unit friendlyName as text
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select count(friendlyname) from unit where cityname=%(cname)s",{'cname':cityName})
        c = self.cur.fetchone()
        result = cityName[0] + str(c[0] + 1)
        return result

    # This method will query the unitid based on the unitfriendlyname
    def QueryUnitId(self,unitfriendlyname):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select unitid from unit where friendlyname=%(frname)s",{'frname':unitfriendlyname})
        result = self.cur.fetchone()
        return result[0]

    def QueryUnitsForgivenuserid(self, userID):
        """
        Query units for given userID
        :param userID: as int
        :return: list [unit.friendlyname, unit.latitudelongitude, type.type, unit.cityname, unit.properties]
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select unit.friendlyname, unit.latitudelongitude, type.type, unit.cityname, unit.properties from unit, type where unit.userid=%(uid)s and unit.typeid=type.typeid",{'uid':userID})
        result = self.cur.fetchall()
        return result

    def QueryUnitFriendlyName(self, unitid):
        """
        Query unit friendlyName based on the provided unitid
        :param unitid: unit id
        :return: unit friendlyName as text
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select friendlyname from unit where unitid=%(uid)s",{'uid':unitid})
        result = self.cur.fetchone()[0]
        return result

    def QueryUnit(self, unitid):
        """
        Query unit based on the provided unitid
        :param unitid: unit id
        :return: full unit record as dict ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from unit where unitid=%(uid)s",{'uid':unitid})
        unit = self.cur.fetchone()
        if not unit:
            return None
        else:
            columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
            return dict(zip(columns, unit))

    def QueryUnitAddress(self, unitid):
        """
        Query unit address based on the provided unitid
        :param unitid: unit id
        :return: unit address as text, None if none found
        """
        if not self.con:
            self.ConnectToDb()

        # select properties->'fulladdress' from unit where unitid = 246
        self.cur.execute("select properties->%(tag)s from unit where unitid=%(uid)s",{'tag': "fulladdress", 'uid':unitid})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def QueryUnitAddressByUnitname(self, unitname):
        """
        Query unit address based on the provided unitname
        :param unitname: unitname
        :return: unit address as text, None if none found
        """
        if not self.con:
            self.ConnectToDb()

        # select properties->'fulladdress' from unit where friendlyname = 'A2'
        self.cur.execute("select properties->%(tag)s from unit where friendlyname=%(uname)s",{'tag': "fulladdress", 'uname':unitname})
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def QueryUnitByUserId(self, userid):
        """
        Query unit based on the provided userid
        :param userid: user id
        :return: full unit record as dict ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from unit where userid=%(userid)s",{'userid':userid})
        unit = self.cur.fetchone()
        if not unit:
            return None
        else:
            columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
            return dict(zip(columns, unit))

    def QueryUnitsByUserUUID(self, useruuid):
        """
        Query units based on the provided useruuid
        :param useruuid: useruuid
        :return: full unit record as dict ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from public.unit, public.users where unit.userid=users.userid and users.useruuid=%(useruuid)s",{'useruuid':useruuid})
        rows = self.cur.fetchall()
        if not rows:
            return None
        else:
            columns = ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results

    # Below code is adding a schedule
    # Timestamp of schedule.json looks like: 2016-01-21T09:00:00.000Z
    def AddSchedule(self, unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, userid, poieventid, properties=None):
        if not self.con:
            self.ConnectToDb()

        # Add Schedule
        if not userid:
            self.cur.execute("INSERT INTO schedule(unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,poieventid,properties) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)",(unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,poieventid,json.dumps(properties)))
        else:
            # INSERT INTO schedule (unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, poieventid) VALUES (3, 1, '2016-06-19 19:30:00+02', '2016-06-19 23:30:00+02', 10, 1, 1, 1, 11);
            self.cur.execute("INSERT INTO schedule(unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,userid,poieventid,properties) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",(unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,userid,poieventid,json.dumps(properties)))
        self.con.commit()
        return True

    def QuerySchedule(self, scheduleid):
        """
        Query SCHEDULE table to return schedule with given ID
        :param scheduleid: ID from SCHEDULE table
        :return: None if negative, [unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,userid,properties,scheduleid,poieventid]
        """
        if not self.con:
            self.ConnectToDb()

        # select * from schedule where scheduleid='125'
        self.cur.execute("select * from schedule where scheduleid=%(schid)s",{'schid':scheduleid})
        result = self.cur.fetchone()
        return result

    def QuerySchedulesbyUserUUIDandStatus(self, usruuid, sts):
        """
        Query SCHEDULE table to return all reserved schedules for given User UUID
        :param usruuid: user UUID
        :param status: schedule status string
        :return: list of schedules [], null if none found
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select unit.friendlyname, schedule.startdatetime, schedule.enddatetime from public.schedule, public.status, public.unit, public.users where status.status=%(sta)s AND users.useruuid=%(uid)s AND schedule.unitid=unit.unitid AND schedule.statusid=status.statusid and schedule.userid=users.userid", {'uid':usruuid, 'sta':sts})
        result = self.cur.fetchall()
        return result

    def QueryScheduleByTimeslot(self, startTimeSlot, endTimeSlot):
        """
        Query SCHEDULE table to return schedule for given timeslot
        :param startTimeslot: timeslot startdatetime
        :param endTimeslot: timeslot enddatetime
        :return: None if not found or false arguments, else [scheduleID, scheduleStart, scheduleEnd, status, userID, poieventid]
        """
        if not self.con:
            self.ConnectToDb()

        if (pplazautils.checkIfValidDatetime(startTimeSlot) and pplazautils.checkIfValidDatetime(endTimeSlot)):
            self.cur.execute("select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid, schedule.poieventid from public.schedule, public.status, public.users where schedule.startdatetime=%(start)s AND schedule.enddatetime=%(end)s AND schedule.statusid=status.statusid", {'start':startTimeSlot,'end':endTimeSlot})
            result = self.cur.fetchone()
            return result
        else:
            # not timestamp arguments
            return None

    def QueryScheduleStatusByUserUUIDandTimeslot(self, usruuid, startTimeSlot, endTimeSlot):
        """
        Query SCHEDULE table to return schedule for given User UUID
        :param usruuid: user UUID
        :param startTimeslot: timeslot startdatetime
        :param endTimeslot: timeslot enddatetime
        :return: null if not found, else [scheduleID, scheduleStart, scheduleEnd, status, userID]
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid from public.schedule, public.status, public.users where schedule.startdatetime=%(start)s AND schedule.enddatetime=%(end)s AND users.useruuid=%(uid)s AND schedule.statusid=status.statusid", {'start':startTimeSlot,'end':endTimeSlot, 'uid':usruuid})
        result = self.cur.fetchone()
        return result

    def QuerySchedulePricebyUuidTimeslotsandUnitID(self,usruuid, startTimeSlot, endTimeSlot, unitid):
        """
        Query SCHEDULE table to return price per hour for given User UUID, schedule start & stop and unitid
        :param usruuid: user UUID
        :param startTimeslot: timeslot startdatetime
        :param endTimeslot: timeslot enddatetime
        :param unitid: unit id
        :return: null if not found, else [pricepertimeunit]
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select schedule.pricepertimeunit, schedule.timeunitid from schedule, users where schedule.startdatetime=%(start)s AND schedule.enddatetime=%(end)s AND users.useruuid=%(uid)s AND schedule.unitid=%(unid)s and schedule.userid = users.userid", {'start':startTimeSlot,'end':endTimeSlot, 'uid':usruuid, 'unid':unitid})
        result = self.cur.fetchone()
        return result

    def QueryScheduleinstatusprocessingByUserUUIDandTimeslot(self, usruuid, starttimeslot, endtimeslot):
        """
        Query SCHEDULE table to return schedule in status 'processing' for given User UUID
        :param usruuid: user UUID
        :param starttimeslot: timeslot startdatetime
        :param endtimeslot: timeslot enddatetime
        :return: null if not found, else [scheduleID, scheduleStart, scheduleEnd, status, userID, pricepertimeunit, timeunitid]
        """
        if not self.con:
            self.ConnectToDb()

        # select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid, schedule.pricepertimeunit, schedule.timeunitid from public.schedule, public.status, public.users where status.status='processing' AND schedule.startdatetime='2016-05-11 10:00:00+02' AND schedule.enddatetime='2016-05-11 11:00:00+02' AND users.useruuid='605bada9-139e-4efe-89e7-7a62bcd53001' AND schedule.statusid=status.statusid AND schedule.userid = users.userid
        self.cur.execute("select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid, schedule.pricepertimeunit, schedule.timeunitid from public.schedule, public.status, public.users where status.status='processing' AND schedule.startdatetime=%(start)s AND schedule.enddatetime=%(end)s AND users.useruuid=%(uid)s AND schedule.statusid=status.statusid AND schedule.userid = users.userid", {'start':starttimeslot,'end':endtimeslot, 'uid':usruuid})
        result = self.cur.fetchone()
        return result

    def QueryScheduleinstatusprocessingByUserUUIDandEventdescription(self, usruuid, eventdescription):
        """
        Query SCHEDULE table to return schedule in status 'processing' for given User UUID and given event description
        :param usruuid: user UUID
        :param eventdescription: eventdescription as string
        :return: None if not found, else [scheduleID, scheduleStart, scheduleEnd, status, userID, pricepertimeunit, timeunitid]
        """
        if not self.con:
            self.ConnectToDb()

        # select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid, schedule.pricepertimeunit, schedule.timeunitid from public.schedule, public.status, public.users, public.poievents where status.status='processing' AND schedule.poieventid=poievents.poieventid AND poievents.eventdescription='R.S.C. Anderlecht - Test1' AND users.useruuid='2967b3f5-e3f0-41be-87c5-1f1ad6fc61c2' AND schedule.statusid=status.statusid AND schedule.userid = users.userid
        self.cur.execute("select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, status.status, schedule.userid, schedule.pricepertimeunit, schedule.timeunitid from public.schedule, public.status, public.users, public.poievents where status.status='processing' AND schedule.poieventid=poievents.poieventid AND poievents.eventdescription=%(eventdes)s AND users.useruuid=%(uid)s AND schedule.statusid=status.statusid AND schedule.userid = users.userid", {'eventdes':eventdescription, 'uid':usruuid})
        result = self.cur.fetchone()
        if not result:
            return None
        else:
            columns = ('scheduleID', 'scheduleStart', 'scheduleEnd', 'status', 'userID', 'pricepertimeunit', 'timeunitid')
            return dict(zip(columns, result))

    def QueryFutureSchedulesbyUnitname(self, unitname, unittest=False):
        """
        Query SCHEDULE table to return all future schedules for given Unitname, ordered by poievents.eventstart
        Contains hard-coded timemstap for unittests (in line with Benares-dev): startdatetime beyond '2016-06-10 13:00:00+02'
        :param unitname: unitname as string
        :return: list of schedules ['eventstart', 'eventdescription', 'schedulestatus'], [] if none found
        """
        if not self.con:
            self.ConnectToDb()

        # select poievents.eventstart, poievents.eventdescription, status.status from public.schedule, public.poievents, public.status, public.unit where unit.friendlyname='A1' and unit.unitid=schedule.unitid and schedule.poieventid=poievents.poieventid and status.statusid=schedule.statusid and schedule.startdatetime>'2016-06-10 13:00:00+02' order by poievents.eventstart

        if unittest:
            self.cur.execute("select poievents.eventstart, poievents.eventdescription, status.status from public.schedule, public.poievents, public.status, public.unit where unit.friendlyname=%(unitn)s and unit.unitid=schedule.unitid and schedule.poieventid=poievents.poieventid and status.statusid=schedule.statusid and schedule.startdatetime>'2016-06-10 13:00:00+02' order by poievents.eventstart", {'unitn':unitname})
            rows = self.cur.fetchall()
        else:
            self.cur.execute("select poievents.eventstart, poievents.eventdescription, status.status from public.schedule, public.poievents, public.status, public.unit where unit.friendlyname=%(unitn)s and unit.unitid=schedule.unitid and schedule.poieventid=poievents.poieventid and status.statusid=schedule.statusid and schedule.startdatetime>%(start)s order by poievents.eventstart", {'unitn':unitname, 'start': timezone(TIMEZONE).localize(datetime.now())})
            rows = self.cur.fetchall()

        if not rows:
            return []
        else:
            columns = ('eventstart', 'eventdescription', 'schedulestatus')
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            return results

    def ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription(self, usruuid, eventdescription):
        """
        Reset SCHEDULE record identified by given User UUID and given event description from status 'processing' to state 'available' (reason= abortion of reservation workflow so schedule record should be "freed up again")
        :param usruuid: user UUID
        :param eventdescription: eventdescription as string
        :return: True if successfully updated, else False
        """
        if not self.con:
            self.ConnectToDb()

        # verify whether a schedule in status processing exists for the given user and eventdescription
        sch = self.QueryScheduleinstatusprocessingByUserUUIDandEventdescription(usruuid, eventdescription)
        if sch:
            availableid = self.QueryStatusID('available')
            uid = self.QueryUserIDbyUserUUID(usruuid)
            poieventid = self.QueryPoieventIDByEventdescription(eventdescription)
            # update schedule set statusid=1, userid=NULL where userid = 40 AND poieventid = 8
            self.cur.execute("update schedule set statusid= %(statid)s, userid=NULL where userid = %(uid)s AND poieventid = %(eventid)s", {'statid': availableid, 'uid': uid, 'eventid': poieventid})
            self.con.commit()
            return True
        else:
            return False

    # Query unit
    # Starting point is the following:
    # 1) query poi table with friendlyname
    # 2) Based on poiid, search units with their points
    # 3) http://www.postgresql.org/docs/8.3/static/earthdistance.html -> choosen method is: F8.2 point based earth distances.
    #   One disadvantage of the longitude/latitude representation is that you need to be careful about the edge conditions
    #   near the poles and near +/- 180 degrees of longitude. The cube-based representation avoids these discontinuities.
    #   Operator	    Returns	Description
    #   point <@> point	float8	Gives the distance in statute miles between two points on the Earth's surface
    # 4) function will return first 30 units with closest to destination location as first, the last field is the distance to the unit in KM
    def QueryUnitsNearLocationAtPOI(self, poifriendlyname, destlatitude, destlongitude):
        if not self.con:
            self.ConnectToDb()

        # the below will search for the POIID based on a poifriendlyname
        self.cur.execute("select poiid from poi where poifriendlyname=%(poifr)s",{'poifr':poifriendlyname})
        reqpoiid = self.cur.fetchone()

        # if reqpoiid is not empty then execute query on unit table
        if reqpoiid:
            self.cur.execute("select friendlyname,latitudelongitude,unitid,userid,ownerid,typeid,properties, round( ( latitudelongitude <@> point(%(lat)s,%(long)s) )::numeric * 1.609344, 3 ) as km from unit where poiid=%(poiID)s order by latitudelongitude <-> point(%(lat)s,%(long)s)limit 30",{'poiID':reqpoiid,'lat':destlatitude,'long':destlongitude})
            result = self.cur.fetchall()
            return result

    def FindPoiIDforGivenPoint(self, point):
        """
        Check whether the given point 'belongs to a Poi': if point (lat,lon) is closer <=2.5km from the Poi Center (DB Point calculation), it's considered to belong to this Poi
        :param point: 'lat,lon' of certain point position on earth
        :return: PoiID if point belongs to specific Poi, else 0
        """
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select poiid, round( ( center <@> point(%(latlong)s) )::numeric * 1.609344, 3) as km from poi where round( ( center <@> point(%(latlong)s) )::numeric * 1.609344, 3 ) < 2.5 order by center <-> point(%(latlong)s) limit 5", {'latlong': point})
        # return first item of list (closest)
        result = self.cur.fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    def QueryIfUnitExists(self, point):
        """
        Check whether the existing point already exists as unit in our DB (avoid duplicates)
        :param point: 'lat,lon' of certain point position on earth.
        :return: true if DB already holds a unit with latitudelongitude == point
        """
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select unitid from unit where latitudelongitude ~= point(%(latlong)s)", {'latlong': point})
        result = self.cur.fetchall()
        if result:
            return True
        else:
            return False

    def QueryAvailableScheduleNotFixedPrice(self, unitid, customerstartdatetime, customerenddatetime, statusname):
        """
        Query SCHEDULE table to return whether unit has given status in start-end time slot; HARD-CODED filter on schedules that are 'not fixed price (timeunitid != 1)'
        :param unitid: ID from UNITS table
        :param customerstartdatetime: startTime of time-slot in ISO 8601 UTC time
        :param customerenddatetime: endTime of time-slot in ISO 8601 UTC time
        :param statusname: specific status of unit
        :return: null if negative, [scheduleID, scheduleStartTime, scheduleEndTime, schedulePricePerHour, Currency, Status, unitID, ownerID, userID]
        """
        if not self.con:
            self.ConnectToDb()

        # TODO: add catch for 'wrong statusname'?
        # TEST QUERY
        # select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, schedule.pricepertimeunit, currency.currency, status.status, schedule.unitid, schedule.ownerid, schedule.userid from public.schedule,public.status,public.currency where schedule.statusid = status.statusid AND schedule.currencyid = currency.currencyid AND schedule.unitid = 2 AND schedule.startdatetime <= '2016-05-11 13:00:00+02:00' AND schedule.enddatetime >= '2016-05-11 14:00:00+02:00' AND status.status = 'available' AND schedule.timeunitid != 1
        self.cur.execute("select schedule.scheduleid, schedule.startdatetime, schedule.enddatetime, schedule.pricepertimeunit, currency.currency, status.status, schedule.unitid, schedule.ownerid, schedule.userid from public.schedule,public.status,public.currency where schedule.statusid = status.statusid AND schedule.currencyid = currency.currencyid AND schedule.unitid = %(unid)s AND schedule.startdatetime <= %(start)s AND schedule.enddatetime >= %(end)s AND status.status = %(sts)s AND schedule.timeunitid != 1", {'unid':unitid,'start':customerstartdatetime,'end':customerenddatetime,'sts':statusname})
        availableSchedule = self.cur.fetchone()
        return availableSchedule

    def UpdateSchedule(self, scheduleID, scheduleStartTime, scheduleEndTime, stid, userid):
        """
        Update schedule with given ID
        :param scheduleID: schedule ID that will be changed
        :param scheduleStartTime: startTime of schedule
        :param scheduleEndTime: endTime of schedule
        :param statusid: status ID
        :param userid: user ID
        :return: true if success, else false
        """
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the scheduleID is existing in the db. If non existing, then update will not be performed.
        self.cur.execute("select * from schedule where scheduleid=%(schid)s", {'schid': scheduleID})
        rows = self.cur.fetchall()
        if rows:
            if not userid:
                self.cur.execute("UPDATE schedule SET startdatetime=%(start)s,enddatetime=%(end)s,statusid=%(statid)s WHERE scheduleid=%(schid)s", {'start': scheduleStartTime,'end':scheduleEndTime,'statid':stid,'schid':scheduleID})
            else:
                self.cur.execute("UPDATE schedule SET startdatetime=%(start)s,enddatetime=%(end)s,statusid=%(statid)s,userid=%(uid)s WHERE scheduleid=%(schid)s", {'start': scheduleStartTime,'end':scheduleEndTime,'statid':stid,'uid':userid,'schid':scheduleID})
            self.con.commit()
            return True
        else:
            return False

    def UpdateEventSchedule(self, scheduleID, stid, userid):
        """
        Update event schedule with given ID
        :param scheduleID: schedule ID that will be changed
        :param statusid: status ID
        :param userid: user ID
        :return: true if success, else false
        """
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the scheduleID is existing in the db. If non existing, then update will not be performed.
        self.cur.execute("select * from schedule where scheduleid=%(schid)s", {'schid': scheduleID})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE schedule SET statusid=%(statid)s,userid=%(uid)s WHERE scheduleid=%(schid)s", {'statid':stid,'uid':userid,'schid':scheduleID})
            self.con.commit()
            return True
        else:
            return "scheduleID doesn't exist, so not possible to update schedule"

    # This method will delete a specific schedule based on the schedule id. Please note that there is no roll back possible after delete.
    # Maybe should we add the specified line first to a backup table before delete, so we can execute a rollback if necessary ? - To be discussed for another sprint
    def DeleteSchedule(self, scheduleid):
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("delete from schedule where scheduleid = %(schid)s",{'schid':scheduleid})
        self.con.commit()
        return "Schedule has been deleted"

    #This method will add an event to the event db. Goal is to dump as much as possible information in this table for later usage.
    def AddEvent(self, timestamp, groupname, properties):
        if not self.con:
            self.ConnectToDb()

        try:
            json.dumps(properties)
        except: # catch Decimal and Python Datetime serialization errors
            for key, value in properties.iteritems():
                if type(value) == dict:
                    for k, v in value.iteritems():
                        if type(v) == Decimal:
                            properties[key][k] = float(v)
                        if type(v) == datetime:
                            properties[key][k] = v.isoformat()
                elif type(value) == tuple:
                    result = [None] * len(value)
                    i = 0
                    for item in value:
                        if type(item) == Decimal:
                            result[i] = float(item)
                        if type(item) == datetime:
                            result[i] = item.isoformat()
                        else:
                            result[i] = item
                        i += 1
                    # replace tuple by array with datetime converted
                    properties[key] = result

                else:
                    if type(value) == Decimal:
                        properties[key] = float(value)
                    if type(value) == datetime:
                        properties[key] = value.isoformat()

        self.cur.execute("INSERT INTO events(timestamp,groupname,properties) VALUES (%s, %s, %s)",(timestamp,groupname,json.dumps(properties)))
        self.con.commit()
        return "Event has been added"

    def cast_point(self, value, cur):
        """
        Support method to typecast PostgreSQL point object
        """
        if value is None:
            return None

        # Convert from (f1, f2) syntax using a regular expression.
        m = re.match(r"\(([^)]+),([^)]+)\)", value)
        if m:
            return dict(lat=float(m.group(1)), lon=float(m.group(2)))
        else:
            print("bad point representation: %r" % value)
            # raise InterfaceError("bad point representation: %r" % value)

    def AddPoievent(self, eventdescr, eventstart, poiid):
        """
        Add Poievent with given params
        :param eventdescr: eventdescription as string
        :param eventstart: event start as datetime or string
        :param poiid: poi id (from POI table) as int
        :return: poieventid if succesfully added to POIEVENTS table, else None
        """

        if not self.con:
            self.ConnectToDb()
        # INSERT INTO poievents (eventdescription, eventstart, poiid)
        #   VALUES ('K.R.C. Genk - Club Brugge K.V', '2016-04-20 20:30:00+02', 3);
        self.cur.execute("INSERT INTO poievents(eventdescription, eventstart, poiid) VALUES (%s, %s, %s)", (eventdescr, eventstart, poiid))
        result = self.cur.fetchone()
        if result:
            return int(result[0])
        else:
            return None

    def UpdatePoieventProperties(self, poieventid, props):
        """
        Overwrite the properties field in the POIEVENTS table with given props
        :param poieventid: poieventid, as int
        :param props: properties field written to table, as Python dictionary
        :return:
        """
        if not self.con:
            self.ConnectToDb()
        # First check will be done to be sure that the poieventid is existing in the db. If non existing, then update will not be performed.
        # select * from poievents where poieventid=3
        self.cur.execute("select * from poievents where poieventid=%(poieventid)s", {'poieventid': poieventid})
        rows = self.cur.fetchall()
        if rows:
            # UPDATE poievents SET properties='{"setschedule": {"unit": "A1", "timestamp":"26/2"}}' WHERE poieventid=3
            self.cur.execute("UPDATE poievents SET properties=%(prp)s WHERE poieventid=%(poieventid)s", {'prp': props, 'poieventid': poieventid})
            self.con.commit()
        else:
            return "id not found"

    def QueryPoievent(self, poieventid):
        """
        Query poievent based on the provided poieventid
        :param poieventid: unit id
        :return: full unit record as dict ('poieventid', 'eventdescription', 'eventstart', 'properties', 'poiid')
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from poievents where poieventid=%(poievid)s",{'poievid':poieventid})
        event = self.cur.fetchone()
        if not event:
            return None
        else:
            columns = ('poieventid', 'eventdescription', 'eventstart', 'properties', 'poiid')
            return dict(zip(columns, event))

    def QueryPoieventIDByEventdescription(self, poieventdescription):
        """
        Query poieventid based on the provided poieventdescription
        :param poieventdescription: event description as string
        :return: poieventid as int if found, else None
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select poieventid from poievents where eventdescription=%(descr)s",{'descr':poieventdescription})
        result = self.cur.fetchone()
        if not result:
            return None
        else:
            return result[0]

    def QueryFuturePoiEventsForGivenPoi(self, poifriendlyname):
        """
        Query POIEVENTS table to return all future poievents with available capacity for the given poi
        :param poifriendlyname: text field from table POI
        :return: null if negative, else list with [eventdescription, eventstart, availablecapacity]
        """
        if not self.con:
            self.ConnectToDb()

        # test SQL queries succesfully executed from SQL Editor for this method
        # select poievents.eventdescription, poievents.eventstart
        #     from public.poievents, public.poi
        #     where poi.poifriendlyname='R.S.C. Anderlecht' AND poi.poiid=poievents.poiid
        #
        # select poievents.eventdescription, poievents.eventstart
        #     from public.poievents, public.poi
        #     where poi.poifriendlyname='R.S.C. Anderlecht' AND poi.poiid=poievents.poiid AND poievents.eventstart>'2016-05-08 14:30:00+02'
        #     order by poievents.eventstart

        self.cur.execute("select poievents.eventdescription, poievents.eventstart from public.poievents, public.poi where poi.poifriendlyname=%(poifname)s AND poi.poiid=poievents.poiid AND poievents.eventstart>%(start)s order by poievents.eventstart", {'start': timezone(TIMEZONE).localize(datetime.now()),'poifname':poifriendlyname})
        queryresult = self.cur.fetchall()
        result = []
        if queryresult:
            for item in queryresult:
                cap = self.CheckAvailableCapacityForGivenPoiEvent(item[0])
                result.append([item[0], item[1], cap])
        return result

    def CheckAvailableCapacityForGivenPoiEvent(self, eventdescription):
        """
        Check how much available capacity there is for given poievent description
        :param eventdescription: event description
        :return: availableCapacity as int >=0 (0 if none, positive int else)
        """
        if not self.con:
            self.ConnectToDb()
        # SELECT COUNT (schedule.scheduleid) FROM public.schedule, public.poievents, public.status WHERE schedule.poieventid=poievents.poieventid AND poievents.eventdescription='R.S.C. Anderlecht - Test3' AND schedule.statusid=status.statusid and status.status='available'
        self.cur.execute("SELECT COUNT (schedule.scheduleid) FROM public.schedule, public.poievents, public.status WHERE schedule.poieventid=poievents.poieventid AND poievents.eventdescription=%(descr)s AND schedule.statusid=status.statusid and status.status=%(sts)s", {'descr':eventdescription, 'sts': "available"})
        result = self.cur.fetchone()
        if result:
            return int(result[0])
        else:
            return 0

    def QueryPoilatlonForgivenpoieeventdescription(self, eventdescription):
        """
        Query poi latlon for given poievent description
        :param eventdescription: event description
        :return: (lat,lon) of poi
        """
        if not self.con:
            self.ConnectToDb()

        # select poi.center from public.poi, public.poievents where poi.poiid=poievents.poiid AND poievents.eventdescription='R.S.C. Anderlecht - Test3'
        self.cur.execute("select poi.center from public.poi, public.poievents where poi.poiid=poievents.poiid AND poievents.eventdescription=%(poievd)s",{'poievd':eventdescription})
        center = self.cur.fetchone()
        if center:
            return center[0]
        else:
            return None

    def QueryAvailableScheduleForGivenEvent(self, eventdescription):
        """
        Query and return available schedule for given poievent description
        :param eventdescription: event description
        :return: null if negative, [scheduleID, unitid, schedulePricePerTimeUnit, currency, unitaddress, unitdistancetopoi]
        """
        if not self.con:
            self.ConnectToDb()

        # fetch poi center from the given eventdescription
        poilatlongdict = self.QueryPoilatlonForgivenpoieeventdescription(eventdescription)
        if poilatlongdict:
            # select schedule.scheduleid, schedule.unitid, schedule.pricepertimeunit, currency.currency, unit.properties->'fulladdress', round( ( unit.latitudelongitude <@> point('(50.834295,4.298057)') )::numeric * 1.609344, 3) as km from public.schedule,public.status,public.currency,public.poievents, public.unit where schedule.unitid = unit.unitid AND schedule.statusid = status.statusid AND schedule.currencyid = currency.currencyid AND schedule.poieventid = poievents.poieventid AND status.status = 'available' AND schedule.timeunitid = 1 AND poievents.eventdescription = 'R.S.C. Anderlecht - Test3' order by round( ( unit.latitudelongitude <@> point('(50.834295,4.298057)') )::numeric * 1.609344, 3)
            self.cur.execute("select schedule.scheduleid, schedule.unitid, schedule.pricepertimeunit, currency.currency, unit.properties->%(tag)s, round( ( unit.latitudelongitude <@> point(%(lat)s,%(long)s) )::numeric * 1.609344, 3) as unitdistance from public.schedule,public.status,public.currency,public.poievents, public.unit where schedule.unitid = unit.unitid AND schedule.statusid = status.statusid AND schedule.currencyid = currency.currencyid AND schedule.poieventid = poievents.poieventid AND status.status = 'available' AND schedule.timeunitid = 1 AND poievents.eventdescription =%(eventdesc)s order by round( ( unit.latitudelongitude <@> point(%(lat)s,%(long)s) )::numeric * 1.609344, 3)", { 'tag': "fulladdress", 'eventdesc': eventdescription, 'lat': poilatlongdict['lat'], 'long': poilatlongdict['lon'] })
            availableSchedule = self.cur.fetchone()
            if not availableSchedule:
                return None
            else:
                columns = ('scheduleID', 'unitid', 'schedulePricePerTimeUnit', 'currency', 'unitaddress', 'unitdistancetopoi')
                return dict(zip(columns, availableSchedule))
        else:
            return None

    def QueryAvailablePoiEventsWithinGivenAmountofdays(self, startdate, amountofdays, unittest=False):
        """
        Query and return the poievents that will occur within the given amount of days from startdate
        :param startdate: date from within amountdays is calculated, as Python datetime or string, needs to be >= now
        :param amountofdays: number of days as int, needs to be >0
        :return: [] or [poieventid, eventdescription, eventdate, unitid, unitaddress, ownername, ownermail]
        """
        # data validation: it doesn't make sense to look for events in the past
        if not unittest and startdate < (timezone(TIMEZONE).localize(datetime.now()) + timedelta(seconds=-10)) or amountofdays <= 0:
            return []
        else:
            if not self.con:
                self.ConnectToDb()
            start = startdate.date()
            reach = datetime(start.year, start.month, start.day) + timedelta(days=(amountofdays + 1))
            # select poievents.poieventid, poievents.eventdescription, poievents.eventstart, unit.unitid, unit.properties::json -> 'fulladdress', users.fullname, users.email from public.poievents, public.unit, public.users where poievents.eventstart > '2016-06-07 20:00:00+02' AND poievents.eventstart <= '2016-06-13 00:00:00+02' AND unit.poiid = poievents.poiid AND unit.userid = users.userid
            self.cur.execute("select poievents.poieventid, poievents.eventdescription, poievents.eventstart, unit.unitid, unit.properties::json -> 'fulladdress', users.fullname, users.email from public.poievents, public.unit, public.users where poievents.eventstart > %(start)s AND poievents.eventstart <= %(reach)s AND unit.poiid = poievents.poiid AND unit.userid = users.userid ORDER BY unit.friendlyname ASC", {'start': startdate, 'reach': reach})
            rows = self.cur.fetchall()
            if not rows:
                return []
            else:
                columns = ('poieventid', 'eventdescription', 'eventdate', 'unitid', 'unitaddress', 'ownername', 'owneremail')
                results = []
                for row in rows:
                    results.append(dict(zip(columns, row)))
                return results

    def CheckIfUnitHasScheduleForGivenPoieventid(self, unitid, poieventid):
        """
        Check if given unit has an entry in the schedule table for given poieventid
        :param unitid: unitid from UNIT table, as int
        :param poieventid: poieventid from POIEVENTS table, as int
        :return: True if check is positive, false otherwise
        """
        if not self.con:
            self.ConnectToDb()

        # select unitid from schedule where unitid = 1 and poieventid = 6
        self.cur.execute("select unitid from schedule where unitid=%(uid)s and poieventid=%(poievid)s", {'uid': unitid, 'poievid': poieventid})
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return True

    def AddPayment(self, useruuid, ordernr, description, paymentdatetime, amountinclTAX, amountExclTAX, TAXamount, unitid, starttime, endtime):
        # Call this method to add a new payment to the table
        # userid should be provided
        # not possible to include all variables at once, as they are not available yet
        # table name: paymentgwstatus
        # fields  userid integer,ordernr integer,description text,paymentgwref text,status text,
        # paymentdatetime timestamp with time zone, amountinclbtw double precision, invoicelink text, paymentid integer

        if not self.con:
            self.ConnectToDb()

        self.cur.execute("INSERT INTO paymentgwstatus(ordernr, description, paymentdatetime, amountinclbtw, amountexclbtw, btwamount,useruuid, unitid, starttime, endtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(ordernr, description, paymentdatetime, amountinclTAX, amountExclTAX, TAXamount, useruuid, unitid, starttime, endtime))
        self.con.commit()

    #Query payment details for invoice on uuid
    def QueryPaymentDetails(self, ordernr):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select users.email, paymentgwstatus.ordernr, paymentgwstatus.description, paymentgwstatus.amountinclbtw, paymentgwstatus.amountexclbtw, paymentgwstatus.btwamount "
                         "from users,paymentgwstatus "
                         "where paymentgwstatus.useruuid = users.useruuid and "
                         "paymentgwstatus.ordernr = %(onr)s", {'onr':ordernr})
        rows = self.cur.fetchone()
        if rows:
            return rows
        else:
            return "no details found"

    # Update Payment
    def UpdatePaymentStatus(self,ordernr, paymentgwref, status):
        if not self.con:
            self.ConnectToDb()
        #First check will be done to be sure that the userid is existing in the db. If non existing, then update will not be performed.
        self.cur.execute("select * from paymentgwstatus where ordernr=%(onr)s", {'onr': ordernr})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE paymentgwstatus SET status=%(sts)s,paymentgwref=%(pgwref)s WHERE ordernr=%(onr)s", {'sts': status,'pgwref':paymentgwref,'onr':ordernr})
            self.con.commit()
        else:
            return "ordernr doesn't exist, so not possible to update paymentgwstatus"

    def UpdateInvoiceLink(self,ordernr, link):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select * from paymentgwstatus where ordernr=%(onr)s", {'onr': ordernr})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE paymentgwstatus SET invoicelink=%(inlnk)s WHERE ordernr=%(onr)s", {'inlnk': link,'onr':ordernr})
            self.con.commit()
        else:
            return "ordernr doesn't exist, so not possible to update paymentgwstatus"

    def UpdatePaymentDetails(self,paymentdetails,ordernr):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select * from paymentgwstatus where ordernr=%(onr)s", {'onr': ordernr})
        rows = self.cur.fetchall()
        if rows:
            self.cur.execute("UPDATE paymentgwstatus SET properties=%(props)s WHERE ordernr=%(onr)s", {'props': json.dumps(paymentdetails),'onr':ordernr})
            self.con.commit()
        else:
            return "ordernr doesn't exist, so not possible to update paymentgwstatus"

    def GetPaymentStatus(self,ordernr):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select status from paymentgwstatus where ordernr=%(onr)s", {'onr': ordernr})
        rows = self.cur.fetchone()
        if rows:
            return rows
        else:
            return "ordernr doesn't exist, so not possible to get paymentstatus"

    def GetLastInvoiceNumber(self):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select ordernr from paymentgwstatus order by paymentdatetime DESC limit 1")
        rows = self.cur.fetchone()
        if rows:
            return rows
        else:
            return "no details found"

    #Query details of user for invoice
    def QueryInvoiceEmailRecipientAddr(self, email):
        if not self.con:
            self.ConnectToDb()
        self.cur.execute("select fullname, email from users where email = %(em)s", {'em':email})
        rows = self.cur.fetchone()
        if rows:
            return rows
        else:
            return "no details found"

    def QueryScheduleByPaymentOrdernr(self, ordernr):
        """
        ordernr: payment ordernr received by Mollie
        return: [useruuid, starttime, endtime, description, unitid]
        """
        if not self.con:
            self.ConnectToDb()
        # select useruuid, starttime, endtime, description, unitid from paymentgwstatus where ordernr = '1606200007'
        self.cur.execute("select useruuid, starttime, endtime, description, unitid from paymentgwstatus where ordernr = %(onr)s", {'onr': ordernr})
        rows = self.cur.fetchone()
        if rows:
            return rows
        else:
            return "no details found"

    def QueryPayment(self):
        """
        Return full payment table
        """
        if not self.con:
            self.ConnectToDb()

        self.cur.execute("select * from paymentgwstatus")
        rows = self.cur.fetchall()
        if not rows:
            return False
        else:
            return rows

    def DeletePaymentForgivenordernr(self, ordernr):
        """
        Delete Payment record for given ordernr, do nothing if not found
        """
        if not self.con:
            self.ConnectToDb()

        try:
            self.cur.execute("delete from paymentgwstatus where ordernr = %(onr)s", {'onr': ordernr})
            self.con.commit()
            return "Payment record for ordernr %s has been deleted" % ordernr
        except:
            return "Payment record for ordenr %s not found" % ordernr

"""
if __name__ == "__main__":

    dummyJson = {"keyA":"valueKeyA","KeyB":"valueKeyB","keyC":"valueKeyC","KeyD":"valueKeyD"}

    #Creates a new instance of the db_logic class
    mytest = db_logic("Benares","localhost","5432","ParkingPlaza","BENARES")

    #first things first: connect to DB in the beginning
    mytest.ConnectToDb()

    #The following method checks of a user already exits. If true -> already exists, otherwise false -> if false, then go
    #to the function add new user
    returnedval1 = mytest.CheckIfUserAlreadyExists("jeroenmachiels@gmail.com")

    #Adds a new user
    mytest.AddUser("jeroenmachiels@gmail.com","Jeroen Machiels",dummyJson)

    #below functions adds a new owner. If you provide an unknown user mailadres the function will return the following
    # "User doesn't exits in DB, first add as a user before making an owner"
    # if owner has been added ot the db the following is returned: user has been added as owner
    returnedval2 = mytest.AddOwner("jeroenmachiels@gmail.com","063223452",dummyJson)

    #Below functions queries the user based on an email adres
    returnedval2 = mytest.QueryUser("jeroenmachiels@gmail.com")

    #Below functions queries all from users & ownvers table based on email addres
    returnedval2 = mytest.QueryOwnerandUserInfo("jeroenmachiels@gmail.com")

    #Below function will add a POI
    returnedval2 = mytest.AddPoi("RSCA Anderlecht", "Belgium","Anderlecht",dummyJson)

    #Below will query POI table based on poifriendlyname, country, city
    returnedval2 = mytest.GetPoiInfoViaFriendlyName("RSCA Anderlecht")
    returnedval2 = mytest.GetPoiInfoViaCountry("Belgium")
    returnedval2 = mytest.GetPoiInfoViaCity("Anderlecht")

    #Will add a type and query info based on type
    mytest.AddType("GB",dummyJson)
    Returnedval2 = mytest.QueryType("GB")

    #will add a currency and query info based on currency
    mytest.AddCurrency("EUR",dummyJson)
    returnedval2 = mytest.QueryCurrency("EUR")

    #Will add new statusses. Probably only need to add a couple of statusses...
    #currently no check is done if a status already exists before adding
    mytest.AddStatus("Reserved",dummyJson)
    returnedval2 = mytest.QueryStatus("Reserved")

    #Query the different Primary keys needed for adding in subsequent tables
    userid = mytest.QueryUserID("jeroenmachiels@gmail.com")
    ownerid = mytest.QueryOwnerID("jeroenmachiels@gmail.com")
    typeid = mytest.QueryTypeID("GB")
    poiid = mytest.QueryPoiID("RSCA Anderlecht")
    currencyid = mytest.QueryCurrencyID("EUR")
    statusID = mytest.QueryStatusID("Reserved")
    unitID = mytest.QueryUnitId("JeroensBox")

    #add a unit
    #Below function is adding latitudelongitude as a string to a point structure in the DB
    mytest.AddUnit("JeroensBox","51.1906249,5.11601399999995",userid,typeid,poiid,ownerid,dummyJson)

    #Add a Schedule

    mytest.AddSchedule(unitID,ownerid,"2016-01-21T09:00:00.000Z","2016-01-29T11:00:00.000Z","3",currencyid,statusID,userid,dummyJson)

    #Add Event
    mytest.AddEvent("2016-01-21T09:00:00.000Z","db_logic",dummyJson)

    resultunits = mytest.QueryUnitsNearLocationAtPOI("RSCA Anderlecht","51","3")

    resultSchedule = mytest.QueryAvailableScheduleNotFixedPrice(4,'2016-01-21 09:00:00','2016-01-21 11:00:00',"Reserved")

    mytest.DeleteSchedule(3)

    mytest.CloseConnection()
"""