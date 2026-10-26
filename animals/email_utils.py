
import requests
from django.conf import settings


def send_adoption_email(recipient_email, subject, message):
    """Send an adoption notification to Mailtrap Sandbox."""

    token = settings.MAILTRAP_API_TOKEN
    inbox_id = settings.MAILTRAP_INBOX_ID

    if not token:
        return False, "Mailtrap API token is missing from .env."

    if not inbox_id:
        return False, "Mailtrap inbox ID is missing from .env."

    if not recipient_email:
        return False, "The applicant has no email address."

    url = f"https://sandbox.api.mailtrap.io/api/send/{inbox_id}"

    headers = {
        "Api-Token": token,
        "Content-Type": "application/json",
    }

    payload = {
        "from": {
            "email": "sandbox@example.com",
            "name": "Animal Rescue Team",
        },
        "to": [{"email": recipient_email}],
        "subject": subject,
        "text": message,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=15,
        )

        if response.status_code in (200, 201, 202):
            return True, "Email captured by Mailtrap Sandbox."

        return False, (
            f"Mailtrap Sandbox returned HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    except requests.RequestException as error:
        return False, f"Email request failed: {error}"
