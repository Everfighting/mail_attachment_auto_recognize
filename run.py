#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 4:21 下午
# @File    : run.py
import time
import configparser
from receive_mail import FetchEmail
from extract_content import extract_content
from send_mail import SendMail
from loguru import logger

config = configparser.ConfigParser()
config.read('./config.ini', encoding='utf-8')


def main_process():

    # 1. 调用receive_mail.py
    # 下载对应邮箱的附件图片，下载到对应的文件夹 received
    receiver_mail_server = config['receiver']['mail_server']
    receiver_username = config['receiver']['username']
    receiver_password = config['receiver']['password']
    logger.info("Receive from mail_server is :{}, username is :{}!",
                receiver_mail_server, receiver_username, feature="f-strings")

    flag = True
    while flag:
        try:
            fetch_email = FetchEmail(receiver_mail_server, receiver_username, receiver_password)
            emails = fetch_email.fetch_unread_messages()
            logger.info("Receiving from mail_server...please wait...")
            if emails:
                flag = False
                logger.info("Receive mail attachment success!")
            time.sleep(1)
        except Exception as e:
            logger.debug("Receive mail attachment error, error is {}!", e, feature="f-strings")

    # 2. 调用extract_content.py
    # 对下载的图片进行识别，识别后内容生成xls
    try:
        save_dir_path = "to_send"
        extract_content(save_dir_path)
        logger.info("Extract mail attachment success!")
    except Exception as e:
        logger.debug("Extract mail attachment error, error is {}!", e, feature="f-strings")

    # 3. 调用sendmail.py
    # 将生成的xls发送到对应的邮箱列表
    sender_mail_server = config['sender']['sender_mail_server']
    to_username = config['sender']['to_username']
    sender_username = config['sender']['sender_username']
    sender_password = config['sender']['sender_password']  # 此处填写授权码

    logger.info("Send mail from sender_mail_server is :{}, sender_username is :{}, to_username is :{}!",
                sender_mail_server, sender_username, to_username, feature="f-strings")

    try:
        send = SendMail(sender_mail_server, to_username, sender_username, sender_password)
        send.send_mail('./to_send')
        logger.info("Send extract xls success!")
    except Exception as e:
        logger.debug("Send extract xls error, error is {}!", e, feature="f-strings")


if __name__ == '__main__':
    main_process()