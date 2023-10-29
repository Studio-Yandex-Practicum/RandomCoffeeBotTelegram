from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def render_email_message(subject, context, from_email, to, template):
    """Render email from html template."""
    html_body = render_to_string(template, context)
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=to,
    )
    email.attach_alternative(html_body, "text/html")
    return email
