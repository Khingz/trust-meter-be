from fastapi_mail import FastMail, MessageSchema
from .config import conf
from typing import List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Optional
import os
from jinja2.exceptions import TemplateNotFound

class EmailService:
    def __init__(self):
        loader_path = os.path.join(os.path.dirname(__file__), "templates")
        self.fm = FastMail(conf)
        self.template_env = Environment(
            loader=FileSystemLoader(loader_path),
            autoescape=select_autoescape(['html', 'xml'])
        )


    def render_template(self, template_name: str, context: dict):
        """Render a template with the given context."""
        try:
            template = self.template_env.get_template(template_name)
            return template.render(context)
        except TemplateNotFound:
            raise ValueError(f"Template {template_name} not found.")
    
    async def send_email(self,
                         subject: str,
                         recipients: List[str],
                         body: Optional[str] = None,
                         subtype: str = "html",
                         template_name: Optional[str] = None,
                         template_context: Optional[dict] = None):

        if template_name and template_context:
            body = self.render_template(template_name, template_context)

        if not body:
            raise ValueError("Email body or template must be provided.")
        
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=subtype
        )
        await self.fm.send_message(message)
