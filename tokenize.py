__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'

from datetime import datetime, timedelta
from pytz import timezone
import jwt  # Python PyJWT package


class tokenize:
    '''
    Class to handle JWT tokens (create, get, checkValidity)
    '''

    def __init__(self, secret, tz):
        """
        Init tokenizer
        :param secret: HMAC secret
        :param tz: timezone passed from config.json
        """
        self.HMAC_SECRET = secret
        # TZ set to BXL in config.json as I consider all user to be in CET for start
        # brussels = timezone('Europe/Brussels')
        self.timezone = timezone(tz)

    def createUUIDToken(self, uid):
        """
        Create JWT token for given user ID using HMAC algorithm (symmetric key from config file).
        :return: JWT token with exp claim set to 'valid for 1week'
        """
        payload = {
            'exp': self.timezone.localize(datetime.now()) + timedelta(weeks=1),
            'sub': uid
        }
        return jwt.encode(payload, self.HMAC_SECRET, algorithm='HS256')

    def createSetScheduleToken(self, poieventid, unitid):
        """
        Create JWT token for /setschedule using HMAC algorithm (symmetric key from config file).
        :param: poieventid as int
        :param: unit as int
        :return: JWT token with exp claim set to 'valid for 1day'
        """
        payload = {
            'exp': self.timezone.localize(datetime.now()) + timedelta(days=1),
            'poieventid': poieventid,
            'unitid': unitid
        }
        return jwt.encode(payload, self.HMAC_SECRET, algorithm='HS256')

    def createScheduleToken(self, poieventdescription, unitname):
        """
        Create JWT token for /schedule using HMAC algorithm (symmetric key from config file).
        :param: poieventdescription as string
        :param: unitname as string
        :return: JWT token with exp claim set to 'valid for 8days'
        """
        payload = {
            'exp': self.timezone.localize(datetime.now()) + timedelta(days=8),
            'eventdescription': poieventdescription,
            'unitname': unitname
        }
        return jwt.encode(payload, self.HMAC_SECRET, algorithm='HS256')

    def createEmailConfirmationToken(self, emailaddress):
        """
        Create JWT token for emailconfirmation using HMAC algorithm (symmetric key from config file).
        :param emailaddress: user email address
        :return: JWT token with exp claim set to 'valid for 7days'
        """
        payload = {
            'exp': self.timezone.localize(datetime.now()) + timedelta(days=7),
            'emailaddress': emailaddress
        }
        return jwt.encode(payload, self.HMAC_SECRET, algorithm='HS256')

    def isValidToken(self, token):
        """
        Verify whether given JWT token is still valid.
        :return: true if JWT token doesn't give jwt.ExpiredSignatureError
        """
        # print('in isValidToken: ', token)
        try:
            jwt.decode(token, self.HMAC_SECRET)
            return True
        except jwt.ExpiredSignatureError:
            # Signature has expired
            return False
        except jwt.DecodeError, e:
            # Signature verification failed: e.g. server-side change (new secret etc) will make 'old tokens still stored in client obselete and force now login'
            print('failed token: ', token)
            return e

    def getClaims(self, token):
        """
        Return all claims set for this token
        :return: dictionary with JWT token claims (e.g. 'exp', 'sub' for UUIDtoken), None if jwt.ExpiredSignatureError
        """
        result = None
        try:
            result = jwt.decode(token, self.HMAC_SECRET)
        except jwt.ExpiredSignatureError, e:
            pass
            print('failed token: ', token, ' at timestamp: ', self.timezone.localize(datetime.now()).isoformat())
            print('claims: ', jwt.decode(token, self.HMAC_SECRET, verify=False), ' at timestamp: ', self.timezone.localize(datetime.now()).isoformat())
        return result