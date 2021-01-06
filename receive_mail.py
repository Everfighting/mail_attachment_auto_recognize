#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/29 6:07 下午
# @File    : receive_mail.py
import email
import imaplib
import os


class FetchEmail():
    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=1)

    def close_connection(self):
        self.connection.close()

    def save_attachment(self, msg, download_folder="received"):
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()

            att_path = os.path.join(os.path.dirname(__file__), download_folder, filename)
            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path

    def fetch_unread_messages(self):
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].decode('utf-8').split(' '):
                try:
                    ret, data = self.connection.fetch(message, '(RFC822)')
                except:
                    print("No new emails to read.")
                    self.close_connection()
                    break
                msg = email.message_from_bytes(data[0][1])
                self.save_attachment(msg)
                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS', '\\Seen')
            return emails
        self.error = "Failed to retreive emails."
        return emails

    def parse_email_address(self, email_address):
        return email.utils.parseaddr(email_address)


if __name__ == '__main__':
    mail_server = 'imap.qq.com'
    username = '903601682'
    password = 'hdypatutgdvcbdig'

    flag = True
    while flag:
        fetch_email = FetchEmail(mail_server, username, password)
        emails = fetch_email.fetch_unread_messages()
        print("邮件收取中。。。")
        if emails:
            flag = False