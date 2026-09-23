import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from decoder import decode_s2120
from alerts import check_thresholds
from email_sender import send_alert_email
from database import save_measurement
from web import update_data


# ==========================================
# Chargement du fichier .env
# ==========================================

load_dotenv()


# ==========================================
# Configuration MQTT
# ==========================================

MQTT_BROKER = os.getenv(
    "MQTT_BROKER",
    "test.mosquitto.org"
)

MQTT_PORT = int(
    os.getenv(
        "MQTT_PORT",
        "1883"
    )
)

MQTT_TOPIC = os.getenv(
    "MQTT_TOPIC",
    "cci/SenseCAP"
)


# ==========================================
# Connexion MQTT
# ==========================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    print()
    print("======================================")
    print("          CONNEXION MQTT")
    print("======================================")

    print(
        f"Résultat : {reason_code}"
    )

    if reason_code == 0:

        print(
            f"✓ Connexion réussie à : "
            f"{MQTT_BROKER}:{MQTT_PORT}"
        )

        try:

            result = client.subscribe(
                MQTT_TOPIC
            )

            if result[0] == mqtt.MQTT_ERR_SUCCESS:

                print(
                    f"✓ Abonnement au topic : "
                    f"{MQTT_TOPIC}"
                )

            else:

                print(
                    "❌ Impossible de s'abonner "
                    f"au topic : {MQTT_TOPIC}"
                )

        except Exception as error:

            print(
                f"❌ Erreur abonnement MQTT : "
                f"{error}"
            )

    else:

        print(
            "❌ Échec de la connexion MQTT"
        )


# ==========================================
# Réception d'un message MQTT
# ==========================================

def on_message(
    client,
    userdata,
    msg
):

    print()
    print("======================================")
    print("        NOUVEAU MESSAGE MQTT")
    print("======================================")

    print(
        f"Topic : {msg.topic}"
    )


    # ======================================
    # Décodage du message
    # ======================================

    try:

        message = msg.payload.decode(
            "utf-8"
        )

    except UnicodeDecodeError as error:

        print(
            f"❌ Impossible de décoder "
            f"le message : {error}"
        )

        return


    # ======================================
    # Conversion JSON
    # ======================================

    try:

        data = json.loads(
            message
        )

    except json.JSONDecodeError as error:

        print(
            f"❌ JSON invalide : {error}"
        )

        print(
            f"Message reçu : {message}"
        )

        return


    print(
        f"Données reçues : {data}"
    )


    # ======================================
    # CAS 1
    #
    # Données déjà décodées
    #
    # Exemple :
    #
    # {
    #   "device_id": "S2120_01",
    #   "temperature": 25.5,
    #   "humidity": 50,
    #   "wind_speed": 3.2
    # }
    # ======================================

    if "temperature" in data:

        print()
        print(
            "✓ Format : données déjà décodées"
        )


        # ----------------------------------
        # Récupération des mesures
        # ----------------------------------

        measurements = {

            "temperature": data.get(
                "temperature"
            ),

            "humidity": data.get(
                "humidity"
            ),

            "wind_speed": data.get(
                "wind_speed"
            ),

            "wind_direction": data.get(
                "wind_direction"
            ),

            "peak_wind": data.get(
                "peak_wind"
            ),

            "uv_index": data.get(
                "uv_index"
            ),

            "illumination": data.get(
                "illumination"
            ),

            "rainfall": data.get(
                "rainfall"
            ),

            "rain_accumulation": data.get(
                "rain_accumulation"
            ),

            "air_pressure": data.get(
                "air_pressure"
            )
        }


        # ----------------------------------
        # Informations du capteur
        # ----------------------------------

        device_name = data.get(
            "device_id",
            "S2120"
        )

        device_type = data.get(
            "deviceTypeName",
            "SenseCAP S2120"
        )


        # ----------------------------------
        # Données complètes
        # ----------------------------------

        web_data = {

            **measurements,

            "device_name": device_name,

            "device_type": device_type,

            "time": data.get(
                "time",
                ""
            ),

            "rssi": data.get(
                "rssi"
            ),

            "snr": data.get(
                "snr"
            ),

            "latitude": data.get(
                "latitude"
            ),

            "longitude": data.get(
                "longitude"
            )
        }


        # ----------------------------------
        # Mise à jour du site
        # ----------------------------------

        update_data(
            web_data
        )


        # ----------------------------------
        # Enregistrement SQLite
        # ----------------------------------

        try:

            save_measurement(
                web_data
            )

        except Exception as error:

            print(
                f"❌ Erreur SQLite : {error}"
            )


        print()
        print(
            "🌐 Données envoyées au site web"
        )

        print(
            "💾 Données enregistrées dans SQLite"
        )


        # ----------------------------------
        # Affichage
        # ----------------------------------

        if measurements[
            "temperature"
        ] is not None:

            print(
                f"🌡️ Température : "
                f"{measurements['temperature']} °C"
            )


        if measurements[
            "humidity"
        ] is not None:

            print(
                f"💧 Humidité : "
                f"{measurements['humidity']} %"
            )


        if measurements[
            "wind_speed"
        ] is not None:

            print(
                f"💨 Vent : "
                f"{measurements['wind_speed']}"
            )


        # ----------------------------------
        # Vérification des seuils
        # ----------------------------------

        alerts = check_thresholds(

            temperature=measurements[
                "temperature"
            ],

            humidity=measurements[
                "humidity"
            ],

            wind_speed=measurements[
                "wind_speed"
            ]
        )


        # ----------------------------------
        # Gestion des alertes
        # ----------------------------------

        if alerts:

            print()
            print(
                "⚠️ =================================="
            )
            print(
                "⚠️         ALERTE CAPTEUR"
            )
            print(
                "⚠️ =================================="
            )

            for alert in alerts:

                print(
                    f"⚠️ {alert}"
                )


            try:

                send_alert_email(

                    device_id=device_name,

                    alerts=alerts
                )

                print(
                    "✓ Email d'alerte envoyé."
                )

            except Exception as error:

                print(
                    f"❌ Erreur email : {error}"
                )

        else:

            print()
            print(
                "✓ Aucune alerte"
            )


        return


    # ======================================
    # CAS 2
    #
    # Message SenseCAP avec payload
    # ======================================

    if "payload" in data:

        print()
        print(
            "✓ Format : payload SenseCAP"
        )


        payload = data.get(
            "payload"
        )


        if not payload:

            print(
                "❌ Le payload est vide."
            )

            return


        print(
            f"Payload : {payload}"
        )


        # ----------------------------------
        # Décodage SenseCAP
        # ----------------------------------

        try:

            measurements = decode_s2120(
                payload
            )

        except Exception as error:

            print()
            print(
                f"❌ Erreur décodage SenseCAP : "
                f"{error}"
            )

            return


        # ----------------------------------
        # Informations capteur
        # ----------------------------------

        device_name = data.get(
            "deviceName",
            "SenseCAP S2120"
        )

        device_type = data.get(
            "deviceTypeName",
            "SenseCAP S2120"
        )


        # ----------------------------------
        # Données complètes
        # ----------------------------------

        web_data = {

            **measurements,

            "device_name": device_name,

            "device_type": device_type,

            "time": data.get(
                "time",
                ""
            ),

            "rssi": data.get(
                "rssi"
            ),

            "snr": data.get(
                "snr"
            ),

            "latitude": data.get(
                "latitude"
            ),

            "longitude": data.get(
                "longitude"
            )
        }


        # ----------------------------------
        # Mise à jour du site
        # ----------------------------------

        update_data(
            web_data
        )


        # ----------------------------------
        # Enregistrement SQLite
        # ----------------------------------

        try:

            save_measurement(
                web_data
            )

        except Exception as error:

            print(
                f"❌ Erreur SQLite : {error}"
            )


        print()
        print(
            "🌐 Données envoyées au site web"
        )

        print(
            "💾 Données enregistrées dans SQLite"
        )

        print(
            f"Mesures : {measurements}"
        )


        # ----------------------------------
        # Vérification des seuils
        # ----------------------------------

        alerts = check_thresholds(

            temperature=measurements.get(
                "temperature"
            ),

            humidity=measurements.get(
                "humidity"
            ),

            wind_speed=measurements.get(
                "wind_speed"
            )
        )


        # ----------------------------------
        # Alertes
        # ----------------------------------

        if alerts:

            print()
            print(
                "⚠️ =================================="
            )
            print(
                "⚠️         ALERTE CAPTEUR"
            )
            print(
                "⚠️ =================================="
            )

            for alert in alerts:

                print(
                    f"⚠️ {alert}"
                )


            try:

                send_alert_email(

                    device_id=device_name,

                    alerts=alerts
                )

                print(
                    "✓ Email d'alerte envoyé."
                )

            except Exception as error:

                print(
                    f"❌ Erreur email : {error}"
                )

        else:

            print()
            print(
                "✓ Aucune alerte"
            )


        return


    # ======================================
    # Format inconnu
    # ======================================

    print()
    print(
        "⚠️ Format MQTT inconnu."
    )

    print(
        f"Contenu : {data}"
    )


# ==========================================
# Démarrage MQTT
# ==========================================

def start_mqtt():

    print()
    print(
        f"Connexion à "
        f"{MQTT_BROKER}:{MQTT_PORT}..."
    )


    # ======================================
    # Création client
    # ======================================

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2
    )


    # ======================================
    # Callbacks
    # ======================================

    client.on_connect = on_connect

    client.on_message = on_message


    # ======================================
    # Connexion
    # ======================================

    try:

        client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            60
        )

    except Exception as error:

        print()
        print(
            f"❌ Erreur de connexion MQTT : "
            f"{error}"
        )

        return


    # ======================================
    # Démarrage
    # ======================================

    print()
    print(
        "Client MQTT démarré."
    )

    print(
        "En attente des données..."
    )

    print()


    # ======================================
    # Boucle MQTT
    # ======================================

    client.loop_forever()