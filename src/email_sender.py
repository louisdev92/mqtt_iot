import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def send_alert_email(
    device_id,
    alerts
):
    """
    Envoie un email d'alerte.
    """

    smtp_host = os.getenv(
        "SMTP_HOST"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_user = os.getenv(
        "SMTP_USER"
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )

    alert_email = os.getenv(
        "ALERT_EMAIL"
    )

    # --------------------------------------
    # Vérification configuration
    # --------------------------------------

    if not smtp_host:
        print(
            "SMTP_HOST non configuré."
        )
        return

    if not smtp_user:
        print(
            "SMTP_USER non configuré."
        )
        return

    if not smtp_password:
        print(
            "SMTP_PASSWORD non configuré."
        )
        return

    if not alert_email:
        print(
            "ALERT_EMAIL non configuré."
        )
        return

    # --------------------------------------
    # Création du mail
    # --------------------------------------

    message = EmailMessage()

    message["Subject"] = (
        f"⚠️ Alerte station météo - "
        f"{device_id}"
    )

    message["From"] = smtp_user
    message["To"] = alert_email

    body = (
        "Une alerte a été détectée "
        "sur la station météo.\n\n"
    )

    body += (
        f"Capteur : {device_id}\n\n"
    )

    body += "Alertes détectées :\n"

    for alert in alerts:

        body += (
            f"- {alert}\n"
        )

    message.set_content(
        body
    )

    # --------------------------------------
    # Envoi
    # --------------------------------------

    try:

        with smtplib.SMTP(
            smtp_host,
            smtp_port
        ) as smtp:

            smtp.ehlo()

            smtp.starttls()

            smtp.ehlo()

            smtp.login(
                smtp_user,
                smtp_password
            )

            smtp.send_message(
                message
            )

        print(
            "✓ Email d'alerte envoyé."
        )

    except Exception as error:

        print(
            f"❌ Erreur email : {error}"
        )