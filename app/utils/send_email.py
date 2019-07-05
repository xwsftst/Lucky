#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/6/28 15:59
#@Author: xws
#@File  : send_email.py


# 第三方 SMTP 服务
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from flask import current_app


def send_email(app, project_name, build_no, status, starttime, endtime, report_url, log):

    mail_host = app.config['MAIL_SERVER']  # 设置服务器
    mail_user = app.config['MAIL_USERNAME']  # 用户名
    mail_pass = app.config['MAIL_PASSWORD']  # 口令

    sender = app.config['FLASKY_MAIL_SENDER']
    receivers = app.config['MAIL_RECIPIENTS']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_msg = """Hello, 测试消息来啦<hr>
                    项目名称：%s<hr>
                    构建编号: %s<hr>
                    构建状态: %s<hr>
                    开始时间: %s<hr>
                    结束时间: %s<hr>
                    详细报告: <a href='%s'>%s</a><hr>
                    构建日志: <br>%s<hr><br><br>
                    (本邮件是程序自动下发的，请勿回复！)""" % (project_name,
                                              build_no,
                                              status,
                                              starttime,
                                              endtime,
                                              report_url, report_url,
                                              log)

    subject = 'Lucky 通知消息'
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = ';'.join(receivers)
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, 'xwsftst@126.com', message.as_string())
        print("邮件发送成功")
        smtpObj.quit()

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
