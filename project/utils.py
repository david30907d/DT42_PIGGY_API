"""
line function
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def notify_line_message(sess, token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = {"message": msg}
    resp = sess.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload
    )
    return resp.status_code


def send_gmail(email_subject, email_from, email_to, email_text, email_app_password):
    content = MIMEMultipart()
    content["subject"] = email_subject
    content["from"] = email_from
    content["to"] = email_to
    content.attach(MIMEText(email_text))
    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_from, email_app_password)
            smtp.send_message(content)
        except smtplib.SMTPAuthenticationError as err:
            print(err)
