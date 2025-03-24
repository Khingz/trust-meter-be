from fastapi import BackgroundTasks
from app.email.mail_service import EmailService
from typing import List, Optional

email_service = EmailService()

def send_email_in_background(
    background_tasks: BackgroundTasks,
    subject: str,
    recipients: List[str],
    body: Optional[str] = None,
    template_name: Optional[str] = None,
    template_context: Optional[dict] = None
):
    background_tasks.add_task(email_service.send_email, subject=subject, recipients=recipients, body=body, template_name=template_name, template_context=template_context)
