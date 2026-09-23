import threading

from database import init_database
from mqtt_client import start_mqtt
from web import start_web


if __name__ == "__main__":

    print()
    print("======================================")
    print("      STATION MÉTÉO SENSECAP S2120")
    print("======================================")
    print()

    # ======================================
    # Initialisation de la base de données
    # ======================================

    init_database()

    # ======================================
    # Démarrage MQTT
    # ======================================

    mqtt_thread = threading.Thread(
        target=start_mqtt,
        daemon=True
    )

    mqtt_thread.start()

    # ======================================
    # Démarrage du serveur web
    # ======================================

    print()
    print("Interface web disponible sur :")
    print("http://127.0.0.1:5000")
    print()

    start_web()