# -*- coding: utf-8 -*-
# 通过 SMTP 把 testpage.pdf 作为附件发送到打印机专属邮箱（Epson Email Print）
import os, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

host = os.environ['SMTP_HOST']
port = int(os.environ.get('SMTP_PORT', '465'))
user = os.environ['SMTP_USER']
pwd  = os.environ['SMTP_PASS']
to   = os.environ['PRINTER_EMAIL']

msg = MIMEMultipart()
msg['From'] = user
msg['To'] = to                       # 收件人只允许一个，否则 Email Print 不打印
msg['Subject'] = 'Epson Nozzle Test'
msg.attach(MIMEText('每周自动打印，防止喷头堵墨。', 'plain', 'utf-8'))

with open('testpage.pdf', 'rb') as f:
    part = MIMEApplication(f.read(), 'pdf', Name='testpage.pdf')
part.add_header('Content-Disposition', 'attachment', filename='testpage.pdf')
msg.attach(part)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(host, port, context=ctx) as s:
    s.login(user, pwd)
    s.send_message(msg)

print('EMAIL SENT to', to)
