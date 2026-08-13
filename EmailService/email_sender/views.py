import logging
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

# ==============================================================================
# EMAIL SERVICE CONTROLLER / VIEW
# ==============================================================================
# INTEGRATION INSTRUCTIONS FOR EXTERNAL PROJECTS:
# 
# 1. Microservice / HTTP API Integration:
#    If connecting another frontend or backend project via HTTP/REST:
#    Send a POST request to this view's endpoint with payload:
#    - email: recipient email address
#    - subject (optional): email subject line
#    - message (optional): email body content
#
# 2. Reusable Helper Function (Python/Django project integration):
#    You can extract `dispatch_test_email(recipient_email, subject, message)` into a 
#    standalone utility module (e.g., `email_sender.utils`) and call it directly from
#    any python app.
# ==============================================================================

def dispatch_test_email(recipient_email, subject=None, message=None):
    """
    Core reusable helper to send emails.
    Can be imported directly into other Django/Python modules.
    
    Args:
        recipient_email (str): Target email address.
        subject (str, optional): Subject line.
        message (str, optional): Body text.
    Returns:
        bool: True if sent successfully, False otherwise.
    """
    email_subject = subject or "Test Email from EmailService"
    email_body = message or (
        "Hello!\n\n"
        "This is a test email sent from the EmailService application.\n"
        "If you are receiving this, your email dispatch configuration is working correctly!\n\n"
        "Best regards,\n"
        "EmailService Team"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'noreply@emailservice.com'))

    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
        raise e


def send_email(request):
    """
    Web view handling form submission to send a test email to the user-provided address.
    """
    status_message = None
    status_type = None # 'success' or 'error'
    email_input = ""

    if request.method == "POST":
        email_input = request.POST.get("email", "").strip()

        if not email_input:
            status_message = "Please enter a valid email address."
            status_type = "error"
        else:
            try:
                dispatch_test_email(recipient_email=email_input)
                status_message = f"Test email successfully sent to {email_input}!"
                status_type = "success"
            except Exception as exc:
                status_message = f"Failed to send email: {str(exc)}"
                status_type = "error"

    return render(request, "email_sender/email.html", {
        "status_message": status_message,
        "status_type": status_type,
        "email_input": email_input,
    })