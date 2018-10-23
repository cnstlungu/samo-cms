"""
Contains the logic for the creation of the confirmation email to be sent.
"""

from flask_mail import Message

from samo.core import app, mail, celery


@celery.task(bind=True)
def send_email(recipients, subject, template):
    """
    Sends an email being provided a destination, subject and template.
    :rtype: void
    :param recipients:
    :param subject:
    :param template:
    """
    msg = Message(
        subject,
        recipients=[recipients],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
