__author__ = 'Joeri Nicolaes'
__author_email__ = 'joerinicolaes@gmail.com'
__version__ = 'alpha'

#!/usr/bin/python
import io

class adaptEmailTemplate:

    def __init__(self, contentfolder):
        self.contenturl = contentfolder

    def adaptAddUnitEmailTemplate(self, useremail, username, unitname, poiname, eventrate, hourlyrate, bankaccount, unitaddress):
        """
        Adapt addunit-email-template by replacing variables with system data
        :param useremail:
        :param username:
        :param unitname:
        :param poiname:
        :param eventrate:
        :param hourlyrate:
        :return: none, output.txt will be
        """
        # Create the new config file for writing
        config = io.open('addUnit', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('addunit-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$useremail' in line:
                line = line.replace('$useremail', useremail)
            if '$username' in line:
                line = line.replace('$username', username)
            if '$unitname' in line:
                line = line.replace('$unitname', unitname)
            if '$poiname' in line:
                line = line.replace('$poiname', poiname)
            if '$eventrate' in line:
                line = line.replace('$eventrate', eventrate)
            if '$hourlyrate' in line:
                line = line.replace('$hourlyrate', hourlyrate)
            if '$bankaccount' in line:
                line = line.replace('$bankaccount', bankaccount)
            if '$unitaddress' in line:
                line = line.replace('$unitaddress', unitaddress)
            config.write(line)

        # Close the files
        config.close()

    def adaptAddUnitPendingEmailTemplate(self, useremail, username, unitname):
        """
        Adapt addunitpending-email-template by replacing variables with system data
        :param useremail:
        :param username:
        :param unitname:
        :return: none, output.txt will be
        """
        # Create the new config file for writing
        config = io.open('addUnitPending', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('addunitpending-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$useremail' in line:
                line = line.replace('$useremail', useremail)
            if '$username' in line:
                line = line.replace('$username', username)
            if '$unitname' in line:
                line = line.replace('$unitname', unitname)
            config.write(line)

        # Close the files
        config.close()

    def adaptNewPoiEmailTemplate(self, userid, unitname, date):
        """
        Adapt newPoi-email-template by replacing variables with system data
        :param userid:
        :param unitname:
        :param date:
        :return:
        """
        # Create the new config file for writing
        config = io.open('addPoi', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('newPoi-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$userid' in line:
                line = line.replace('$userid', userid)
            if '$unitname' in line:
                line = line.replace('$unitname', unitname)
            if '$date' in line:
                line = line.replace('$date', date)
            config.write(line)

        # Close the files
        config.close()

    def adaptUserEmailConfirmationTemplate(self, userem, userfn, link):
        """
        Adapt newUserEmailConfirmationTemplate by replacing variables with system data
        :param userem: user email
        :param userfn: user first name
        :param link: confirmation url
        :return:
        """
        # Create the new config file for writing
        config = io.open('userEmailConfirmation', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('userEmailConfirmationTemplate', 'r'):
            # check for specific variables and overwrite if found
            if '$useremail' in line:
                line = line.replace('$useremail', userem)
            if '$firstname' in line:
                line = line.replace('$firstname', userfn)
            if '$link' in line:
                line = line.replace('$link', link)
            config.write(line)

        # Close the files
        config.close()

    def adaptNewUserEmailTemplate(self, userem, usern):
        """
        Adapt newUserTemplate by replacing variables with system data
        :param userem: user email
        :param usern: user full name
        :return:
        """
        # Create the new config file for writing
        config = io.open('newUser', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('newUserTemplate', 'r'):
            # check for specific variables and overwrite if found
            if '$useremail' in line:
                line = line.replace('$useremail', userem)
            if '$username' in line:
                line = line.replace('$username', usern)
            config.write(line)

        # Close the files
        config.close()

    def adaptInvoiceEmailTemplate(self, username):
        """
        Adapt invoice-email-template by replacing variables with system data
        :param username:
        :return: none, output.txt will be
        """
        # Create the new config file for writing
        config = io.open('invoiceemail', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open('invoice-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$username' in line:
                line = line.replace('$username', username)
            config.write(line)

        # Close the files
        config.close()

    def adaptNotifyOwnerEmailTemplate(self, username, unitaddress, eventdescription, parkingstart, parkingend, setschedulelink):
        """
        Adapt notify-email-template by replacing variables with system data
        :param username: ownername string
        :param unitaddress: unitaddress string
        :param eventdescription: eventdescription string
        :param parkingstart: start of parking, string
        :param parkingend: end of parking, string
        :param setschedulelink: setschedulelink string
        :return: none, ownernotificationemail.txt will be updated
        """
        # Create the new config file for writing
        config = io.open(self.contenturl + '/ownernotificationemail', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open(self.contenturl + '/ownernotification-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$username' in line:
                line = line.replace('$username', username)
            if '$unitaddress' in line:
                line = line.replace('$unitaddress', unitaddress)
            if '$eventdescription' in line:
                line = line.replace('$eventdescription', eventdescription)
            if '$parkingstart' in line:
                line = line.replace('$parkingstart', parkingstart)
            if '$parkingend' in line:
                line = line.replace('$parkingend', parkingend)
            if '$setschedulelink' in line:
                line = line.replace('$setschedulelink', setschedulelink)
            config.write(line)

        # Close the files
        config.close()

    def adaptSuggestLocationEmailTemplate(self, user, location, date):
        """
        Adapt suggestLocation-email-template by replacing variables with system data
        :param user:
        :param location:
        :param date:
        :return:
        """
        # Create the new config file for writing
        config = io.open(self.contenturl + '/suggestLocationEmail', 'w')

        # Read the lines from the template, substitute the values, and write to the new config file
        for line in io.open(self.contenturl + '/suggestLocation-email-template', 'r'):
            # check for specific variables and overwrite if found
            if '$useremail' in line:
                line = line.replace('$useremail', user)
            if '$location' in line:
                line = line.replace('$location', location)
            if '$date' in line:
                line = line.replace('$date', date)
            config.write(line)

        # Close the files
        config.close()