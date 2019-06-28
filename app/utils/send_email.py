#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2019/6/28 15:59
#@Author: xws
#@File  : send_email.py


# 第三方 SMTP 服务
import smtplib
from email.header import Header
from email.mime.text import MIMEText

mail_host = "smtp.126.com"  # 设置服务器
mail_user = "xwsftst@126.com"  # 用户名
mail_pass = "yahong940316"  # 口令

sender = 'xwsftst<xwsftst@126.com>'
receivers = ['739650977@qq.com', 'xwsftst@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

mail_msg = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
"""

subject = 'Lucky SMTP 邮件测试'
message = MIMEText(mail_msg, 'html', 'utf-8')
# message['From'] = Header("Lucky_admin", 'utf-8')
message['From'] = sender
message['To'] = ';'.join(receivers)
# message['To'] = Header("测试", 'utf-8')
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
