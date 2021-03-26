import logging

from .http import Http
from django.conf import settings
from django.core.mail import EmailMessage

import zmail

logger = logging.getLogger('views')


class Notice(object):

    @staticmethod
    def send_sms(phones, content):
        """
        发送短信
        """
        headers = {"Token": settings.HERMES_TOKEN}
        for phone in phones.split(','):
            data = {'phone': phone, 'content': content}
            ret, err = Http.post(settings.HERMES_API + '/send/sms/', data, headers=headers)
            if err:
                logger.error(err)
        return 'done'

    @staticmethod
    def send_html_mail(tos, subject, content, fromer=None, cc=None, bcc=None):
        """
        发送html邮件
        """
        if fromer:
            _fromer = '%s<%s>' % (fromer, settings.EMAIL_HOST_USER)
        else:
            _fromer = settings.EMAIL_HOST_USER

        msg = EmailMessage(subject, content, _fromer, tos.split(','))
        msg.content_subtype = "html"
        if cc: msg.cc = cc.split(',')
        if bcc: msg.bcc = bcc.split(',')
        ret = msg.send(fail_silently=True)
        if ret == 1:
            ret = True
        else:
            ret = False
        return ret

    @staticmethod
    def send_mail_nocs(mail_receiver, mail_name, mail_message):
        mail_server = zmail.server(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.EMAIL_HOST)
        mail_content = {
            'subject': mail_name,
            'content_text': mail_message,
        }
        try:
            res = mail_server.send_mail(mail_receiver, mail_content)
            if res:
                return True
        except Exception as e:
            print(e)
            return False
