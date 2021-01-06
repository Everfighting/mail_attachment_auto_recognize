#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 5:07 下午
# @File    : send_mail.py
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import smtplib
import datetime
import os

now = datetime.datetime.now()
day1 = datetime.timedelta(days=0)
trad = now - day1
str_trad = trad.strftime('%Y-%m-%d')


class SendMail:

    def __init__(self, from_mail, to_username, username, password):
        self.From = from_mail  # 发件人
        self.to_username = to_username  # 收件人
        self.username = username
        self.password = password

    def send_mail(self, excel_path):
        # mail.qq
        server = smtplib.SMTP("smtp.qq.com", 25)
        # # mail.163
        # server = smtplib.SMTP("smtp.163.com",25)
        server.starttls()
        server.set_debuglevel(0)
        server.login(self.username, self.password)  # smtp服务器验证

        # 构造MIMEMultipart对象做为根容器
        main_msg = MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = MIMEText("附件是%s日的数据, 请查收" % str_trad)
        main_msg.attach(text_msg)

        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        for i in os.listdir(excel_path):
            file_name = os.path.join(excel_path, i)
            # 构造附件1，传送指定目录下的 excel文件
            att1 = MIMEText(open(file_name, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="{xls}"'.format(xls=i)  # filename 客户端接收到的附件名称
            main_msg.attach(att1)

        # 设置根容器属性
        main_msg['From'] = self.From
        main_msg['To'] = self.to_username  # 收件人
        main_msg['Subject'] = Header("%s日运营数据..." % str_trad)
        main_msg['Date'] = formatdate()  # 发件时间

        # 得到格式化后的完整文本
        fulltext = main_msg.as_string()

        # 用smtp发送邮件
        try:
            server.sendmail(self.From, self.to_username, fulltext)
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)
        finally:
            server.quit()


if __name__ == '__main__':
    # # mail.qq.com
    from_mail = ''
    to_username = ''
    username = ''
    password = ''  # 此处填写授权码

    file_path = r'./to_send'
    # sendmail
    send = SendMail(from_mail, to_username, username, password)
    send.send_mail(file_path)