import os
import smtplib
import requests
from dotenv import load_dotenv
from tasks.settings_celery import app_celery
from email.message import EmailMessage

load_dotenv()

smtp_host = os.getenv('SMTP_HOST')
smtp_port = os.getenv('SMTP_PORT')
smtp_user = os.getenv('SMTP_USER')
aplication_password = os.getenv('APPLICATION_PASSWORD')


@app_celery.task
def send_email(emails_list, from_email, subject, message):
    """
    Отправка Email
    :param emails_list: на какой email
    :param from_email: с какого email
    :param subject: тема email
    :param message: текст email
    """

    with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port) as server:
        server.login(user=smtp_user, password=aplication_password)
        try:
            msg = EmailMessage()
            msg['To'] = emails_list
            msg['From'] = from_email
            msg['Subject'] = subject
            msg.set_content(message)
            server.send_message(msg)
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPException, ValueError) as ex:
            return f'{ex}'
        return 200


bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_GROUP_ID')
user_chat_id = os.getenv('USER_CHAT_ID')
recipient_list = [chat_id, user_chat_id]


@app_celery.task
def send_telegram_chat(messages):
    """
    Отправка сообщение в телеграм (отправляет в группу и в личные сообщение)
    :param messages: сообщение которое будет отправлено
    :return: возвращает статус 200 или ошибку
    """
    try:
        api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        for chat in recipient_list:
            params = {
                'chat_id': chat,
                'text': messages
            }
            requests.post(api_url, json=params)
    except Exception as ex:
        return f'{ex}'
    return 200
