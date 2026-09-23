🌦️ Dashboard Météo

Dashboard web permettant de récupérer et d'afficher les données d'une station météo ou d'un capteur connecté.

L'interface permet de consulter les données météorologiques en temps réel ainsi que leur historique.

📋 Fonctionnalités

🌡️ Température

💧 Humidité

💨 Vitesse du vent

📊 Pression atmosphérique

📈 Historique des mesures

🔘 Sélection de la période d'historique

🗺️ Localisation de la station

🛰️ Carte interactive

🟢 État de connexion de la station

🕐 Heure en temps réel

📡 Informations du capteur

📱 Interface responsive

📊 Graphiques des données

🛠️ Technologies

HTML5

CSS3

JavaScript

Python

Chart.js

Leaflet

📁 Structure du projet
weather-dashboard/
│
├── main.py
├── requirements.txt
├── index.html
│
├── css/
│   └── style.css
│
├── js/
│   └── app.js
│
├── assets/
│
└── README.md

🚀 Installation et démarrage
1. Cloner le projet
git clone <URL_DU_PROJET>


Puis entrer dans le dossier :

cd weather-dashboard

2. Installer les dépendances
pip install -r requirements.txt

3. Lancer le projet
python main.py


Une fois le serveur lancé, ouvrir dans un navigateur l'adresse indiquée dans le terminal.

📊 Données affichées
Donnée	Unité
Température	°C
Humidité	%
Vent	km/h
Pression	hPa
Latitude	°
Longitude	°
📈 Historique

L'utilisateur peut sélectionner différentes périodes afin de consulter l'évolution des données météorologiques.

Exemples :

24 heures

7 jours

30 jours

Le bouton sélectionné est automatiquement mis en évidence.

🗺️ Localisation

La position de la station météo est affichée sur une carte interactive avec Leaflet.

📱 Responsive

L'interface est adaptée :

💻 Ordinateur

📱 Mobile

📲 Tablette

🔄 Fonctionnement
Station météo
      │
      ▼
Récupération des données
      │
      ▼
Traitement
      │
      ▼
Dashboard
   ┌──┼──┐
   ▼  ▼  ▼
  📊 📈 🗺️

📌 Objectif

L'objectif du projet est de fournir une interface simple et moderne permettant de consulter les données d'une station météo et leur évolution dans le temps.

👨‍💻 Auteur

Projet réalisé dans le cadre du développement d'un dashboard de station météo connectée.