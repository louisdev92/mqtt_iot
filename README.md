# 🌦️ Station météo IoT — SenseCAP S2120

Application Python permettant de récupérer, décoder, enregistrer et afficher les données d'une station météo SenseCAP S2120 via MQTT.

Le projet permet également de conserver un historique des mesures dans une base SQLite, d'afficher les données sur une interface web et de déclencher des alertes par e-mail lorsque certains seuils sont dépassés.

---

## 📋 Fonctionnalités

- 📡 Réception des données du capteur via MQTT
- 🌦️ Récupération des mesures météorologiques
- 🌡️ Température
- 💧 Humidité
- 💨 Vitesse du vent
- 🧭 Direction du vent
- 🌪️ Rafale maximale
- 🔵 Pression atmosphérique
- ☀️ Indice UV
- 💡 Luminosité
- 🌧️ Pluie
- 📍 Latitude et longitude du capteur
- 🗺️ Affichage de la localisation sur une carte
- 💾 Enregistrement des mesures dans SQLite
- 📈 Historique des mesures
- 📊 Statistiques des mesures
- 📉 Graphiques d'évolution
- 🚨 Gestion de seuils
- 📧 Envoi d'e-mails d'alerte
- 🌐 Interface web avec Flask
- 🕐 Affichage de l'heure
- 🔄 Actualisation automatique des données

---

## 🛠️ Technologies utilisées

- Python
- Paho MQTT
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js
- Leaflet
- OpenStreetMap
- SMTP

---

## 📁 Structure du projet

```text
mqtt_iot/
│
├── src/
│   ├── main.py
│   ├── mqtt_client.py
│   ├── database.py
│   ├── web.py
│   ├── email_sender.py
│   ├── decoder.py
│   └── alerts.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── data/
│   └── weather.db
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
