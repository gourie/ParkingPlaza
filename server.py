__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

import adaptEmailTemplate
from apscheduler.schedulers.tornado import TornadoScheduler
from datetime import datetime, timedelta
import db_logic
import emailChecker
import invoice
import iso8601
import json
import Mollie # Payment gateway
from notifyOwner import notifyOwnerToSetSchedule
import os.path
from pytz import timezone
import readdocument
import re   # regex library
import requests  # Python http client
import smtpclient
import sys  # catch CLI arguments
from time import strftime
import tokenize
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.auth
from tornado import locks
from tornado import gen
import utilities
import uuid

# application configuration settings
with open('./config.json', 'r') as file:
    conf = json.loads(file.read())

CONTENTFOLDER = conf['content']
DAYS_TO_EVENT = conf['days-to-event']
EMAILSUBJECT = conf['email-subject']
EMAILSUBJECTUNITPENDING = conf['email-subject-action-required']
HMAC_SECRET = conf['secret']

#invoice specific global settings
INV_COMP_NAME = conf['invoice-companyname']
INV_COMP_STREET = conf['invoice-companystreet']
INV_COMP_NR = conf['invoice-companynumber']
INV_COMP_CITY = conf['invoice-companycity']
INV_COMP_STATE = conf['invoice-companystate']
INV_COMP_COUNTRY = conf['invoice-companycountry']
INV_COMP_POSTAL = conf['invoice-companypostal']
INV_COMP_VATNR = conf['invoice-companyvat']
INV_COMP_TAXRATE = conf['invoice-companytaxrate']
INV_COMP_FOOT = conf['invoice-companyfooter']
INV_COMP_PATH = conf['invoice-companypathtoinvoice']
INV_COMP_PRODNAME = conf['invoice-productname']
INV_COMP_PRECISION = conf['invoice-precision']
INV_SUBJECT_PAYMENTRECEIVED = conf['subject-mail-attachinvoice']
OWNERNOTIFICATION_TIMEBEFOREVENT = conf['ownernotificationtimebeforeevent']
OWNERNOTIFICATION_EMAIL = conf['ownernotification-email']
OWNERNOTIFICATION_EMAIL_SUBJECT = conf['ownernotification-email-subject']
OWNERNOTIFICATION_HOUR = conf['ownernotification-hour']
OWNERNOTIFICATION_MINUTE = conf['ownernotification-minute']
STAT_CALC_HOUR = conf['statistics-calc-hour']
STAT_CALC_MINUTE = conf['statistics-calc-minute']
SUGGESTLOCATION_EMAIL = conf['suggestlocation-email']
SUGGESTLOCATION_EMAIL_SUBJECT = conf['suggestlocation-email-subject']
SUPPORT_EMAIL = conf['support-email']
TIMEZONE = str(conf['timezone'])
TOS_CONTENT = CONTENTFOLDER + conf['tos-doc']

for arg in sys.argv:
    if arg == "prod":
        ENVIRONMENT = 'PROD'
        SERVER_URL = conf['prod-server']
        SERVER_PORT = int(conf['prod-port'])
        HOMEPAGE = "home.min.html"
        MAPPAGE = "map.min.html"
        SCHEDULEPAGE = "schedule.min.html"
        TOSPAGE = "tos.min.html"
        EMAILCONFPAGE = "emailconfirmation.min.html"
        MOLLIE_API_KEY = conf['mollie-prodAPIkey']
        MOLLIE_WEBHOOKURL = conf['mollie-prodwebhookUrl']
        MOLLIE_REDIRECTURL = conf['mollie-prodredirecturl']
        DBINSTANCE = "Benares"
        DBSERVER = conf['prod-dbserver']
        DBPORT = "5432"
        DBUSER = conf['db-user']
        DBPW = conf['db-pw']
        HTTPS_REDIRECT_FLAG = True
    elif arg == "test":
        ENVIRONMENT = 'BETA'
        SERVER_URL = conf['test-server']
        SERVER_PORT = int(conf['test-port'])
        HOMEPAGE = "home.min.html"
        MAPPAGE = "map.min.html"
        SCHEDULEPAGE = "schedule.min.html"
        TOSPAGE = "tos.min.html"
        EMAILCONFPAGE = "emailconfirmation.min.html"
        MOLLIE_API_KEY = conf['mollie-betaAPIkey']
        MOLLIE_WEBHOOKURL = conf['mollie-testwebhookUrl']
        MOLLIE_REDIRECTURL = conf['mollie-testredirecturl']
        DBINSTANCE = "Benares"
        DBSERVER = conf['test-dbserver']
        DBPORT = "5432"
        DBUSER = conf['db-user']
        DBPW = conf['db-pw']
        HTTPS_REDIRECT_FLAG = True
    elif arg == "dev-test":
        ENVIRONMENT = 'DEV'
        SERVER_URL = conf['dev-server']
        SERVER_PORT = int(conf['dev-port'])
        HOMEPAGE = "home.min.html"
        MAPPAGE = "map.min.html"
        SCHEDULEPAGE = "schedule.min.html"
        TOSPAGE = "tos.min.html"
        EMAILCONFPAGE = "emailconfirmation.min.html"
        MOLLIE_API_KEY = conf['mollie-testAPIkey']
        MOLLIE_WEBHOOKURL = conf['mollie-devwebhookUrl']
        MOLLIE_REDIRECTURL = conf['mollie-devredirecturl']
        DBINSTANCE = "Benares"
        DBSERVER = "localhost"
        DBPORT = "5432"
        DBUSER = conf['db-user']
        DBPW = "BENARES"
        HTTPS_REDIRECT_FLAG = False
    else:
        ENVIRONMENT = 'dev'
        SERVER_URL = conf['dev-server']
        SERVER_PORT = int(conf['dev-port'])
        HOMEPAGE = "home.html"
        MAPPAGE = "map.html"
        TOSPAGE = "tos.html"
        SCHEDULEPAGE = "schedule.html"
        TESTPAGE = "testing.html"
        EMAILCONFPAGE = "emailconfirmation.html"
        MOLLIE_API_KEY = conf['mollie-testAPIkey']
        MOLLIE_WEBHOOKURL = conf['mollie-devwebhookUrl']
        MOLLIE_REDIRECTURL = conf['mollie-devredirecturl']
        DBINSTANCE = "Benares"
        DBSERVER = "localhost"
        DBPORT = "5432"
        DBUSER = conf['db-user']
        DBPW = "BENARES"
        HTTPS_REDIRECT_FLAG = False

# Initialize connection to DB
parkingDb = db_logic.db_logic(DBINSTANCE, DBSERVER, DBPORT, DBUSER, DBPW)
parkingDb.ConnectToDb()

# Initialize the smtpclient to enable sending emails to Google SMTP
emailclient = smtpclient.smtpclient(conf['support-email'], conf['support-pw'])
templ = adaptEmailTemplate.adaptEmailTemplate(conf['content'])
emailchecker = emailChecker.emailChecker()
print("emailclient initialized")

readdoc = readdocument.readdocument()
print("readdocument initialized")

#create lock
lock = locks.Lock()

# Initialize token object
tokenizer = tokenize.tokenize(HMAC_SECRET, TIMEZONE)
# Initialize utilities object
pplazautils = utilities.utilities()

# Initialize Invoice object
invoicePDF = invoice.Invoice(INV_COMP_NAME,INV_COMP_STREET,INV_COMP_NR,INV_COMP_CITY,INV_COMP_STATE,INV_COMP_COUNTRY,INV_COMP_POSTAL,INV_COMP_VATNR,INV_COMP_TAXRATE,INV_COMP_FOOT,INV_COMP_PATH,INV_COMP_PRECISION)

#
# Initialize the Mollie API library with your API key.
#
# See: https://www.mollie.nl/beheer/account/profielen/
#
# Initialize Mollie payment gateway
mollie = Mollie.API.Client()
mollie.setApiKey(MOLLIE_API_KEY)

# init ownerNotification object to send emails from 5 days before the event
ownerNotification = notifyOwnerToSetSchedule(SERVER_URL + ":" + str(SERVER_PORT), "/parkings/setSchedule", "email", SUPPORT_EMAIL, CONTENTFOLDER, OWNERNOTIFICATION_EMAIL, OWNERNOTIFICATION_EMAIL_SUBJECT, OWNERNOTIFICATION_TIMEBEFOREVENT, tokenizer, parkingDb)

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# dummy change to force auto-reload upon deploymentt

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', indexHandler),
            (r'/tos', tosHandler),
            (r'/map', MapHandler),
            (r'/schedule', scheduleHandler),
            (r'/paymentwebhook',PaymentWebHookHandler),
            (r'/paymentredirect',PaymentRedirectHandler),
            (r'/auth/google-signup', OAuthGoogleSignupHandler),
            (r'/auth/email-signup', OAuthEmailSignupHandler),
            (r'/auth/google-login', OAuthGoogleLoginHandler),
            (r'/auth/email-login', OAuthEmailLoginHandler),
            (r'/auth/confirm-email', OAuthConfirmEmailHandler),
            (r'/parkings/findAvailableParking', findAvailableParkingAPIHandler),
            (r'/parkings/findAvailableEventParking', findAvailableEventParkingAPIHandler),
            (r'/parkings/reserveParking', reserveParkingAPIHandler),
            (r'/parkings/add', addParkingAPIHandler),
            (r'/parkings/suggestLocation', suggestLocationAPIHandler),
            (r'/parkings/setSchedule', setScheduleAPIHandler),
            (r'/parkings/resetSchedulestate', resetScheduleStateAPIHandler),
            (r'/reservations', reservationsAPIHandler),
            (r'/AccountInfo', AccountInfoAPIHandler),
            (r'/myparkings', myparkingsAPIHandler),
            (r'/health', awshealthAPIHandler),
            (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': './images'}),
            (r'/sitemap/(.*)', tornado.web.StaticFileHandler, {'path': './sitemap'}),
            (r'/fonts/(.*)', tornado.web.StaticFileHandler, {'path': './fonts'})
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=uuid.uuid4().bytes,# OBSELETE: secure cookie not used anymore; generate random UUID object as secret for symmetric signature of cookie and convert to bytes (RFC 4122 python package)
            google_oauth={"key": conf['google-oauth-clientid'],
                          "secret": conf['google-oauth-clientsecret']}
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "server-start", {'environment': arg, 'server-url': SERVER_URL, 'server-port': SERVER_PORT, 'https-redirect-flag': HTTPS_REDIRECT_FLAG, })

        # weird patch for problems with connecting from Tornado on AWS Ubuntu 14.04 using SSL -> only apply to AWSTest environment
        if (arg == "__test__"):
            tornado.httpclient.AsyncHTTPClient.configure(None, defaults=dict(ca_certs="/etc/ssl/certs/ca-certificates.crt"))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_cookie("token")

class indexHandler(BaseHandler):
    '''
    Class to handle HTTP requests for rendering homepage
    '''

    def prepare(self):
        if HTTPS_REDIRECT_FLAG and 'X-Forwarded-Proto' in self.request.headers and self.request.headers['X-Forwarded-Proto'] != 'https':
            print('indexhandler prepare: ', self.request.headers)
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "http-redirect", {'url': self.request.full_url()})
            self.redirect("%s:%d" % (SERVER_URL, SERVER_PORT), permanent=True)

    def get(self):

        configForClient = ""

        # query all Poi's from DB
        poi = parkingDb.GetAllPois()
        poiTypes = parkingDb.GetAllUnitTypes()
        invaliduser = False

        reservationDone = False
        orderFinished = False
        linktodirections = ""
        useragent = "not available"

        try:
            reservationDone = self.get_arguments("reservationstatus")[0]
        except:
            pass

        try:
            ordernb = self.get_arguments("ordernr")[0]
        except:
            pass

        try:
            unitid = parkingDb.QueryScheduleByPaymentOrdernr(ordernb)[4]
            orderFinished = True
            poicenter = parkingDb.QueryPoiCenterByUnitid(unitid)
            center = (poicenter['lat'], poicenter['lon'])
            linktodirections = "https://www.google.be/maps/dir/%s/%s" % (parkingDb.QueryUnitAddress(unitid), center)
        except:
            pass

        try:
            useragent = self.request.headers['user-agent']
        except:
            pass

        # check if user presents a cookie
        if self.get_current_user():

            # check if token is still valid, if not send back to login screen
            if not tokenizer.isValidToken(self.get_current_user()):
                invaliduser = True
                print("token expired")
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "homepage-login-token-failure-expired", {'token': self.get_current_user(), 'user-agent': useragent})
                self.redirect("/auth/google-login")

            # check if user still exists in our DB and the presented
            if not invaliduser and not parkingDb.QueryUserByUserUUID(tokenizer.getClaims(self.get_current_user())['sub']):
                invaliduser = True
                print("trying to login to / with user that no longer exists in our DB")
                configForClient = '{ "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "userprops" : {}' + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "linktodirections" : ' + json.dumps(linktodirections) + ', "loggedin" : "false" }'

                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "homepage-login-token-failure-no-user-in-DB", {'token': self.get_current_user(), 'user-agent': useragent})

            elif not invaliduser:
                id = tokenizer.getClaims(self.get_current_user())['sub']
                # try to get user's email
                try:
                    useremail = parkingDb.QueryEmail(id)
                except:
                    useremail = ""
                # verify whether this user is also an owner
                checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)

                # prepare specific client config for rendering of HOME page
                userprops = {'userName': uMechelen.GetUserDisplayName(id), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}
                configForClient = '{ "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "userprops" : ' + json.dumps(userprops) + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "linktodirections" : ' + json.dumps(linktodirections) + ', "loggedin" : "true" }'

                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-token-homepage-success", {"useruuid": id, "user": userprops, "user-agent": useragent})

        elif orderFinished:
            # redirect from Mollie
            order = parkingDb.QueryScheduleByPaymentOrdernr(ordernb)
            id = order[0]
            destinationstring = parkingDb.QueryPoiFriendlynameByUnitid(order[4])
            description = order[3]
            # try to get user's email
            try:
                useremail = parkingDb.QueryEmail(id)
            except:
                useremail = ""
            # verify whether this user is also an owner
            checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)

            # prepare specific client config for rendering of HOME page
            userprops = {'userName': uMechelen.GetUserDisplayName(id), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}
            configForClient = '{ "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "userprops" : ' + json.dumps(userprops) + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "linktodirections" : ' + json.dumps(linktodirections) + ', "loggedin" : "true" }'
        else:
        # render page without user logged in
            configForClient = '{ "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "userprops" : {}' + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "linktodirections" : ' + json.dumps(linktodirections) + ', "loggedin" : "false" }'
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "homepage-no-user-success", {"user-agent": useragent})

        if not invaliduser:
            self.render(HOMEPAGE, items=configForClient)

class awshealthAPIHandler(BaseHandler):
    """
    Class for AWS health checks
    """
    def get(self):
        print('AWS Health check at timestamp: ', timezone(TIMEZONE).localize(datetime.now()).isoformat())

class tosHandler(BaseHandler):
    """
    class to handle HTTP GET requests for rendering Parking-Plaza Terms of Service
    """

    def get(self):

        poiTypes = parkingDb.GetAllUnitTypes()
        useragent = 'not available'
        try:
            useragent = self.request.headers['user-agent']
        except:
            pass

        if self.get_current_user():
            id = tokenizer.getClaims(self.get_current_user())['sub']
            # try to get user's email
            try:
                useremail = parkingDb.QueryEmail(id)
            except:
                useremail = ""
            # verify whether this user is also an owner
            checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)

            # prepare specific client config for rendering of HOME page
            userprops = {'userName': uMechelen.GetUserDisplayName(id), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}
            loggedIn = "true"
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-token-tospage-success", {"useruuid": id, "user": userprops, "user-agent": useragent})

        else:
            # render page without user logged in
            userprops = {}
            loggedIn = "false"
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "tospage-no-user-success", {"user-agent": useragent})

        parags = readdoc.readParagraph(TOS_CONTENT)
        configForClient = '{ "tos" : ' + json.dumps(parags) + ', "userprops" : ' + json.dumps(userprops) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "loggedin" :' + json.dumps(loggedIn) + ' }'

        self.render(TOSPAGE, title=parags[0], lines=parags[1:], items=configForClient)

class scheduleHandler(BaseHandler):
    """
    class to handle HTTP requests for /schedule
    Arguments: GET (none, setscheduletoken) & POST  (unit)
    """

    def get(self):
        """
        Return the schedule for setscheduletoken provided
        If no setscheduletoken provided, return the unit found in db based on uuid (in cookie)
        """

        configForClient = ""
        invaliduser = False
        filter = {"type":"schedule"}
        results = []
        useragent = 'not available'
        try:
            useragent = self.request.headers['user-agent']
        except:
            pass

        # query all Poi's from DB
        poi = parkingDb.GetAllPois()
        poiTypes = parkingDb.GetAllUnitTypes()

        # check if user presents a cookie
        if self.get_current_user():

            # check if token is still valid, if not send back to login screen
            if not tokenizer.isValidToken(self.get_current_user()):
                invaliduser = True
                print("token expired")
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "schedulepage-login-token-failure-expired", {'useruuid': self.get_current_user(), "user-agent": useragent})
                self.redirect("/auth/google-login")

            # check if user still exists in our DB and the presented
            if not invaliduser and not parkingDb.QueryUserByUserUUID(tokenizer.getClaims(self.get_current_user())['sub']):
                invaliduser = True
                # TODO: implement logging
                print("trying to login to / with user that no longer exists in our DB")
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "schedulepage-login-token-failure-no-user-in-DB", {'useruuid': tokenizer.getClaims(self.get_current_user())['sub'], "user-agent": useragent})

            elif not invaliduser:
                uuid = tokenizer.getClaims(self.get_current_user())['sub']
                # try to get user's email
                try:
                    useremail = parkingDb.QueryEmail(uuid)
                except:
                    useremail = ""
                # verify whether this user is also an owner
                checkOwnerId = parkingDb.QueryOwnerIDWithUUID(uuid)
                userprops = {'userName': uMechelen.GetUserDisplayName(uuid), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}

                # if owner: try fetching results from arguments (redirect from setScheduleAPIHandler)
                # dummy variable to adapt function argument to the arguments provided with the API call (3 mutually exclusive options: none, setscheduletoken or unit)
                arg1 = ""
                arg2 = ""
                unitaddress = ""
                if checkOwnerId != 0:
                    try:
                        # check if valid 'setscheduletoken' argument has been provided (that holds unitid and eventdescription -coming from setScheduleAPIHandler)
                        if tokenizer.isValidToken(self.get_arguments('setscheduletoken')[0]):
                            arg1 = tokenizer.getClaims(self.get_arguments('setscheduletoken')[0])['unitname']
                            arg2 = tokenizer.getClaims(self.get_arguments('setscheduletoken')[0])['eventdescription']
                    except:
                        # not 'schedulesettoken' provided' => check if valid 'unit' argument has been provided
                        try:
                            if self.get_arguments('unit')[0]:
                                myunits = parkingDb.QueryUnitsByUserUUID(uuid)
                                # check if 'unit' argument has been provided (API call from client)
                                for unit in myunits:
                                    if self.get_arguments('unit')[0] == unit['unitname']:
                                        arg1 = self.get_arguments('unit')[0]
                                if arg1 == "":
                                    # none found => unit provided doesn't belong to this user so return his first unit as found in our DB
                                    # TODO: extend to return list and allow to adapt screen based on unit (dropdown)
                                    arg1 = myunits[0]
                        except:
                            # no 'unit' provided as argument so move ahead => read from DB by finding first unitname associated with the user (from uuid in cookie)
                            arg1 = parkingDb.QueryUnitsByUserUUID(uuid)[0]['unitname']
                    results = pplazautils.prepSchedulesListForParkingListApp(parkingDb.QueryFutureSchedulesbyUnitname(arg1), arg2)
                    unitaddress = parkingDb.QueryUnitAddressByUnitname(arg1)
                configForClient = '{ "filter" : ' + json.dumps(filter) + ', "schedules" : ' + json.dumps(results) + ', "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "unitaddress" : ' + json.dumps(unitaddress) + ', "userprops" : ' + json.dumps(userprops) + ', "loggedin" : "true" }'

                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-token-schedulepage-success", {"useruuid": uuid, "user": userprops, "user-agent": useragent})

        else:
        # render page without user logged in
            configForClient = '{ "filter" : ' + json.dumps(filter) + ', "schedules" : ' + json.dumps(results) + ', "poi" : ' + json.dumps(poi) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "userprops" : {}' + ', "loggedin" : "false" }'

        if not invaliduser:
            self.render(SCHEDULEPAGE, items=configForClient)


    def post(self):
        """
        Return the schedule for given unit argument
        If none provided, return the unit found in db based on uuid (in cookie)
        If unit provided doesn't belong to the user, return unit found in db based on uuid (in cookie)
        """

        invaliduser = False
        results = []

        # check if user presents a cookie
        if self.get_current_user():

            # check if token is still valid, if not send back to login screen
            if not tokenizer.isValidToken(self.get_current_user()):
                invaliduser = True
                print("token expired")
                self.redirect("/auth/google-login")

            # check if user still exists in our DB and the presented
            if not invaliduser and not parkingDb.QueryUserByUserUUID(tokenizer.getClaims(self.get_current_user())['sub']):
                invaliduser = True
                # TODO: implement logging
                print("trying to login to / with user that no longer exists in our DB")
                self.write(json.dumps(""))

            elif not invaliduser:
                uuid = tokenizer.getClaims(self.get_current_user())['sub']

                if parkingDb.QueryOwnerIDWithUUID(uuid) != 0:
                    myunits = parkingDb.QueryUnitsByUserUUID(uuid)
                    arg1 = ""
                    try:
                        # check if 'unit' argument has been provided (API call from client)
                        for unit in myunits:
                            if self.get_arguments('unit')[0] == unit['unitname']:
                                arg1 = self.get_arguments('unit')[0]
                        if arg1 == "":
                            # none found => unit provided doesn't belong to this user so return his first unit as found in our DB
                            # TODO: extend to return list and allow to adapt screen based on unit (dropdown)
                            arg1 = myunits[0]
                    except:
                        # no argument provided => read from DB by finding --one/first-- unitname associated with the user (from uuid in cookie)
                        # TODO: extend to return list and allow to adapt screen based on unit (dropdown)
                        arg1 = myunits[0]
                    results = pplazautils.prepSchedulesListForParkingListApp(parkingDb.QueryFutureSchedulesbyUnitname(arg1))

                self.write(json.dumps(results))


class MapHandler(BaseHandler):
    """
    Class to handle HTTP requests for rendering parking map for Renter Reservation
    """

    def get(self):

        configForClient = ""
        destinationstring = "Tell us where you want to go"
        reservationDone = False
        orderFinished = False
        ordernb = ""

        try:
            destinationstring = self.get_arguments("destination")[0]  # this method returns a list!!
        except:
            pass
            print("except thrown in GET /map with arguments")

        try:
            reservationDone = self.get_arguments("reservationstatus")[0]
        except:
            pass

        try:
            ordernb = self.get_arguments("ordernr")[0]
            orderFinished = True
        except:
            pass

        # query all Poi's from DB
        poi = parkingDb.GetAllPois()
        poiTypes = parkingDb.GetAllUnitTypes()
        invaliduser = False

        inp = parkingDb.QueryFuturePoiEventsForGivenPoi(destinationstring)
        eventlist = pplazautils.prepListOfEventsForMap(inp)

        # check if user presents a cookie
        if self.get_current_user():

            # check if token is still valid, if not send back to login screen
            if not tokenizer.isValidToken(self.get_current_user()):
                invaliduser = True
                print("token expired")
                self.redirect("/auth/google-login")

            # check if user still exists in our DB and the presented
            if not invaliduser and not parkingDb.QueryUserByUserUUID(tokenizer.getClaims(self.get_current_user())['sub']):
                invaliduser = True
                print("trying to login to /map with user that no longer exists in our DB")
                self.redirect("/auth/google-login")
                # configForClient = '{ "poi" : ' + json.dumps(poi) + ', "initialPoi" : ' + json.dumps(destinationstring) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "events" : ' + json.dumps(eventlist) + ', "userprops" : {}' + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "loggedin" : "false" }'

            elif not invaliduser:
                id = tokenizer.getClaims(self.get_current_user())['sub']
                # try to get user's email
                try:
                    useremail = parkingDb.QueryEmail(id)
                except:
                    useremail = ""
                # verify whether this user is also an owner
                checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)

                # prepare specific client config for rendering of HOME page
                userprops = {'userName': uMechelen.GetUserDisplayName(id), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}
                configForClient = '{ "poi" : ' + json.dumps(poi) + ', "initialPoi" : ' + json.dumps(destinationstring) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "events" : ' + json.dumps(eventlist) + ', "userprops" : ' + json.dumps(userprops) + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "loggedin" : "true" }'
        elif orderFinished:
            # redirect from Mollie
            order = parkingDb.QueryScheduleByPaymentOrdernr(ordernb)
            id = order[0]
            destinationstring = parkingDb.QueryPoiFriendlynameByUnitid(order[4])
            description = order[3]
            # try to get user's email
            try:
                useremail = parkingDb.QueryEmail(id)
            except:
                useremail = ""
            # verify whether this user is also an owner
            checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)

            # prepare specific client config for rendering of HOME page
            userprops = {'userName': uMechelen.GetUserDisplayName(id), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': useremail}
            configForClient = '{ "poi" : ' + json.dumps(poi) + ', "initialPoi" : ' + json.dumps(destinationstring) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "events" : ' + json.dumps(eventlist) + ', "userprops" : ' + json.dumps(userprops) + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "loggedin" : "true" }'
        else:
        # Design change: prompt user to login
            invaliduser = True
            self.redirect("/auth/google-login")
            # configForClient = '{ "poi" : ' + json.dumps(poi) + ', "initialPoi" : ' + json.dumps(destinationstring) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "events" : ' + json.dumps(eventlist) + ', "userprops" : {}' + ', "reservationstatus" : ' + json.dumps(reservationDone) + ', "loggedin" : "false" }'

        if not invaliduser:
            self.render(MAPPAGE, items=configForClient)


class AccountInfoAPIHandler(BaseHandler):
    """
    Class AccountInfoAPIHandler
    Returns reservations Collection
    """
    def get(self, *args, **kwargs):
        # API security: check user id
        if self.get_current_user():
            print("in GET /AccountInfo, user: ", self.get_current_user())

            try:
                uuid = tokenizer.getClaims(self.get_current_user())['sub']
                usr = parkingDb.QueryUserByUserUUID(uuid)
                # prep format for HeaderApp
                usrresult = pplazautils.prepListOfTuplesAccountInfoUser(usr)
                own = parkingDb.QueryOwnerandUserInfo(usrresult['email'])
                if(own):
                    ownerresult = pplazautils.prepListOfTuplesAccountInfoOwner(own)
                    self.write(json.dumps(ownerresult))
                else:
                    self.write(json.dumps(usrresult))
            except:
                # TODO: implement logging
                print('something went wrong in GET /AccountInfo with API call from: ', self.get_current_user(), 'timestamp: ',
                      timezone(TIMEZONE).localize(datetime.now()).isoformat())
                self.write(json.dumps("failure"))

        else:
            # If no user, redirect to log-in
            self.redirect("/auth/google-login")

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


class findAvailableEventParkingAPIHandler(BaseHandler):
    """
    Class to retrieve eventlist for given POIfriendlyname
    """

    def post(self):

        poifname = ""
        try:
            poifname = self.get_arguments("poifname")[0]  # this method returns a list!!
        except:
            print("except thrown in POST /map with arguments")

        inp = parkingDb.QueryFuturePoiEventsForGivenPoi(poifname)
        eventlist = pplazautils.prepListOfEventsForMap(inp)
        self.write(json.dumps(eventlist))


class OAuthEmailSignupHandler(BaseHandler):
    '''
    Class to sign up a new user with email address
    '''

    def post(self):

        print("in POST /auth/email-signup, arguments: ", self.request.body)
        emailAdd = self.get_argument("email")

        try:
            # 0- verify if valid email address has been provided
            if not emailchecker.verifyEmailFormat(emailAdd):
                self.write(json.dumps("invalid email"))
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email-failed", {'email-address': emailAdd, 'error': "invalid email"})

            else:
                # valid email addr so continue
                # 1- check if user exists already in DB
                if not parkingDb.CheckIfUserAlreadyExists(emailAdd):
                    # 2- new user: write to DB
                    checkTimestamp = timezone(TIMEZONE).localize(datetime.now()).isoformat()
                    uid = uMechelen.generateUserID()
                    # change #28:delayed till email confirmation!!!
                    # token = ''
                    # 6/9: rolled back to / to allow integration of email-signup into becomeowner!!!
                    token = tokenizer.createUUIDToken(uid)
                    self.set_cookie("token", token, expires_days=7)
                    user = {'token': token, 'password': self.get_arguments("password")[0], 'birthdate': self.get_arguments("birthdate")[0], 'toscheckdone': checkTimestamp}

                    parkingDb.AddUser(emailAdd, self.get_argument("firstname") + " " + self.get_argument("lastname"), uid, user)

                    # 4- sent back data for updating UI
                    # change #28: delayed till email confirmation!!!
                    # 6/9: rolled back to / to allow integration of email-signup into becomeowner!!!
                    checkOwnerId = parkingDb.QueryOwnerIDWithUUID(uid)
                    userprops = {'userName': uMechelen.GetUserDisplayName(uid), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': self.get_argument("email")}
                    # userprops = ""
                    self.write(json.dumps(userprops))

                    # send email with verification link (JWT since #28) that needs to be clicked before activation
                    emailconftoken = tokenizer.createEmailConfirmationToken(emailAdd)
                    link = "%s:%d/auth/confirm-email?confirmationtoken=%s" % (SERVER_URL, SERVER_PORT, emailconftoken)
                    user = parkingDb.QueryUserByUserUUID(uid)
                    user[3]['confirmation-token'] = emailconftoken
                    user[3]['email-confirmation'] = "pending"
                    parkingDb.UpdateUserPropsBasedOnUserUUID(uid, user[3])

                    templ.adaptUserEmailConfirmationTemplate(emailAdd, self.get_argument("firstname"), link)
                    emailclient.sendEmail([emailAdd], './userEmailConfirmation', conf['support-email'], EMAILSUBJECT)

                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email", {'user': user})
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-accepted-tos", {'user': user, 'trigger': "signup"})

                else:
                    # user exists already: move to loggedIn screen
                    uid = parkingDb.queryUUID(self.get_argument("email"))
                    checkOwnerId = parkingDb.QueryOwnerIDWithUUID(uid)
                    userprops = {'userName': uMechelen.GetUserDisplayName(uid), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': self.get_argument("email")}
                    self.write(json.dumps(userprops))
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email-error", {'user': userprops, 'error': "user already exists - automatically logged in user"})

        except:
            # TODO: implement logging
            print('something went wrong with POST /auth/email-signup: ', self.get_argument("email"), 'timestamp: ',
                  timezone(TIMEZONE).localize(datetime.now()).isoformat())
            self.write(json.dumps("not allowed"))


class OAuthConfirmEmailHandler(BaseHandler):
    """
    Class to handle email confirmations (triggered after sign-up by email)
    """

    def get(self):

        poiTypes = parkingDb.GetAllUnitTypes()
        useragent = 'not available'
        try:
            useragent = self.request.headers['user-agent']
        except:
            pass

        emailconfirmation = dict(status=False)

        # 1- unpack token to find user and fetch emailaddress
        # check if valid 'token' argument has been provided (coming from OAuthEmailSignupHandler)
        if tokenizer.isValidToken(self.get_arguments('confirmationtoken')[0]):
            emailAdd = tokenizer.getClaims(self.get_arguments('confirmationtoken')[0])['emailaddress']
            user = parkingDb.QueryUser(emailAdd)
            emailconfirmation['email'] = emailAdd

            # 2- check if confirmation token matches the one generated for this user and the email-confirmation hasn't been done yet
            if parkingDb.QueryUserPropertiesForEmailconfirmationWithGivenuseridandtoken(user[0], self.get_arguments('confirmationtoken')[0]) == 'pending':
                # generate token, update user record, send COOKIE to browser
                uid = user[4]
                # 6/9: rolled back to / to allow integration of email-signup into becomeowner!!!
                # token = tokenizer.createUUIDToken(uid)
                # send cookie to browser
                # self.set_cookie("token", token, expires_days=7)

                # update user record in DB
                emailconfirmation['status'] = True
                user[3]['email-confirmation'] = timezone(TIMEZONE).localize(datetime.now()).isoformat()
                # 6/9: rolled back to / to allow integration of email-signup into becomeowner!!!
                # user[3]['token'] = token
                parkingDb.UpdateUserPropsBasedOnUserUUID(user[4], user[3])

                # verify whether this user is also an owner
                checkOwnerId = parkingDb.QueryOwnerIDWithUUID(uid)
                userprops = {'userName': uMechelen.GetUserDisplayName(uid), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': emailAdd}
                configForClient = '{ "userprops" : ' + json.dumps(userprops) + ', "emailconf" : ' + json.dumps(emailconfirmation) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "loggedin" : "true" }'

            else:   # confirmation code does not match or user has already tried to confirm >> present empty user screen and prompt to redo sign up
                    configForClient = '{ "userprops" : {}' + ', "emailconf" : ' + json.dumps(emailconfirmation) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "loggedin" : "false" }'
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email-confirmation-failed", {'error-code': "token doesn't match for user", 'user': user, 'token': self.get_arguments('confirmationtoken')[0], "user-agent": useragent})

        else:   # token expired >> present empty user screen and prompt to redo sign up
            configForClient = '{ "userprops" : {}' + ', "emailconf" : ' + json.dumps(emailconfirmation) + ', "poitypes" : ' + json.dumps(poiTypes) + ', "loggedin" : "false" }'
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email-confirmation-failed", {'error-code': "invalid token", 'token': self.get_arguments('confirmationtoken')[0], "user-agent": useragent})

        # 3- render page
        self.render(EMAILCONFPAGE, items=configForClient)

        # 4- send email if confirmation email successful
        if emailconfirmation['status']:
            # send welcome email to user
            templ.adaptNewUserEmailTemplate(emailAdd, user[1])
            emailclient.sendEmail([emailAdd], './newUser', conf['support-email'], EMAILSUBJECT)
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-email-confirmation-success", {'user': user, "user-agent": useragent})


class OAuthGoogleSignupHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    '''
    Class to sign up a new user using OAuth2.0 to Google API
    '''

    @tornado.gen.coroutine
    def get(self):
        redirect_uri = "%s:%d/auth/google-signup" % (SERVER_URL, SERVER_PORT)

        if self.get_argument("code", False):
            credentials = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument("code"))

            # 1- try to add user to DB (including sending welcome email)
            token = uMechelen.AddGoogleUser(credentials)

            # 2- if user added successfully -> token is returned, cookie created and redirect to HOME
            if token:
                #TODO: add token validity check?
                self.set_cookie("token", token, expires_days=31)
                self.redirect("/")
            # else False is returned and redirect to LOGIN
            else:
                self.redirect("/auth/google-login")

        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings["google_oauth"]["key"],
                scope=["profile", "email"],
                response_type="code")


class OAuthEmailLoginHandler(BaseHandler):
    '''
    Class to log in an existing user with email address
    '''

    def post(self):

        # 1- find out which user this is in our DB (assert: it is a user in our DB, if not --> redirect to signup)
        uid = parkingDb.queryUUID(self.get_argument("email"))

        # 2- if uid is returned (user has been found): recreate TOKEN, create cookie and redirect to HOME
        if uid:
            # 2- verify if the password provided matches our DB
            checkpw = parkingDb.VerifyUserPassword(uid, self.get_argument("password"))

            if checkpw == "no password":
                # this user signed up without PW (Google Account)
                self.write(json.dumps("no password"))
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-email-failure", {'error': "Google user, no PW provided", "useruuid": uid, "user-email": self.get_argument("email")})
            elif checkpw:
                # 3- create a new JWT token with exp claim, put this inside a cookie and refresh user record
                token = tokenizer.createUUIDToken(uid)
                self.set_cookie("token", token, expires_days=31)
                uMechelen.RefreshUser(uid, token)

                # 4- redirect to home page
                checkOwnerId = parkingDb.QueryOwnerIDWithUUID(uid)
                userprops = {'userName': uMechelen.GetUserDisplayName(uid), 'ownerYesNo': (checkOwnerId != 0), 'userEmail': self.get_argument("email")}
                self.write(json.dumps(userprops))
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-email-success", {"useruuid": uid, "user": userprops})
            else:
                # incorrect pw: prompt for re-entry
                self.write(json.dumps("incorrect password"))
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-email-failure", {'error': "Wrong password", "useruuid": uid, "user-email": self.get_argument("email")})

        else:
            # incorrect user: prompt for re-entry
            self.write(json.dumps("incorrect email"))
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-email-failure", {'error': "Wrong email", "useruuid": uid, "user-email": self.get_argument("email")})


class OAuthGoogleLoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    '''
    Class to log in an existing user using OAuth2.0 to Google API
    '''

    @tornado.gen.coroutine
    def get(self):

        #TODO: add try - except with assert: not self.get_current_user() --> you expect that we don't have a cookie so need a new login here!!!!

        # pretty heavy implementation: fetch new Google data at every login (this could be scheduled once every x weeks or months)
        redirect_uri = "%s:%d/auth/google-login" % (SERVER_URL, SERVER_PORT)
        #redirect_uri = "http://localhost:%d/auth/google-login" % options.port
        if self.get_argument("code", False):
            credentials = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument("code"))

            # 1- find out which user this is in our DB (assert: it is a user in our DB, if not --> redirect to signup)
            uid = uMechelen.FindUserUUIDBasedOnGoogleCredentials(credentials)

            # 2- if uid is returned (user has been found): recreate TOKEN, create cookie and redirect to HOME
            if uid:
                # 2- create a new JWT token with exp claim, put this inside a cookie and refresh user record
                token = tokenizer.createUUIDToken(uid)
                self.set_cookie("token", token, expires_days=31)
                uMechelen.RefreshUser(uid, token)
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-login-google-success", {"useruuid": uid, "google-credentials": credentials})

                # 3- redirect to home page
                try:
                    host = self.request.headers._dict['Host']
                    referer = self.request.headers._dict['Referer']
                    refurl = re.split(host, referer)[1]
                    if (refurl[1:4] == 'map'):
                        self.redirect(refurl)
                    else:
                        self.redirect("/")
                except:
                    self.redirect("/")

            else:
                # redirect to sign-up (not a known user yet in our DB)
                self.redirect("/auth/google-signup")

        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings["google_oauth"]["key"],
                scope=["profile", "email"],
                response_type="code")


class users:
    '''
    Class containing all users (temp, no child classes yet for renter/owner etc)
    @params:
        credentials
        displayName: display name
        email: email address
        name: {givenName, surName}
        gender: gender
        language: language
    '''

    def __init__(self):
        '''Constructor to load users from the 'temp DB' into memory
        :return: none 
        '''

        #print('init users')

    def AddGoogleUser(self, credentials):
        '''
        Add user with given user credentials
        :credentials: dictionary with expected keys credentials, displayName, email, name, gender, language
        :return: JWT token for user if success, false if user already exists
        '''

        # 1 - fetch user data from Google API
        user = self.fetchUserDataFromAPI(credentials)

        # 2 - add user to DB
        if not parkingDb.CheckIfUserAlreadyExists(user['emails'][0]['value']):
            uid = uMechelen.generateUserID()
            token = tokenizer.createUUIDToken(uid)
            user['token'] = token
            user['toscheckdone'] = timezone(TIMEZONE).localize(datetime.now()).isoformat()
            parkingDb.AddUser(user['emails'][0]['value'], user['displayName'], uid, user)
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-signup-google", {'user': user})
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "user-accepted-tos", {'user': user, 'trigger': "signup"})
            # send welcome email to user
            templ.adaptNewUserEmailTemplate(user['emails'][0]['value'], user['displayName'])
            emailclient.sendEmail([user['emails'][0]['value']], './newUser', conf['support-email'], EMAILSUBJECT)
            return token
        else:
            return False


    def GetUserDisplayName(self, uid):
        """
        Return DisplayName for user with given uid
        :param: uid is the user's uuid set at time of creation
        :return: user's DisplayName as registered in our DB
        """

        return parkingDb.QueryFullname(uid)


    def FindUserUUIDBasedOnGoogleCredentials(self, credentials):
        """
        Find user in our DB based on Google Credentials
        :param credentials: Google Credentials (email, displayname,...)
        :return: user's UUID as found in DB; false if user has not been found
        """
        user = self.fetchUserDataFromAPI(credentials)
        if parkingDb.CheckIfUserAlreadyExists(user['emails'][0]['value']):
            return parkingDb.queryUUID(user['emails'][0]['value'])
        else:
            return False


    def RefreshUser(self, uid, token):
        """
        Refresh JWT token of user with given uid
        :param: uid, token
        :return: users list updated + user record updated in temp DB
        """

        user = parkingDb.QueryUserByUserUUID(uid)
        user[3]['token'] = token
        parkingDb.UpdateUserBasedOnUserUUID(user[2], user[1], user[4], user[3])


    def fetchUserDataFromAPI(self, credentials):
        '''
        Call Google API to fetch user data with provided credentials
        :param: credentials: dictionary with expected keys credentials, displayName, email, name, gender, language(TBD
        :return: empty string if credentials expired; users list updated  ---TEMP: should write to DB
        '''

        # test: do something with access token and get Google+ user data
        if bool(credentials):
            # print("in if loop, credentials are: ", credentials)
            if credentials['expires_in'] <= 0:
                # TODO: implement logging
                print('credentials expired: ', credentials, 'timestamp: ',
                      timezone(TIMEZONE).localize(datetime.now()).isoformat())
            else:
                headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
                req_uri = 'https://www.googleapis.com/plus/v1/people/me'
                r = requests.get(req_uri, headers=headers)
                return r.json()

    def generateUserID(self):
        '''
        Return Unique User ID
        '''
        return str(uuid.uuid4())  # RFC 4122


class schedule:
    '''
    Class schedule
    @params:
        availableParkingUnits: parking units active in the given schedule with their {id} and position in {lat, lon}
        startTime: start time of parking requested by user
        endTime: end time of parking requested by user
    '''

    def __init__(self):
        """Constructor to load available parking units from the 'temp DB' into memory
        :return: none
        """
        #print('in init schedule')


    def findAvailableParkingUnit(self, destination, timeslot, userID, poifname):
        """Return the nearest available parking unit
        :destination: dictionary object with lat, lon arguments of the destination (where renter wants to go)
        :timeslot: dictionary object with startTime, endTime arguments of desired time slot (when renter wants to go); both in UTC 8601 objects
        :id: user ID
        :poifname: poifriendlyname
        :return: nearest available parking unit with friendlyName, latitudelongitude and pricepertimeunit
        """
        try:
            # catch 'timeslot is not a dictionary error'
            if (type(timeslot) != dict):
                raise TypeError("Timeslot is not a dictionary")

            # catch 'timeslot has wrong dictionary keys'
            if (list(timeslot.keys()) != ['endTime', 'startTime']):
                raise ValueError("Timeslot doesn't have the keys startTime and endTime")

            # catch invalid timeslot start>=end
            if (timeslot['startTime'] >= timeslot['endTime']):
                raise ValueError("Not a valid timeslot: start must < end!")

            listOfUnits = parkingDb.QueryUnitsNearLocationAtPOI(poifname, destination['lat'], destination['lon'])

            timedifference = pplazautils.convert_timedelta(timeslot['endTime'] - timeslot['startTime'])

            nearestAvailableUnit = {}
            for i in range(len(listOfUnits)):
                sch = parkingDb.QueryAvailableScheduleNotFixedPrice(listOfUnits[i][2], timeslot['startTime'], timeslot['endTime'], "available")
                if sch:
                    nearestAvailableUnit['id'] = listOfUnits[i][0]
                    nearestAvailableUnit['price'] = str(timedifference['hours'] * sch[3]) + " " + sch[4]
                    nearestAvailableUnit['lat'] = listOfUnits[i][1]['lat']
                    nearestAvailableUnit['lon'] = listOfUnits[i][1]['lon']

                    # call splitSchedule(scheduleID, timeslot, userID) to break schedule into pieces
                    self.splitScheduleID(sch[0], timeslot, userID)

                    return nearestAvailableUnit
                else:
                    pass

        except (TypeError, ValueError, KeyError), e:
            # send errors to logging later
            # print("server.py/schedule/findAvailableParkingUnit: ", e)
            pass


    def splitScheduleID(self, scheduleID, timeslot, uuid):
        """
        Set status of given schedule id to processing by splitting existing schedule ID into multiple slots
        :param scheduleID: scheduleID that needs to be split
        :param timeslot: dictionary {startTime,endtime} of slot to be set
        :param uuid: user uuid from cookie
        :return: none, schedule in-memory object changed (db not changed)
        """
        userID = parkingDb.QueryUserIDByUUID(uuid)
        #:return: null if negative, [unitid,ownerid,startdatetime,enddatetime,pricepertimeunit,timeunitid,currencyid,statusid,userid,properties,scheduleid,poieventid]
        schedule = parkingDb.QuerySchedule(scheduleID)
        availableStatusID = parkingDb.QueryStatusID('available')
        processingStatusID = parkingDb.QueryStatusID('processing')

        # Check if timeslot[start] == scheduleStartTime (no new slot possible before)
        if (schedule[2] == timeslot['startTime']):
            # 1- Convert existing schedule id to Status
            parkingDb.UpdateSchedule(scheduleID, schedule[2], timeslot["endTime"], processingStatusID, userID)

        else: #there is a new slot (oldStart, Timeslot[start]) before => set to available
            # 1- Convert existing schedule id to slot before and set to available
            parkingDb.UpdateSchedule(scheduleID, schedule[2], timeslot["startTime"], availableStatusID, "")

            # 2- Create new schedule entry and set given slot to given status
            # AddSchedule(self, unitid, ownerid, startdatetime, enddatetime, pricepertimeunit, timeunitid, currencyid, statusid, userid, poieventid, properties):
            parkingDb.AddSchedule(schedule[0], schedule[1], timeslot["startTime"], timeslot["endTime"], schedule[4], schedule[5], schedule[6], processingStatusID, userID, schedule[11], schedule[8])

        # Check if timeslot[end] == self.activeParkingUnits[i]['endTime'] ()
        if (schedule[3] != timeslot['endTime']):
            # 3- Create new schedule record and set after end to Available
            parkingDb.AddSchedule(schedule[0], schedule[1], timeslot["endTime"], schedule[3], schedule[4], schedule[5], schedule[6], availableStatusID, "", schedule[11], schedule[8])

        else: # no new slot possible after => do nothing
            pass

class findAvailableParkingAPIHandler(BaseHandler):
    """
    Class findAvailableParkingAPIHandler
    Returns json file with available Parking Slot ('id', 'parkingprice', location{lat,lon})
    """

    def post(self, *args, **kwargs):

        # API security: check user id
        if self.get_current_user():
            # 1- check if valid user
            # STUB: e.g. catch exceptions such as not paid last invoice, ...

            print("in POST /parkings/findAvailableParking, arguments: ", self.request.body)

            # TODO: write unit-test for this API endpoint and test for exception cases (e.g. invalid params)
            if self.get_arguments("eventdescription"):
                # event-parking
                result = ""
                event = {'eventdescription': self.get_arguments("eventdescription")[0], 'eventstart': self.get_arguments("eventstart")[0]}
                sch = parkingDb.QueryAvailableScheduleForGivenEvent(event['eventdescription'])
                if sch: # catch sch=None (e.g. wrong/false eventdescription)
                    processingStatusID = parkingDb.QueryStatusID('processing')
                    result = parkingDb.UpdateEventSchedule(sch['scheduleID'], processingStatusID, parkingDb.QueryUserIDByUUID(tokenizer.getClaims(self.get_current_user())['sub']))
                if result:
                    availableUnit = {'id': parkingDb.QueryUnitFriendlyName(sch['unitid']),
                                     'price': str(sch['schedulePricePerTimeUnit']) + " " + sch['currency'],
                                     'address': sch['unitaddress'],
                                     'distance': str(sch['unitdistancetopoi'])}
                    self.write(json.dumps(availableUnit))
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "renter-find-parking-success", {'useruuid': tokenizer.getClaims(self.get_current_user())['sub'], 'event': event, 'schedule': sch, 'unit-returned': availableUnit})
                else:
                    self.write(json.dumps("invalid"))
            else:
                # city-parking
                # fetch URI arguments from GET requests
                destination = {}
                destination['lat'] = self.get_arguments("lat")[0]  # this method returns a list!!
                destination['lon'] = self.get_arguments("lon")[0]
                timeslotInput = {}
                timeslotInput["startTime"] = self.get_arguments("startTime")[0]
                timeslotInput["endTime"] = self.get_arguments("endTime")[0]
                # convert input Timestamp from ISO8601 UTC (unicode string) to Python datetimeobject
                timeslot = {}
                timeslot['startTime'] = iso8601.parse_date(timeslotInput["startTime"])
                timeslot['endTime'] = iso8601.parse_date(timeslotInput["endTime"])

                self.write(json.dumps(sMechelen.findAvailableParkingUnit(destination, timeslot, tokenizer.getClaims(self.get_current_user())['sub'], self.get_arguments("poi")[0])))

        else:
            # TODO: implement logging
            print(
            'invalid POST request to /parkings/findAvailableParking, timestamp: ', timezone(TIMEZONE).localize(datetime.now()).isoformat())
            self.write(json.dumps("no user"))

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


class resetScheduleStateAPIHandler(BaseHandler):
    """
    Reset the schedule state of the schedule posted by the user -- UI async actions to alert when user has aborted the reservation workflow
    """

    def post(self, *args, **kwargs):

        print("in POST /parkings/resetSchedulestate, arguments: ", self.request.body)

        # API security: check user id
        if self.get_current_user():
            useruuid = tokenizer.getClaims(self.get_current_user())['sub']
            eventdescr = self.get_arguments('eventdescription')[0]
            result = parkingDb.ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription(usruuid=useruuid, eventdescription=eventdescr)
            if result:
                self.write(json.dumps("success"))
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "renter-book-parking-aborted-UI", {'fromState': "processing", 'toState': "available", 'event': eventdescr, 'trigger': "user aborted in UI before payment", 'useruuid': useruuid})
            else:
                self.write(json.dumps("error"))


class reserveParkingAPIHandler(BaseHandler):
    '''
    Class reserveParkingAPIHandler
    Reserves Parking with given ID & timeslot and returns json file with success/failed state
    '''

    def post(self, *args, **kwargs):

        # API security: check user id
        if self.get_current_user():
            # 1- check if valid user
            # STUB: e.g. catch exceptions such as not paid last invoice, ...

            print("in POST /parkings/reserveParking, arguments: ", self.request.body)

            # TODO: write unit-test for this API endpoint and test for exception cases (e.g. invalid params, payment failed, no schedule in state "processing" found)

            try:
                # fetch arguments
                #timeslot = {'startTime': iso8601.parse_date(self.get_argument("startTime")), 'endTime': iso8601.parse_date(self.get_argument("endTime"))}
                unitname = self.get_argument("id")
                eventdescription = self.get_argument("eventdescription")
                useruuid = tokenizer.getClaims(self.get_current_user())['sub']

                # db calls
                # schedule = parkingDb.QueryScheduleinstatusprocessingByUserUUIDandTimeslot(useruuid, timeslot['startTime'], timeslot['endTime'])
                # reservedStatusID = parkingDb.QueryStatusID('reserved')
                # [scheduleID, scheduleStart, scheduleEnd, status, userID, pricepertimeunit, timeunitid]
                result = parkingDb.QueryScheduleinstatusprocessingByUserUUIDandEventdescription(useruuid, eventdescription)

                # 2- Initiate Mollie payment workflow
                try:
                    # prep data
                    # values = [schedule[5], schedule[6]]
                    values = [result['pricepertimeunit'], result['timeunitid']]
                    # amount = pplazautils.CalculateAmount(values, timeslot['startTime'], timeslot['endTime'])
                    amount = pplazautils.CalculateAmount(values, result['scheduleStart'], result['scheduleEnd'])
                    taxamount, amountexclTax = pplazautils.calculateTaxAmounts(amount, INV_COMP_TAXRATE, INV_COMP_PRECISION)
                    description = pplazautils.createInvoiceDescription(result['scheduleStart'], unitname)
                    # generate Mollie payment
                    self.CreatePayment(useruuid, description, amount, amountexclTax, taxamount, parkingDb.QueryUnitId(unitname), result['scheduleStart'], result['scheduleEnd'])

                except:
                    print("Something went wrong in POST /parkings/reserveParking with the CreatePayment step")

                # Update DB by setting state to 'reserved' for given schedule
                # parkingDb.UpdateSchedule(schedule[0], schedule[1], schedule[2], reservedStatusID, schedule[4])

                # 4- send status back to client: TEMP just sending back ID
                #self.write(json.dumps("success"))

            except:
                # TODO: implement logging
                print('something went wrong with POST from: ', self.get_current_user(), 'timestamp: ',
                      timezone(TIMEZONE).localize(datetime.now()).isoformat())
                self.write(json.dumps("not allowed"))

        else:
            # TODO: implement logging
            print(
            'invalid POST request to /parkings/reserveParking, timestamp: ', timezone(TIMEZONE).localize(datetime.now()).isoformat())
            self.write(json.dumps("no user"))

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")

    @gen.coroutine
    def CreatePayment(self, useruuid, description, amountinclTAX, amountExclTAX, TAXamount, unitid, starttime, endtime):

        try:
            # Generate invoice number. This code should prevent from executing multiple times at the same time!
            # http://www.tornadoweb.org/en/stable/locks.html
            # Note that these primitives are not actually thread-safe and cannot be used in place of those
            # from the standard library they are meant to coordinate Tornado co-routines in a single threaded
            # app, not to protect shared objects in a multi-threaded app.

            with (yield lock.acquire()):
                ordernr = self.generateInvoiceNumber()
                parkingDb.AddPayment(useruuid, ordernr, description, timezone(TIMEZONE).localize(datetime.now()).isoformat(), amountinclTAX, amountExclTAX, TAXamount, unitid, starttime, endtime)
                pass
            order_nr = int(ordernr)

            #
            # Payment parameters:
            # amount        Amount in EUROs.
            # description   Description of the payment.
            # redirectUrl   Redirect location. The customer will be redirected there after the payment.
            # metadata      Custom metadata that is stored with the payment.
            # in test phase: -> update weghookurl & redirecturl with parameters as defined in ngrok screen
            #
            payment = mollie.payments.create({
                'amount': amountinclTAX,
                'description': description,
                'webhookUrl': MOLLIE_WEBHOOKURL,
                'redirectUrl': MOLLIE_REDIRECTURL + '?ordernb=' + str(order_nr),
                'metadata': {
                    'order_nr': order_nr
                }
            })

            #
            # Send the customer off to complete the payment.
            #
            redirect_uri = payment.getPaymentUrl()
            self.write(json.dumps(redirect_uri))

        except Mollie.API.Error as e:
            yield 'API call failed: ' + e.message

    def generateInvoiceNumber(self):
        year = strftime('%y')
        month = strftime('%m')
        day = strftime('%d')

        #doe db query om te zien wat laatste factuur nummer was
        #LastInvoiceNr[0] = YYMMDDXXXX

        LastInvoiceNr = parkingDb.GetLastInvoiceNumber()
        LastInvoiceNr = str(LastInvoiceNr[0])
        LastInvoiceNRYY = LastInvoiceNr[:2]
        LastInvoiceNRMM = LastInvoiceNr[2:4]
        LastInvoiceNRDD = LastInvoiceNr[4:6]
        LastInvoiceCounter = LastInvoiceNr[-4:]

        #TODO: If we have more than 9999 invoices we will have issue due to limitations of integer
        #TODO: if we move over to year 22 we will have issue du to int limitations
        #check if laatste year, month, day zijn dezelfde. Indien dezelfde increment counter with 1
        if ((year == LastInvoiceNRYY) and (month == LastInvoiceNRMM) and (day == LastInvoiceNRDD)):
            NewInvoiceNumber = int(LastInvoiceCounter) +1
            NewInvoiceReturnNr = LastInvoiceNRYY + LastInvoiceNRMM + LastInvoiceNRDD + '{0:04}'.format(NewInvoiceNumber)

        else:
            NewInvoiceReturnNr = str(year) + str(month) + str(day) + '0001'

        #indien niet dezelfde update counter to 0 and update year,month,day
        return NewInvoiceReturnNr


class PaymentWebHookHandler(BaseHandler):

    def post(self, *args, **kwargs):

        try:
            # Retrieve the payment's current state.
            payment_id = self.get_argument('id')
            payment = mollie.payments.get(payment_id)
            order_nr = payment['metadata']['order_nr']

            if payment.isPaid():

                #If statement check to be sure we don't send out 2 the same invoices.
                #I've seen some cases where mollie sends 2 webhook messages, this will prevent double invoices sent via mail.
                status = parkingDb.GetPaymentStatus(order_nr)
                if(status[0] != "Paid"):

                    #function below is querying payment info to populate the invoice
                    paymentinfo = parkingDb.QueryPaymentDetails(order_nr)
                    email= paymentinfo[0]
                    description = paymentinfo[2]
                    amountinclTAX = paymentinfo[3]
                    amountexclTAX = paymentinfo[4]
                    TAXamount = paymentinfo[5]

                    #Update order nr to paid in DB
                    parkingDb.UpdatePaymentStatus(order_nr,payment_id,"Paid")

                    #generate invoice, function returns path to invoice
                    pathtoInvoice = invoicePDF.GenerateCustomerInvoice(order_nr,email ,description,"1", amountinclTAX, amountexclTAX, TAXamount, INV_COMP_PRODNAME)

                    #update payment in db with path to invoice
                    parkingDb.UpdateInvoiceLink(order_nr,pathtoInvoice)

                    #add payment details in jsonb of db
                    paymentdetails = payment['details']
                    parkingDb.UpdatePaymentDetails(paymentdetails,order_nr)

                    #Mollie needs a 200 reply otherwise keeps on sending payment updates via the webhook
                    self.set_status(200)
                    self.finish()

                    #send email with generated invoice
                    #below query will receive username from db to use in the email send to the customers.
                    usr = parkingDb.QueryInvoiceEmailRecipientAddr(email)
                    usern = usr[0]
                    userem = email
                    msg = templ.adaptInvoiceEmailTemplate(usern)
                    emailclient.sendEmail([userem],"./invoiceemail",SUPPORT_EMAIL,INV_SUBJECT_PAYMENTRECEIVED,pathtoInvoice)

                else:
                    #Mollie needs a 200 reply otherwise keeps on sending payment updates via the webhook
                    self.set_status(200)
                    self.finish()

            elif payment.isPending():
                #
                # The payment has started but is not complete yet.
                #
                # print("in POST /paymentwebhookhandler: Payment is pending, arguments - id:" + payment_id + " and order_nr: " + order_nr)
                parkingDb.UpdatePaymentStatus(order_nr,payment_id,"Pending")

                #Mollie needs a 200 reply otherwise keeps on sending payment updates via the webhook
                self.set_status(200)
                self.finish()

            elif payment.isOpen():
                #
                # The payment has not started yet. Wait for it.
                #
                # print("in POST /paymentwebhookhandler: Payment is Open, arguments - id: " +payment_id+" and order_nr: " + order_nr)
                parkingDb.UpdatePaymentStatus(order_nr,payment_id,"Payment is still open")

                #Mollie needs a 200 reply otherwise keeps on sending payment updates via the webhook
                self.set_status(200)
                self.finish()

            else:
                #
                # The payment isn't paid, pending nor open. We can assume it was aborted.
                #
                # print("in POST /paymentwebhookhandler: Payment is cancelled, arguments - id: " +payment_id+ " and order_nr: "+ order_nr)
                parkingDb.UpdatePaymentStatus(order_nr,payment_id,"Payment Cancelled")
                sch = parkingDb.QueryScheduleByPaymentOrdernr(order_nr) # useruuid, starttime, endtime, description, unitid
                poievid = parkingDb.QueryScheduleByTimeslot(startTimeSlot=sch[1], endTimeSlot=sch[2])[5]   # [scheduleID, scheduleStart, scheduleEnd, status, userID, poieventid]
                result = parkingDb.ResetScheduleinstatusprocessingtoavailableByUserUUIDandEventdescription(sch[0], parkingDb.QueryPoievent(poieventid=poievid)['eventdescription'])
                if result:
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "renter-book-parking-payment-aborted", {'fromState': "processing", 'toState': "available", 'schedule': sch, 'trigger': "user aborted payment", 'useruuid': sch[0]})

                #Mollie needs a 200 reply otherwise keeps on sending payment updates via the webhook
                self.set_status(200)
                self.finish()

        except Mollie.API.Error as e:
            return 'API call failed: ' + e.message


class PaymentRedirectHandler(BaseHandler):
    """
    Class PaymentRedirectHandler
    Redirect to /map screen after payment has been finished
    """
    def get(self):
        try:
            ordernr = str(self.get_arguments("ordernb")[0])

            # Update DB by setting state to 'reserved' for given schedule
            order = parkingDb.QueryScheduleByPaymentOrdernr(ordernr)    # [useruuid, starttime, endtime, description, unitid]
            schedule = parkingDb.QueryScheduleinstatusprocessingByUserUUIDandTimeslot(order[0], order[1], order[2])
            reservedStatusID = parkingDb.QueryStatusID('reserved')
            parkingDb.UpdateSchedule(schedule[0], schedule[1], schedule[2], reservedStatusID, schedule[4])
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "renter-book-parking-success", {'fromState': "processing", 'toState': "reserved", 'schedule': schedule, 'trigger': "user finished payment", 'useruuid': order[0]})

            self.redirect("/?reservationstatus=True&ordernr=" + ordernr)
        except:
            print('something went wrong with PAYMENTREDIRECTHANDLER at timestamp: ',
                      timezone(TIMEZONE).localize(datetime.now()).isoformat())


class myparkingsAPIHandler(BaseHandler):
    """
    Class myparkingsAPIHandler
    Returns myparkings Collection
    """
    def get(self, *args, **kwargs):
        try:
            if(self.get_current_user()):
                userid = parkingDb.QueryUserIDByUUID(tokenizer.getClaims(self.get_current_user())['sub'])
                parkings = parkingDb.QueryUnitsForgivenuserid(userid)
                result = pplazautils.prepListOfTuplesForMyParkings(parkings)
                self.write(json.dumps(result))

            else:
                # If no user, redirect to log-in
                self.redirect("/auth/google-login")
        except:
            # TODO: implement logging
            print('something went wrong with myparkingsAPIHandler from user:: ', self.get_current_user(), 'timestamp: ',
                timezone(TIMEZONE).localize(datetime.now()).isoformat())
            self.write(json.dumps("failure"))

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


class reservationsAPIHandler(BaseHandler):
    """
    Class reservationsAPIHandler
    Returns reservations Collection
    """

    def get(self, *args, **kwargs):

        # API security: check user id
        if self.get_current_user():

            print("in GET /reservations, user: ", self.get_current_user())

            try:

                # 1- check if valid user   ----TODO: enable token check once bug is fixed
                # STUB: e.g. catch exceptions such as not paid last invoice, ...
                # if not tokenizer.isValidToken(self.get_current_user()):
                #    print("token expired")
                #    self.redirect("/auth/google-login")

                # else:
                id = tokenizer.getClaims(self.get_current_user())['sub']
                # db call
                t = parkingDb.QuerySchedulesbyUserUUIDandStatus(id, 'reserved')
                # prep format for HeaderApp
                result = pplazautils.prepListOfTuplesForHeaderApp(t)
                self.write(json.dumps(result))
            except:
                # TODO: implement logging
                print('something went wrong with POST from: ', self.get_current_user(), 'timestamp: ',
                      timezone(TIMEZONE).localize(datetime.now()).isoformat())
                self.write(json.dumps("failure"))

        else:
            # If no user, redirect to log-in
            self.redirect("/auth/google-login")


    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


class addParkingAPIHandler(BaseHandler):
    """
    Class addParkingAPIHandler
    Returns true if success, false otherwise
    """

    def post(self, *args, **kwargs):

        # API security: check user id
        if self.get_current_user():
            # 1- check if valid user
            # STUB: e.g. catch exceptions such as not paid last invoice, ...

            print("in POST /parkings/addParking, arguments: ", self.request.body)
            id = tokenizer.getClaims(self.get_current_user())['sub']
            checkTimestamp = timezone(TIMEZONE).localize(datetime.now()).isoformat()

            # 1- add owner
            # check whether owner already exists (based on UUID/userID)
            checkOwnerId = parkingDb.QueryOwnerIDWithUUID(id)
            if checkOwnerId != 0:
                # owner already exists, so don't add again; update ownerid and move directly to step 2-
                ownerid = checkOwnerId
            else:
                # ownerprops = {'ownermobile': self.get_arguments("ownermobile")[0], 'toscheckdone': checkTimestamp}
                ownerprops = {'toscheckdone': checkTimestamp}
                # ownerid = parkingDb.AddOwnerWithUUID(id, self.get_arguments("ownerbankaccount")[0], ownerprops)
                ownerid = parkingDb.AddOwnerWithUUID(id, "", ownerprops)
                parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-add-parking-new-owner", {'useruuid': id, 'new-ownerid': ownerid})

            # 2- add unit
            usr = parkingDb.QueryUserByUserUUID(id)
            userid = usr[0]
            usern = usr[1]
            userem = usr[2]
            # TEMP removed parking type and hard-coded to 1 (parking-lot) to simplify as part of #62
            # typeid = parkingDb.QueryTypeID(self.get_arguments("parkingtype")[0])
            typeid = 1
            # retrieve latlon & address
            t = self.get_arguments("unitaddress")

            # find city and use first digit to build unit Friendlyname
            addr = json.loads(t[0])["title"]
            splitaddr = re.split(',', addr)
            # all Places entries are <addr, nb, city, country> or <addr, city, country> or <city, country> or <country>
            # Find the ones with complete address (4 entries) and filter out
            if len(splitaddr) < 3:
                result = "false"
            else:
                cityaddr = splitaddr[len(splitaddr) - 2][1:]
                fname = parkingDb.GetUniqueUnitFriendlyName(cityaddr)
                unitprops = {'fulladdress': addr}
                latlon = str(json.loads(t[0])["latitude"]) + "," + str(json.loads(t[0])["longitude"])
                if parkingDb.QueryIfUnitExists(latlon):
                    # unit already exists in our DB
                    self.write("false")
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-add-parking-failed", {'error': "unit already exists", 'unit-latlon': latlon, 'user': usr})
                else:
                    # detect to which POI this point belongs (based on location) and if none, send email to admin
                    resultpoiid = parkingDb.FindPoiIDforGivenPoint(latlon)
                    if resultpoiid != 0:
                        unitResult = parkingDb.AddUnit(fname, latlon, userid, typeid, resultpoiid, ownerid, cityaddr, unitprops)
                        self.write("true")
                        mess = templ.adaptAddUnitEmailTemplate(userem, usern, fname, parkingDb.QueryPoiFriendlyname(resultpoiid), "15EUR", "2EUR", parkingDb.QueryOwnerBankAccount(ownerid), addr)
                        emailclient.sendEmail([userem], './addUnit', conf['support-email'], EMAILSUBJECT)
                        parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-add-parking-success-existing-poi", {'user': usr, 'unit-laton': latlon, 'poiid': resultpoiid})
                    else:
                        unitResult = parkingDb.AddUnit(fname, latlon, userid, typeid, resultpoiid, ownerid, cityaddr, unitprops)
                        self.write(json.dumps("no-poi"))
                        # no Poi detected -> send email to admin for manual action and change Poiid from 0 to new value
                        # msg = 'User ' + str(userid) + ' registered parking unit ' + fname + ' in our system. \n No Poi has been found so manual action is required to set the price!' + timezone(TIMEZONE).localize(datetime.now()).isoformat()
                        msg = templ.adaptNewPoiEmailTemplate(str(userid), fname, timezone(TIMEZONE).localize(datetime.now()).isoformat())
                        emailclient.sendEmail([conf['support-email'], "joerinicolaes@gmail.com", "jeroenmachiels@gmail.com"], './addPoi', conf['support-email'], EMAILSUBJECTUNITPENDING + ' for environment ' + ENVIRONMENT)
                        mess = templ.adaptAddUnitPendingEmailTemplate(userem, usern, fname)
                        emailclient.sendEmail([userem], './addUnitPending', conf['support-email'], EMAILSUBJECT)
                        parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-add-parking-pending-new-poi", {'user': usr, 'unit-laton': latlon})

        else:
            # TODO: implement logging
            # TODO: implement logging
            print(
            'invalid POST request to /parkings/addParking, timestamp: ', timezone(TIMEZONE).localize(datetime.now()).isoformat())
            self.write(json.dumps("no user"))
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-add-parking-failed", {'error': "no user"})

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


class setScheduleAPIHandler(BaseHandler):
    """
    Class to handle email schedule activations (triggered after ownernotification email)
    """
    def get(self):

        # 1- unpack token and fetch data
        data = tokenizer.getClaims(self.get_arguments('token')[0])

        if data:
            # check if token was valid and claims retrieved
            unit = parkingDb.QueryUnit(data['unitid'])  # dict ('unitname', 'latlon', 'userid', 'typeid', 'poiid', 'ownerid', 'properties', 'unitid', 'cityname')
            event = parkingDb.QueryPoievent(data['poieventid'])     # dict ('poieventid', 'eventdescription', 'eventstart', 'properties', 'poiid')

            # 2- verify whether a setschedule has already occurred for this unitid and poieventid (avoid double-entries by multiple clicks on url)
            if not parkingDb.QueryUnitPropertiesForSetScheduleWithGivenPoieventid(data['unitid'], data['poieventid']):
                # not entry found yet ==> add to schedule
                result = parkingDb.AddSchedule(data['unitid'], unit['ownerid'], event['eventstart'] + timedelta(hours=-1), event['eventstart'] + timedelta(hours=3), parkingDb.QueryPoiPricepertimeunit(event['poiid']), 1, 1, 1, "", data['poieventid'])
                parkingDb.UpdateUnitProperties(data['unitid'], {"setschedule": {"poieventid": data['poieventid'], "timestamp": timezone(TIMEZONE).localize(datetime.now()).isoformat()}})

                # 3- present screen to owner that his unit has been set to available & present overview of available hours for his unit
                if result:
                    self.redirect("/schedule?setscheduletoken=" + tokenizer.createScheduleToken(event['eventdescription'], unit['unitname']))
                    # self.redirect("/schedule?unit=" + json.dumps(data['unitid']))
                    parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-set-schedule-success", {'unit': unit, 'event': event, 'token': self.get_arguments('token')[0]})

        else:
            # getClaims returned None >> present schedule page and log to events table as failure
            self.redirect("/schedule")
            parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-set-schedule-failure", {'token': self.get_arguments('token')[0]})


class suggestLocationAPIHandler(BaseHandler):
    """
    Class suggestLocationAPIHandler
    Returns true if success, false otherwise
    """

    def post(self, *args, **kwargs):

        print("in POST /parkings/suggestLocation, arguments: ", self.request.body)

        id = ''
        loc = ''
        email = ''
        user = ''
        addr = ''
        lat = ''
        long = ''

        try:
            id = tokenizer.getClaims(self.get_current_user())['sub']
        except:
            pass

        try:
            loc = self.get_arguments("location")
            addr = json.loads(loc[0])["title"]
            long = json.loads(loc[0])["longitude"]
            lat = json.loads(loc[0])["latitude"]
            email = self.get_arguments("email")[0]
        except:
            pass

        if email:
            user = email
        else:
            user = id

        msg = templ.adaptSuggestLocationEmailTemplate(str(user), addr + '; lat: ' + str(lat) + '; long: ' + str(long), timezone(TIMEZONE).localize(datetime.now()).isoformat())
        emailclient.sendEmail([conf['support-email'], "joerinicolaes@gmail.com", "jeroenmachiels@gmail.com"], CONTENTFOLDER + SUGGESTLOCATION_EMAIL, conf['support-email'], SUGGESTLOCATION_EMAIL_SUBJECT + ' for environment ' + ENVIRONMENT)

        self.write("true")

    def set_default_headers(self):
        # redefine to JSON for data send back to client
        self.set_header('Content-Type', 'application/json')
        self.set_header("Cache-Control", "no-cache")


def sendSetScheduleEmailsToOwners():
    """
    Send set schedule emails to owners and update DB with event record on number of emails sent
    :return: none
    """
    ownerlist = ownerNotification.sendEmailsToOwners(emailclient, templ, DAYS_TO_EVENT)
    for item in ownerlist:
        parkingDb.AddEvent(timezone(TIMEZONE).localize(datetime.now()), "owner-notification-email", item)


# initialize class objects for Schedule and Users
sMechelen = schedule()
uMechelen = users()
print("schedule and users initialized")


if __name__ == "__main__":
    # launch Python Scheduler
    scheduler = TornadoScheduler()
    # lambda: required to make this a callable function (else TypeError raised by apscheduler)
    scheduler.add_job(lambda: sendSetScheduleEmailsToOwners(), 'cron', hour=OWNERNOTIFICATION_HOUR, minute=OWNERNOTIFICATION_MINUTE)
    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.

    # launch Tornado web server
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    #http_server = tornado.httpserver.HTTPServer(Application(), ssl_options={"certfile": "/Users/Joeri/sshkeys/cert.pem", "keyfile":"/Users/joeri/sshkeys/key.pem"})
    http_server.listen(options.port)

    try:
        print("serving running at port " + str(options.port))   #TODO: implement logging
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        pass
