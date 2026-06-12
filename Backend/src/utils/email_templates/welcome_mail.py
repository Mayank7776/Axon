from src.utils.resend_client import send_email_via_resend


# Welcome Email
async def send_welcome_email(
    email: str,
    username: str
):

    html = f"""
    <div style="
        background-color:#0f172a;
        padding:40px;
        font-family:Arial;
        color:white;
    ">

        <div style="
            max-width:600px;
            margin:auto;
            background:#111827;
            border-radius:16px;
            padding:40px;
        ">

            <h1 style="
                color:#3b82f6;
                text-align:center;
                margin-bottom:20px;
            ">
                Welcome to MyOnix-AI 🚀
            </h1>

            <h2 style="color:white;">
                Hello {username},
            </h2>

            <p style="font-size:16px; line-height:1.7;">
                Your account has been successfully created.
            </p>

            <p style="font-size:16px; line-height:1.7;">
                Welcome to <b>MyOnix-AI</b> — your AI-powered fitness companion.
            </p>

            <div style="
                background:#1e293b;
                padding:20px;
                border-radius:12px;
                margin:25px 0;
            ">
                <p style="margin:0; font-size:16px;">
                    🥗 Ask Onix-AI about your personalized diet plans
                </p>

                <p style="margin-top:10px; font-size:16px;">
                    💪 Get workout recommendations & fitness guidance
                </p>

                <p style="margin-top:10px; font-size:16px;">
                    🔥 Start your fitness journey with us today
                </p>
            </div>

            <div style="text-align:center; margin:30px 0;">
                <a href="https://myonix-ai.com"
                    style="
                        background:#3b82f6;
                        color:white;
                        padding:14px 24px;
                        border-radius:10px;
                        text-decoration:none;
                        font-weight:bold;
                    ">
                    Start Exploring
                </a>
            </div>

            <hr style="margin:30px 0; border-color:#374151;" />

            <p style="
                font-size:12px;
                color:#9ca3af;
                text-align:center;
            ">
                © 2026 MyOnix-AI. All rights reserved.
            </p>

        </div>

    </div>
    """

    await send_email_via_resend(
        to_email=email,
        subject="Welcome to MyOnix-AI 🚀",
        html_content=html
    )
