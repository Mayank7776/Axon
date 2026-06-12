import logging
from src.core.settings import settings
from src.utils.resend_client import send_email_via_resend

logger = logging.getLogger("axon.email.otp")


def _build_otp_html(username: str, otp: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Your Login OTP</title>
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
                Use the OTP below to log in to your Axon account.
                It is valid for <strong style="color:#e2e8f0;">10 minutes</strong>.
              </p>

              <!-- OTP Box -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center"
                      style="background-color:#0f172a;border:1px solid #1e293b;
                             border-radius:12px;padding:28px 0;">
                    <p style="margin:0 0 8px;color:#64748b;font-size:12px;
                               letter-spacing:3px;text-transform:uppercase;">
                      One-Time Password
                    </p>
                    <p style="margin:0;color:#38bdf8;font-size:42px;
                               font-weight:700;letter-spacing:12px;">
                      {otp}
                    </p>
                  </td>
                </tr>
              </table>

              <p style="margin:28px 0 0;color:#64748b;font-size:13px;line-height:1.6;">
                If you did not request this, you can safely ignore this email.
                Someone may have entered your email by mistake.
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


async def send_login_otp_email(email: str, username: str, otp: str) -> None:
    """
    Sends a login OTP email. Logs a warning on failure but does NOT raise —
    the caller (service layer) is responsible for raising HTTPException if needed.
    """
    html = _build_otp_html(username, otp)

    success = await send_email_via_resend(
        to_email=email,
        subject="Your Axon Login OTP",
        html_content=html,
    )

    if not success:
        logger.warning("OTP email delivery failed for %s", email)