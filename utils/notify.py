# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from flask import jsonify

from utils.const import MailConfig, success, message


class MailService:
    def __init__(self, to_mail_list):
        self.strFrom = MailConfig.send_mail_from
        self.strTo = to_mail_list
        self.msgRoot = MIMEMultipart('related')
        self.msgRoot['Subject'] = 'KF Message Service'
        self.msgRoot['From'] = self.strFrom
        self.msgRoot['To'] = self.strTo
        self.msgRoot.preamble = 'This is a multi-part message in MIME format.'
        self.smtp = smtplib.SMTP()
        self.smtp.connect(MailConfig.send_mail_smtp)
        self.smtp.login(MailConfig.send_mail_from, MailConfig.send_mail_password)
        self.msgAlternative = MIMEMultipart('alternative')
        self.msgRoot.attach(self.msgAlternative)

    def add_images(self, context, images):
        image_str = ""
        if images:
            for index, img in enumerate(images):
                # This example assumes the image is in the current directory
                fp = open(img, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image{}>'.format(index))
                self.msgRoot.attach(msgImage)
                image_str = image_str + '<img src="cid:image{}">'.format(index)
        # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText("<b>" + context + "</b>" + image_str, 'html')
        self.msgAlternative.attach(msgText)

    def send(self, content, image_list=None):
        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgText = MIMEText('This is the alternative plain text message.')
        self.msgAlternative.attach(msgText)
        self.add_images(content, image_list)
        self.smtp.sendmail(self.strFrom, self.strTo, self.msgRoot.as_string())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp.quit()



def image_notice(send_text, image_list):
    if not image_list:
        return jsonify({success: False, "message": "image_list params error"})

    try:
        with MailService(MailConfig.to_mail) as ms:
            ms.send(send_text, None)
        return jsonify({
            success: True,
            message: send_text
        })
    except Exception as e:
        return jsonify({success: False, message: str(e)})


mail_content = """
　  •554 HL:IPB 该IP不在网易允许的发送地址列表里；
　　•554 MI:STC 发件人当天内累计邮件数量超过限制，当天不再接受该发件人的投信。请降低发信频率；
　　•554 MI:SPB 此用户不在网易允许的发信用户列表里；
　　•554 IP in blacklist 该IP不在网易允许的发送地址列表里。
"""

if __name__ == '__main__':
    with MailService(MailConfig.to_mail) as ms:
        ms.send(mail_content, None)
