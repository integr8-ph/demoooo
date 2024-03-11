from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema

from src.ctrm.config.settings import EmailSettings
from src.ctrm.helpers.constants import EmailSubject, EmailTemplates
from src.ctrm.schemas.emails import NewAccount


def _send_bg_email(
    bg_tasks: BackgroundTasks, message: MessageSchema, template_name: str
):
    fm = FastMail(EmailSettings())

    bg_tasks.add_task(
        fm.send_message,
        message=message,
        template_name=template_name,
    )


def send_email(
    bg_tasks: BackgroundTasks,
    email: str,
    body: dict,
    subject: str,
    template_name: str,
):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=body,
        subtype="html",
    )

    _send_bg_email(bg_tasks, message, template_name)


def send_new_account_email(client: dict, bg_tasks: BackgroundTasks):
    new_account = NewAccount(**client, link="http://localhost:8000/docs")
    send_email(
        bg_tasks=bg_tasks,
        email=new_account.email,
        body=new_account.model_dump(),
        subject=EmailSubject.NEW_ACCOUNT,
        template_name=EmailTemplates.NEW_ACCOUNT,
    )
