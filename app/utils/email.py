from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app.ext import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, template, **kwargs):
    app = current_app._get_current_object()

    msg = Message(subject=app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=app.config['MAIL_RECIPIENTS'],
                  html=render_template(template + '.html', **kwargs))
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    return thr
