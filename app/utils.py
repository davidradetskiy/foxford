import email
import imaplib
import re
import smtplib
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = "testtfoxford@yandex.ru"
password = "wxwzeofoytcbjgaz"


def read_mail(folder="inbox"):
    mail = imaplib.IMAP4_SSL("imap.yandex.ru")
    mail.login(username, password)
    mail.select(folder)
    _, messages = mail.search(None, "UNSEEN")

    mail_ids = messages[0].split()

    if mail_ids:
        emails = []
        for mail_id in mail_ids:
            _, msg_data = mail.fetch(mail_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding if encoding else "utf-8")

            body = get_email_body(msg)
            sender = decode_header(msg["From"])
            sender_email = "".join(
                part.decode(encoding if encoding else "utf-8")
                if isinstance(part, bytes)
                else part
                for part, encoding in sender
            )

            email_match = re.search(r"<(.+?)>", sender_email)
            if email_match:
                sender_email = email_match.group(1)

            emails.append(
                {"subject": subject, "body": clean_body(body), "sender": sender_email}
            )

        return emails
    else:
        return []


def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
            elif part.get_content_type() == "text/html":
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()


def clean_body(body):
    """Удалить специальные символы из тела письма."""
    return body.strip()


def reply_to_email(sender_email, original_subject, reply_body):
    """Отправить ответ на указанный адрес электронной почты."""
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = sender_email
    msg["Subject"] = f"Re: {original_subject}"

    msg.attach(MIMEText(reply_body, "plain"))

    with smtplib.SMTP("smtp.yandex.ru", 587) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)


def read_all_emails():
    """Читать письма из обеих папок: Входящие и Спам."""
    all_emails = []
    all_emails.extend(read_mail(folder="inbox"))
    all_emails.extend(read_mail(folder="Spam"))
    return all_emails


async def get_data_from_email():
    emails = read_all_emails()
    if emails:
        for email in emails:
            reply_to_email(
                email["sender"], email["subject"], "Ваше обращение зарегистрировано"
            )
    return emails
