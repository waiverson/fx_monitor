#!/usr/bin/python
# encoding:utf-8
__author__ = 'xyc'

import logging
from conf import settings
from utils import SMTPConnection

class ConsoleNotication(object):

    @classmethod
    def alert(cls, url=None, expected_code=None, code=None):
        """
        :param kwargs: 包含url, expected_code, code
        """
        if code:
            logging.error("ALERT %s returned %d, expected %d" % (url, code, expected_code))
        else:
            logging.error("ALERT FAILED TO CONNECT TO %s" % url)

    @classmethod
    def recover(cls, url):
        logging.info("BACK TO NORMAL %s" % url)

class MailNotication(object):

    @classmethod
    def send(cls, subject, msg):
        s = SMTPConnection()
        try:
            s.open()
        except Exception,e:
            logging.error(e)
            logging.error("CANNOT OPEN MAIL CONNECTION")
        pre_subject = getattr(settings, "SUBJECT_PREFIX", "alert from 51DESK AWS SERVER ")
        s.send(settings.RECIPIENTS, settings.EMAIL_HOST_USER, pre_subject + subject, msg)
        s.close()

    @classmethod
    def alert(cls, url, expected_code, code):
        if code:
            msg = "ALERT %s RETURNED %d, EXPECTED %d" % (url, code, expected_code)
        else:
            msg = "ALERT FAILED TO CONNECT TO %s" % url
        cls.send("ALERT NOTICATION", msg)

    @classmethod
    def recover(cls, url):
        logging.info("BACK TO NORMAL %s" % url)
        cls.send("BACK TO NORMAL", "%s HAS TURNED STABLE" % url)