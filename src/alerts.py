import os

from dotenv import load_dotenv


load_dotenv()


# ==========================================
# Seuils
# ==========================================

TEMP_MAX = float(
    os.getenv(
        "TEMP_MAX",
        "35"
    )
)

HUMIDITY_MAX = float(
    os.getenv(
        "HUMIDITY_MAX",
        "80"
    )
)

WIND_MAX = float(
    os.getenv(
        "WIND_MAX",
        "15"
    )
)


def check_thresholds(
    temperature=None,
    humidity=None,
    wind_speed=None
):
    """
    Vérifie les mesures du capteur.

    Retourne une liste d'alertes.
    """

    alerts = []

    # --------------------------------------
    # Température
    # --------------------------------------

    if temperature is not None:

        if temperature > TEMP_MAX:

            alerts.append(
                f"Température trop élevée : "
                f"{temperature:.1f} °C "
                f"(seuil : {TEMP_MAX:.1f} °C)"
            )

    # --------------------------------------
    # Humidité
    # --------------------------------------

    if humidity is not None:

        if humidity > HUMIDITY_MAX:

            alerts.append(
                f"Humidité trop élevée : "
                f"{humidity:.1f} % "
                f"(seuil : {HUMIDITY_MAX:.1f} %)"
            )

    # --------------------------------------
    # Vent
    # --------------------------------------

    if wind_speed is not None:

        if wind_speed > WIND_MAX:

            alerts.append(
                f"Vent trop important : "
                f"{wind_speed:.1f} "
                f"(seuil : {WIND_MAX:.1f})"
            )

    return alerts