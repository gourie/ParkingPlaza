import dateutil

__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

import datetime
from decimal import Decimal
import iso8601

class utilities:
    """
    Class with utility functions shared across all other classes
    """

    def prepListOfEventsForMap(self, inp):
        """
        1/ Add dictionary keys 'eventdescription', 'eventstart', 'eventcapacity' as expected by ParkingMapApp
        2/ Convert each dateTime object in input array to UTC ISO8601 time string
        :param inp: list of tuples with [0]=eventdescription as str, [1]=startTime as Python datetime object, [2] eventcapacity as int
        :return: same array but each tuple converted to dict ('eventdescription', 'eventStart', 'eventCapacity') and times converted to UTC ISO8601 time string
        """
        result = range(len(inp))
        for i in range(len(inp)):
            result[i] = {'eventdescription': inp[i][0], 'eventstart': inp[i][1].isoformat(), 'eventcapacity': inp[i][2]}
        return result

    def prepListOfTuplesForHeaderApp(self, inp):
        """
        1/ Add dictionary keys 'parkingId', 'startTime' and 'endTime' as expected by HeaderApp
        2/ Convert each dateTime object in input array to UTC ISO8601 time string
        :param inp: list of tuples with [0]=id, [1]=startTime as Python datetime object, [2]=endTime as Python datetime object
        :return: same array but each tuple converted to dict ('parkingId', 'startTime' and 'endTime') and times converted to UTC ISO8601 time string
        """
        result = range(len(inp))
        for i in range(len(inp)):
            result[i] = {'parkingId': inp[i][0], 'startTime': inp[i][1].isoformat(), 'endTime': inp[i][2].isoformat()}
        return result

    def prepListOfTuplesAccountInfoUser(self, inp):
        """
        1/ Add dictionary keys 'fullname', 'email' as expected by HeaderApp
        :param inp: list of tuples with [0]=userid, [1]=fullname, ...
        :return: dict of UI user elements ('fullname', 'email')
        """
        return {'fullname': inp[1], 'email': inp[2]}


    def prepListOfTuplesAccountInfoOwner(self, inp):
        """
        1/ Add dictionary keys 'fullname', 'email' as expected by HeaderApp
        :param inp: list of tuples with [0]=userid, [1]=fullname, ...
        :return: dict of UI user elements ('fullname', 'email')
        """
        return {'fullname': inp[1], 'email': inp[2]}

    def prepListOfTuplesForMyParkings(self, inp):
        """
        1/ Add dictionary keys 'unitfriendlyname', 'latitude', 'longitude', 'parkingtype', 'cityname', 'fulladdress' as expected by HeaderApp
        :param inp: list of tuples: ('M1', {'lat': 50.8830758, 'lon': 4.4400302}, 25, 1, 0, 12, {u'fulladdress': u'Telecomlaan, Machelen, Belgium'}, 86, 'Machelen')
        :return: same array but each tuple converted to dict
        """

        result = range(len(inp))
        for i in range(len(inp)):
            result[i] = {'UnitFriendlyName': inp[i][0], 'Latitude': inp[i][1]['lat'], 'Longitude': inp[i][1]['lon'], 'ParkingType': inp[i][2], 'CityName': inp[i][3], 'FullAddress': inp[i][4]['fulladdress']}
        return result

    def prepSchedulesListForParkingListApp(self, listofschedules, eventdescription=""):
        """
        1/ Convert each dateTime object in input array to UTC ISO8601 time string
        2/ Set changed to "true" if 'eventdescription' matches given value
        :param listofschedules: list of dicts from QuerySchedulesbyUnitId schedules ['eventstart', 'eventdescription', 'schedulestatus'], [] if none found
        :param eventdescription: descr that has been changed ("" if none)
        :return: same array but each tuple converted to dict ('eventstart', 'eventdescription', 'schedulestatus' and 'changed') and times converted to UTC ISO8601 time string
        """
        results = []
        for item in listofschedules:
            item['changed'] = "false"
            item['eventstart'] = item['eventstart'].isoformat()
            if item['eventdescription'] == eventdescription:
                item['changed'] = "true"
            results.append(item)
        return results


    # Invoice and Payment related utils
    def createInvoiceDescription(self, starttime, unitfriendlyname):
        #desstarttime = self.retDateTime(starttime)
        description = "Parking place (" + str(unitfriendlyname) + ") reserved on: " + str(starttime.day) + "/" + str(starttime.month) + "/" + str(starttime.year)
        return description

    def calculateTaxAmounts(self, amountinclTAX, INV_COMP_TAXRATE, INV_COMP_PRECISION):
        taxamount = amountinclTAX - (amountinclTAX/((float(INV_COMP_TAXRATE) + 100)/100))
        roundedtaxamount = self.getroundeddecimal(taxamount,INV_COMP_PRECISION)
        roundedamountinclTax = self.getroundeddecimal(amountinclTAX,INV_COMP_PRECISION)
        amountexclTax = roundedamountinclTax - roundedtaxamount
        return roundedtaxamount, amountexclTax

    def getroundeddecimal(self, nrtoround, precision):
        d = Decimal(nrtoround)
        aftercomma = Decimal(precision) # or anything that has the exponent depth you want
        rvalue = Decimal(d.quantize(aftercomma, rounding='ROUND_HALF_UP'))
        return rvalue

    def retDateTime(self,starttime):
        retstarttime = dateutil.parser.parse(starttime)
        return retstarttime

    def getNrOfHoursToBePaidFor(self,starttime,endtime):
        # nrofhours = dateutil.parser.parse(endtime) - dateutil.parser.parse(starttime)
        nrofhours = endtime - starttime
        hours = nrofhours.seconds/float(3600)
        return hours

    def getNrOfDaysToBePaidFor(self,starttime,endtime):
        # nrofdays = dateutil.parser.parse(endtime) - dateutil.parser.parse(starttime)
        nrofdays = endtime - starttime
        return nrofdays.days

    def CalculateAmount(self, values, starttime, endtime):

        try:
            qamount = values[0]
            qtimeunitid = values[1]

            #qtimeunitid = 1 = fixed price
            #qtimeunitid = 2 = hourly
            #qtimeunitid = 3 = daily
            if qtimeunitid == 1 :
                return qamount
            elif qtimeunitid == 2:
                hours = self.getNrOfHoursToBePaidFor(starttime, endtime)
                totalamount = qamount * hours
                return  totalamount
            else:
                days = self.getNrOfDaysToBePaidFor(starttime, endtime)
                totalamount = qamount * days
                return totalamount
        except:
            print ("Something went wrong in the CalculateAmount Function")

    def convert_timedelta(self, duration):
        """
        Convert Timedelta object into days, hours, minutes, seconds
        :param duration: timedelta object with days and seconds of difference
        :return: {'days': <timedelta days difference>, 'hours': <timedelta hours difference>, 'minutes': <timedelta minutes difference>, 'seconds': <timedelta secs difference> }
        """
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}

    def checkIfValidDatetime(self, input):
        """
        Check whether the provided input is a valid datetime input
        :param input: any data point that needs to be validated whether it's a datetime object or string
        :return: True if valid, False else
        """
        try:
            iso8601.parse_date(input)
            return True
        except:
            # not a valid ISO8601 string that can be converted to Python Datetime
            try:
                if isinstance(input, datetime.date):
                    return True
                else:
                    return False
            except:
                return False