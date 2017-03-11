# from numpy.distutils.fcompiler import none

__author__ = 'Jeroen Machiels'
__author_email__ = 'jeroenmachiels@gmail.com'
__version__ = '0.1'

from datetime import datetime, date
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice

class Invoice:

    INV_COMP_NAME = None
    INV_COMP_STREET = None
    INV_COMP_NR = None
    INV_COMP_CITY = None
    INV_COMP_STATE = None
    INV_COMP_COUNTRY = None
    INV_COMP_POSTAL = None
    INV_COMP_VATNR = None
    INV_COMP_TAXRATE = None
    INV_COMP_FOOT = None
    INV_COMP_PATH = None
    INV_COMP_PRECISION = None

    def __init__(self,INV_COMP_NAME, INV_COMP_STREET, INV_COMP_NR, INV_COMP_CITY, INV_COMP_STATE, INV_COMP_COUNTRY, INV_COMP_POSTAL, INV_COMP_VATNR, INV_COMP_TAXRATE, INV_COMP_FOOT, INV_COMP_PATH, INV_COMP_PRECISION = '0.01'):
        self.INV_COMP_NAME = INV_COMP_NAME
        self.INV_COMP_STREET = INV_COMP_STREET
        self.INV_COMP_NR = INV_COMP_NR
        self.INV_COMP_CITY = INV_COMP_CITY
        self.INV_COMP_STATE = INV_COMP_STATE
        self.INV_COMP_COUNTRY = INV_COMP_COUNTRY
        self.INV_COMP_POSTAL = INV_COMP_POSTAL
        self.INV_COMP_VATNR = INV_COMP_VATNR
        self.INV_COMP_TAXRATE = INV_COMP_TAXRATE
        self.INV_COMP_FOOT = INV_COMP_FOOT
        self.INV_COMP_PATH = INV_COMP_PATH
        self.INV_COMP_PRECISION = INV_COMP_PRECISION

    def GenerateCustomerInvoice(self,invoicenumber, clientemail, reservationtype, quantity, amountInclVAT, amountExVAT, vatAmount, productname):
        #invoice number should be int
        #client email we need to receive
        #reservationtype = upfront reservation or instant reservation
        #quantity = numbers of units purchased
        #amountExVAT = amount paid excluding vat
        #VAT = Vat % (21)

        try:
            pathtoInvoice = self.INV_COMP_PATH + invoicenumber +".pdf"
            doc = SimpleInvoice(pathtoInvoice,precision=self.INV_COMP_PRECISION)

            # Paid stamp, optional
            doc.is_paid = True

            doc.invoice_info = InvoiceInfo(invoicenumber, datetime.now(), datetime.now())  # Invoice info, optional

            # Service Provider Info, optional
            doc.service_provider_info = ServiceProviderInfo(
                name=self.INV_COMP_NAME,
                street=self.INV_COMP_STREET + " " + self.INV_COMP_NR,
                city=self.INV_COMP_CITY,
                state=self.INV_COMP_STATE,
                country=self.INV_COMP_COUNTRY,
                post_code=self.INV_COMP_POSTAL,
                vat_tax_number=self.INV_COMP_VATNR
            )

            # Client info, optional
            doc.client_info = ClientInfo(email=clientemail)

            # Add Item
            #doc.add_item(Item(productname, reservationtype, quantity, amountExVAT))
            doc.add_item(Item(productname, reservationtype, quantity, amountInclVAT, amountExVAT, vatAmount))
            #doc.add_item(Item('Item', 'Item desc', 2, '2.2'))
            #doc.add_item(Item('Item', 'Item desc', 3, '3.3'))

            # Tax rate, optional
            doc.set_item_tax_rate(self.INV_COMP_TAXRATE)

            # Transactions detail, optional
            # doc.add_transaction(Transaction('Paypal', 111, datetime.now(), 1))
            # doc.add_transaction(Transaction('Strip', 222, date.today(), 2))

            # Optional
            doc.set_bottom_tip(self.INV_COMP_FOOT)

            doc.finish()
            return pathtoInvoice
        except StandardError:
            print "Unexpected error"
            return "error"