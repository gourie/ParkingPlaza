__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'
__version__ = '0.1'

import dns.resolver
from dns.resolver import query
import re

class emailChecker:
    """
    Class to verify email addresses
    """
    def __init__(self):
        """
        Init class
        :return:
        """
        self.mailsearch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')

    def verifyEmailFormat(self, emailaddr):
        """
        verify whether the emailaddress provided 'resembles' a typical email address
        :param emailaddr: input email address to check
        :return: true if matches x @ y . z format, else false
        """
        result = self.mailsearch.match(emailaddr)
        if result is None:
            return False
        else:
            return True

