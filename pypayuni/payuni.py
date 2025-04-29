# -*- coding: UTF-8 -*-
import base64
import binascii
import time
import datetime
import urllib
import hashlib
import logging
import six

from Crypto.Cipher import AES
'''
    Configure your personal setting in setting.py
'''
from pypayuni.setting import HASH_IV, HASH_KEY
from pypayuni.setting import PAYUNI_SANDBOX_SERVICE_URL, PAYUNI_SERVICE_URL, RETURN_URL, CLIENT_BACK_URL
from pypayuni.setting import PAYUNI_PERIOD_URL, PAYUNI_SANDBOX_PERIOD_URL 

from pypayuni.setting import MERCHANT_ID
from pypayuni.setting import PAYUNI_SANDBOX
from pypayuni.setting import PERIOD_TYPE 

class Payuni():
    # If it is in sandbox mode ?
    is_sandbox = PAYUNI_SANDBOX

    def __init__(self, payment_conf, service_method='post', subscription=False):
        self.url_dict = dict()

        # === BASIC CONFIG FOR PAYUNI ===
        if 'Language' in payment_conf:
            self.language = payment_conf['Language']
        self.service_method = service_method
        self.HASH_KEY = HASH_KEY if not ('HASH_KEY' in payment_conf) else payment_conf['HASH_KEY']
        self.HASH_IV = HASH_IV if not ('HASH_IV' in payment_conf) else payment_conf['HASH_IV']
        self.service_url = PAYUNI_SANDBOX_SERVICE_URL if self.is_sandbox else PAYUNI_SERVICE_URL

        self.url_dict['MerID'] = MERCHANT_ID
        self.url_dict['Version'] = '1.0'
        
        self.return_url = RETURN_URL
        self.back_url = CLIENT_BACK_URL

        self.merTradeNo = hashlib.sha224(str(datetime.datetime.now()).encode()).hexdigest().upper()[:24] if not ('MerTradeNo' in payment_conf) else payment_conf['MerTradeNo'] #
        self.tradeAmt = 300 if not ('TradeAmt' in payment_conf) else payment_conf['TradeAmt']
        self.prodDesc = 'Default Description' if not ('ProdDesc' in payment_conf) else payment_conf['ProdDesc']
        
        self.timestamp = int(time.time())
        
        # === SUBSCRIPTION CONFIG FOR PAYUNI ===
        if subscription:
            self.periodAmt = payment_conf['TradeAmt']
            subscriptionData = payment_conf.get('subscriptionData', {})
            self.periodAmt = self.tradeAmt
            self.periodType = PERIOD_TYPE.get(subscriptionData.get('PeriodType'), 'month')
            self.periodTimes = subscriptionData.get('ExecTimes',)
            self.fType = 'build'

            now = datetime.datetime.now()
            if self.periodType == 'week':
                self.periodDate = str(now.isoweekday())
            elif self.periodType == 'month':
                self.periodDate = str(now.day)
            elif self.periodType == 'year':
                self.periodDate = now.strftime('%Y-%m-%d')

            self.service_url = PAYUNI_SANDBOX_PERIOD_URL if self.is_sandbox else PAYUNI_PERIOD_URL
        
        
    def check_out(self, subscription=False):        
        
        encodeDict = {}
        if self.language:
            encodeDict = {'Lang': self.language}

        if subscription:
            encodeDict.update({
                'MerID': self.url_dict['MerID'],
                'MerTradeNo': self.merTradeNo,
                'PeriodAmt': self.periodAmt,
                'PeriodType': self.periodType,
                'PeriodDate': self.periodDate,
                'PeriodTimes': self.periodTimes,
                'FType': self.fType,
                'Timestamp': self.timestamp,
                'ProdDesc': self.prodDesc,
                'ReturnURL': self.return_url,
                'BackURL': self.back_url,
                'NotifyURL': self.periodReturnUrl,
            })
        else:
            encodeDict.update({
                'MerID': self.url_dict['MerID'],
                'MerTradeNo': self.merTradeNo,
                'TradeAmt': self.tradeAmt,
                'Timestamp': self.timestamp,
                'ProdDesc': self.prodDesc,
                'ReturnURL': self.return_url,
                'BackURL': self.back_url
            })

        # EncryptInfo
        urlEncode = urllib.parse.urlencode(encodeDict)
        aesCipher = AES.new(self.HASH_KEY.encode(), AES.MODE_GCM, self.HASH_IV.encode())
        ciphertext, tag = aesCipher.encrypt_and_digest(urlEncode.encode())
        encryptInfo = binascii.hexlify(base64.b64encode(ciphertext) + b':::' + base64.b64encode(tag)).decode()

        # HashInfo
        hashStr = '%s%s%s' % (self.HASH_KEY, encryptInfo, self.HASH_IV)
        hashInfo = hashlib.sha256(hashStr.encode()).hexdigest().upper()

        self.url_dict['EncryptInfo'] = encryptInfo
        self.url_dict['HashInfo'] = hashInfo

        return self.url_dict

    def gen_check_out_form(self, dict_url, auto_send=True):
        """
        Generate The Form Submission
        :param dict_url:
        :return: the html of the form
        """
        form_html = '<form id="Payuni-Form" name="payuniForm" method="post" target="_self" action="%s" style="display: none;">' % self.service_url

        for i, val in enumerate(dict_url):
            #print val, dict_url[val]
            form_html = "".join((form_html, "<input type='hidden' name='%s' value='%s' />" % (val, dict_url[val])))

        form_html = "".join((form_html, '<input type="submit" class="large" id="payment-btn" value="BUY" /></form>'))
        if auto_send:
            form_html = "".join((form_html, "<script>document.payuniForm.submit();</script>"))
        return form_html

    @classmethod
    def query_payment_info(cls, merchant_trade_no):
        """
        Implementing ...
        :param merchant_trade_no:
        :return:
        """
        logging.info('== Query the info==')
        returns = {}
        logging.info(merchant_trade_no)

        return returns
