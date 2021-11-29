from datetime import datetime, timedelta
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import jwt
from decouple import config
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
import smtplib


def generate_token(email=None, token_time=None):
    exp_time = datetime.now() + timedelta(days=1)
    JWT_PAYLOAD = {
        "email": email,
        "exp": exp_time
    }
    jwt_token = jwt.encode(JWT_PAYLOAD, config('SECRET_KEY'), algorithm='HS256')
    return jwt_token


def decode_token(token):

    payload = jwt.decode(token, config('SECRET_KEY'), algorithms='HS256')

    return payload


def send_mail(subject, template, data):
    context = {}
    context["name"] = data["name"]

    app_url = config('APP_URL')
    if template == "register-success.html":
        token = generate_token(data["email"], None, 2880).decode('utf-8')
        context["login_url"] = app_url + "business/login"
        context["verify_link"] = app_url + "business/account-verification/"
        context["token"] = token
    elif template == "reset-pass.html":
        context["path"] = app_url + "business/reset-password/"
        context["token"] = data["token"]


    html_body = render_to_string(template, context)

    to_email = data["email"]

    msg = MIMEMultipart()
    msg.set_unixfrom('author')
    msg['From'] = "Online Deals <" + config('ADMIN_EMAIL') + ">"
    msg['To'] = to_email
    msg['Subject'] = subject
    part2 = MIMEText(html_body, 'html')
    msg.attach(part2)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    url = os.path.join(BASE_DIR, 'static/images/logo.png')
    img_data = open(url, 'rb').read()
    msImage = MIMEImage(img_data)
    msImage.add_header('Content-ID', '<image1>')
    msg.attach(msImage)

    if template == "register-success.html":
        url = os.path.join(BASE_DIR, 'static/images/checked.png')
        img_data1 = open(url, 'rb').read()
        msImage1 = MIMEImage(img_data1)
        msImage1.add_header('Content-ID', '<image2>')
        msg.attach(msImage1)

    mailserver = smtplib.SMTP_SSL(config('SMTP_EMAIL_SERVER'), 465)
    mailserver.ehlo()

    mailserver.login(config('ADMIN_EMAIL'), config('EMAIL_PASSWORD'))

    mailserver.sendmail(config('ADMIN_EMAIL'), msg['To'], msg.as_string())

    mailserver.quit()
    return HttpResponse("Mail Send", status=200)
