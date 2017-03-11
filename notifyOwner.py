__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime, timedelta
import json
from pytz import timezone

with open('./config.json', 'r') as file:
    conf = json.loads(file.read())
TIMEZONE = str(conf['timezone'])

class notifyOwnerToSetSchedule():
    """
    Class that contains all logic to notify owner for User Story SetSchedule
    """

    def __init__(self, serverurl, serverparkingsetscheduleurl, notificationtype, supportemail, contentfolder, notificationemail, notificationemailsubject, daysbeforeevent, tokenizer, db):
        self.serverurl = serverurl
        self.serverparkingsetscheduleurl = serverparkingsetscheduleurl
        self.notification = notificationtype
        self.supportemail = supportemail
        self.contentfolder = contentfolder
        self.notificationemail = notificationemail
        self.notificationemailsubject = notificationemailsubject
        self.timeToEvent = daysbeforeevent
        self.tokenizer = tokenizer
        self.parkingDb = db

    def findOwnersWhoNeedToSetSchedule(self, fromdate, daystoevent, unittest=False):
        """
        Find all owners that need to set their schedule based
        :param fromdate: date from which the number of days are counted, as Python datetime
        :param daystoevent: number of days as int; used for filtering the events that are occuring from now within daystoevent (e.g. 5 -> filter is set on all poievents that take place within 5 days)
        :return: ['eventdescription', 'eventstart', 'eventendhour', 'unitaddress', 'ownername', 'owneremail', 'setscheduleurl'] for all events occuring within daysbeforeevent
        """

        # Return: None or ('poieventid', 'eventdescription', 'unitid', 'unitname', 'ownername', 'owneremail')
        result = []
        if unittest:
            result = self.parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(fromdate, daystoevent, unittest=True)
        else:
            result = self.parkingDb.QueryAvailablePoiEventsWithinGivenAmountofdays(fromdate, daystoevent)
        ownersList = []
        for item in result:
            if not self.parkingDb.CheckIfUnitHasScheduleForGivenPoieventid(item['unitid'], item['poieventid']):
                url = self.generateOwnerSetScheduleUrl(item['poieventid'], item['unitid'])
                ownersList.append({ 'eventdescription': item['eventdescription'], 'eventstart': self.generateDatetimeString(item['eventdate'] + timedelta(hours=-1), TIMEZONE),  'eventendhour': self.generateTimeString(item['eventdate'] + timedelta(hours=3), TIMEZONE), 'unitaddress': item['unitaddress'], 'ownername': item['ownername'], 'owneremail': item['owneremail'], 'setscheduleurl': url })
        return ownersList

    def generateDatetimeString(self, inputdate, tz):
        """
        Generate datetimestring for the given timezone
        :param inputdate: Python datetime object that needs to be transformed
        :param tz: timezone string
        :return: string formatted
        """
        result = ""
        format = ""
        if tz == 'Europe/Brussels':
            # hard-coded based on https://en.wikipedia.org/wiki/Date_format_by_country
            # TODO: fetch from CLDR later (internationalization enhancement)
            format = "%A %d %B %Y %-H:%M"
        if format:
            result = inputdate.strftime(format)
        return result

    def generateTimeString(self, inputdate, tz):
        """
        Generate timestring for the given timezone
        :param inputdate: Python datetime object that needs to be transformed
        :param tz: timezone string
        :return: string formatted
        """
        result = ""
        format = ""
        if tz == 'Europe/Brussels':
            # hard-coded based on https://en.wikipedia.org/wiki/Date_format_by_country
            # TODO: fetch from CLDR later (internationalization enhancement)
            format = "%-H:%M"
        if format:
            result = inputdate.strftime(format)
        return result

    def generateOwnerSetScheduleUrl(self, poieventid, unitid):
        """
        Generate secure, unique ownersetschedule url for email to owner
        :param poieventid: PK of POIEVENTS table as int
        :param unitid: PK of UNIT table as int
        :return: key as string
        """
        token = self.tokenizer.createSetScheduleToken(poieventid, unitid)
        return self.serverurl + self.serverparkingsetscheduleurl + "?token=" + token

    def sendEmailsToOwners(self, emailclient, emailtemplate, daystoevent):
        """
        Send emails to all owners that require notification; filter on poievents that are occuring within days
        Remark: if an owner has multiple units, he'll receive one separate email for each unit (could be optimised later)
        :param emailclient: emailclient as object
        :param emailtemplate: emailtemplate as object
        :param daystoevent: number of days as int; used for filtering the events that are occuring from now within daystoevent (e.g. 5 -> filter is set on all poievents that take place within 5 days)
        :return: number of emails sent (currently pretty dumb total)
        """
        result = self.findOwnersWhoNeedToSetSchedule(timezone(TIMEZONE).localize(datetime.now()), daystoevent)
        for item in result:
            msg = emailtemplate.adaptNotifyOwnerEmailTemplate(item['ownername'], item['unitaddress'], item['eventdescription'], item['eventstart'], item['eventendhour'], item['setscheduleurl'])
            emailclient.sendEmail([item['owneremail']], self.contentfolder + self.notificationemail, self.supportemail, self.notificationemailsubject)
        # TODO: add checks for sendEmail (e.g. error messages means email not sent) - probably by reading our mailbox and scanning for Google Delivery Status Notification (DSN) emails, see http://stackoverflow.com/questions/5298285/detecting-if-an-email-is-a-delivery-status-notification-and-extract-informatio
        return result



