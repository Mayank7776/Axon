import httpx  #type: ignore
import logging
from src.core.settings import settings

logger = logging.getLogger("myonix.resend")

async def send_email_via_resend(
    to_email: str | list[str],
    subject: str,
    html_content: str
) -> bool:
    """
    Sends an email using Resend's HTTP POST API.
    Handles single string recipient or a list of recipients.
    Returns True if successfully sent, False otherwise.
    """
    if not settings.RESEND_API_KEY:
        logger.warning(
            "RESEND_API_KEY is not configured in settings. "
            "Skipping email delivery to: %s", to_email
        )
        # We print it to console/logger for local developers to inspect reset links / templates
        logger.info(
            "--- EMULATED EMAIL CONTENT ---\n"
            "To: %s\n"
            "Subject: %s\n"
            "HTML Body:\n%s\n"
            "------------------------------",
            to_email, subject, html_content
        )
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    # Ensure to_email is format-compatible with Resend JSON (it expects an array of strings in lowercase)
    recipients = [to_email.lower()] if isinstance(to_email, str) else [e.lower() for e in to_email]


    # From address format
    from_name = settings.MAIL_FROM_NAME or "MyOnix-AI"
    from_email = settings.MAIL_FROM or "onboarding@resend.dev"
    
    # Resend free tier/onboarding only allows onboarding@resend.dev.
    # Standard public domains (gmail, yahoo, etc.) cannot be verified and will cause a 403.
    public_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "live.com", "icloud.com"]
    if any(domain in from_email.lower() for domain in public_domains):
        logger.warning(
            "MAIL_FROM '%s' is a public domain and cannot be verified in Resend. "
            "Using fallback sender 'onboarding@resend.dev' for sandbox delivery.",
            from_email
        )
        from_email = "onboarding@resend.dev"

    # Clean from address string
    from_address = f"{from_name} <{from_email}>"


    payload = {
        "from": from_address,
        "to": recipients,
        "subject": subject,
        "html": html_content
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=12.0
            )
            if response.status_code in [200, 201]:
                logger.info("Resend email sent successfully to %s", recipients)
                return True
            else:
                logger.error(
                    "Resend API error status %s while sending to %s. Response: %s",
                    response.status_code, recipients, response.text
                )
                return False
        except httpx.RequestError as e:
            logger.exception("HTTP transport exception while sending via Resend: %s", e)
            return False
        except Exception as e:
            logger.exception("Unexpected error while sending via Resend: %s", e)
            return False
