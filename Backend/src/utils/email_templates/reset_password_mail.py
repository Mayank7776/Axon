import logging
from src.core.settings import settings
from src.utils.resend_client import send_email_via_resend

logger = logging.getLogger("axon.email.reset_password")


def _build_reset_password_html(username: str, reset_link: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Reset Your Password</title>
</head>
<body style="margin:0;padding:0;background-color:#0a0f1e;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0a0f1e;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background-color:#111827;border-radius:16px;overflow:hidden;
                      border:1px solid #1e293b;">

          <!-- Header -->
          <tr>
            <td align="center"
                style="background:linear-gradient(135deg,#0ea5e9,#6366f1);
                       padding:36px 40px 28px;">
              <h1 style="margin:0;color:#ffffff;font-size:28px;
                         font-weight:700;letter-spacing:1px;">AXON</h1>
              <p style="margin:6px 0 0;color:rgba(255,255,255,0.75);
                        font-size:13px;letter-spacing:2px;text-transform:uppercase;">
                AI-Powered Fitness
              </p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px 40px 32px;">
              <p style="margin:0 0 8px;color:#94a3b8;font-size:14px;">
                Hey <strong style="color:#e2e8f0;">{username}</strong>,
              </p>
              <p style="margin:0 0 32px;color:#94a3b8;font-size:15px;line-height:1.6;">
                We received a request to reset your Axon password.
                Click the button below to choose a new one.
                This link expires in <strong style="color:#e2e8f0;">15 minutes</strong>.
              </p>

              <!-- CTA Button -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="padding:8px 0 32px;">
                    <a href="{reset_link}"
                       style="display:inline-block;background:linear-gradient(135deg,#0ea5e9,#6366f1);
                              color:#ffffff;text-decoration:none;font-size:15px;
                              font-weight:600;padding:14px 40px;border-radius:8px;
                              letter-spacing:0.5px;">
                      Reset Password
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Fallback link -->
              <p style="margin:0 0 8px;color:#64748b;font-size:12px;">
                Button not working? Copy and paste this link into your browser:
              </p>
              <p style="margin:0 0 28px;word-break:break-all;">
                <a href="{reset_link}"
                   style="color:#38bdf8;font-size:12px;text-decoration:underline;">
                  {reset_link}
                </a>
              </p>

              <p style="margin:0;color:#64748b;font-size:13px;line-height:1.6;">
                If you did not request a password reset, ignore this email —
                your password will remain unchanged.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color:#0d1117;padding:20px 40px;
                       border-top:1px solid #1e293b;">
              <p style="margin:0;color:#475569;font-size:12px;text-align:center;">
                &copy; {settings.MAIL_FROM_NAME or "Axon"} &nbsp;|&nbsp;
                This is an automated message, please do not reply.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


async def send_reset_password_email(email: str, username: str, reset_link: str) -> None:
    """
    Sends a password reset email. Logs a warning on failure but does NOT raise —
    the caller (service layer) raises HTTPException if needed.
    """
    html = _build_reset_password_html(username, reset_link)

    success = await send_email_via_resend(
        to_email=email,
        subject="Reset Your Axon Password",
        html_content=html,
    )

    if not success:
        logger.warning("Reset password email delivery failed for %s", email)