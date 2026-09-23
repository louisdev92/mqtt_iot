🌦️ Dashboard Météo

Dashboard web permettant de récupérer, afficher et suivre en temps réel les données d'une station météo / d'un capteur connecté.

L'interface présente les principales mesures météorologiques sous forme de cartes, de graphiques et d'informations détaillées.

📋 Fonctionnalités

🌡️ Affichage de la température

💧 Affichage de l'humidité

💨 Affichage de la vitesse du vent

📊 Affichage de la pression atmosphérique

📈 Historique des mesures

🔘 Sélection de différentes périodes d'historique

🗺️ Affichage de la localisation de la station

🛰️ Carte interactive avec Leaflet

🟢 Indication de l'état de connexion de la station

🕐 Affichage de l'heure en temps réel

📡 Affichage des informations du capteur

📱 Interface responsive pour ordinateur, tablette et mobile

⏳ Gestion des états de chargement et d'attente

📊 Visualisation des données sous forme de graphiques

🖥️ Aperçu

Le dashboard est organisé en plusieurs parties :

🌤️ Données principales

Les principales informations météorologiques sont affichées sous forme de cartes :

Température

Humidité

Vent

Pression atmosphérique

Chaque carte dispose d'un indicateur visuel permettant d'identifier rapidement le type de donnée.

📊 Mesures

Une section permet d'afficher différentes mesures provenant du capteur.

📈 Historique

Les données enregistrées peuvent être consultées sur différentes périodes grâce aux boutons de sélection.

Exemple :

24 heures

7 jours

30 jours

Le bouton sélectionné est automatiquement mis en évidence avec la classe CSS active.

🗺️ Localisation

La station météo peut être localisée sur une carte interactive grâce à Leaflet.

Les informations de localisation peuvent notamment contenir :

Latitude

Longitude

Adresse

Position de la station

📡 Informations du capteur

Une section dédiée permet d'afficher les informations techniques de la station ou du capteur.

🧱 Structure du projet

Exemple d'organisation :

weather-dashboard/
│
├── index.html
│
├── css/
│   └── style.css
│
├── js/
│   ├── app.js
│   ├── weather.js
│   └── chart.js
│
├── assets/
│   ├── images/
│   └── icons/
│
└── README.md

⚙️ Technologies utilisées
Front-end

HTML5

CSS3

JavaScript

CSS Grid

CSS Flexbox

Responsive Design

Bibliothèques

Chart.js pour les graphiques

Leaflet pour la carte interactive

🔄 Fonctionnement

Le fonctionnement général de l'application est le suivant :

        Station météo / Capteur
                 │
                 ▼
        Récupération des données
                 │
                 ▼
          Traitement des données
                 │
                 ▼
          Dashboard JavaScript
                 │
        ┌────────┼─────────┐
        ▼        ▼         ▼
   Cartes météo Graphiques Carte
        │        │         │
        └────────┼─────────┘
                 ▼
              Affichage

📥 Récupération des données

Les données météorologiques sont récupérées depuis la source configurée dans le projet.

Les données peuvent notamment contenir :

{
    "temperature": 21.5,
    "humidity": 58,
    "wind": 12.4,
    "pressure": 1015.2
}


Les valeurs récupérées sont ensuite utilisées pour mettre à jour automatiquement l'interface.

📊 Récupération et affichage des données

Le JavaScript récupère les données puis met à jour les différents éléments du dashboard.

Exemple :

async function getWeatherData() {

    const response = await fetch("/api/weather");

    if (!response.ok) {
        throw new Error("Impossible de récupérer les données");
    }

    const data = await response.json();

    displayWeatherData(data);
}


Puis les données sont affichées dans l'interface :

function displayWeatherData(data) {

    document.querySelector("#temperature").textContent =
        `${data.temperature} °C`;

    document.querySelector("#humidity").textContent =
        `${data.humidity} %`;

    document.querySelector("#wind").textContent =
        `${data.wind} km/h`;

    document.querySelector("#pressure").textContent =
        `${data.pressure} hPa`;
}

🔘 Gestion des boutons d'historique

Les boutons permettent de sélectionner la période d'affichage.

Lorsqu'un bouton est sélectionné, la classe active est ajoutée automatiquement.

function setActiveHistoryButton(button) {

    document
        .querySelectorAll(".history-buttons button")
        .forEach(btn => {
            btn.classList.remove("active");
        });

    button.classList.add("active");
}


Exemple HTML :

<div class="history-buttons">

    <button
        class="active"
        data-period="24h">
        24 h
    </button>

    <button
        data-period="7d">
        7 jours
    </button>

    <button
        data-period="30d">
        30 jours
    </button>

</div>

📈 Graphiques

Les graphiques sont générés avec Chart.js.

Ils permettent de visualiser l'évolution des mesures dans le temps.

Exemple :

const chart = new Chart(ctx, {
    type: "line",

    data: {
        labels: [],
        datasets: [
            {
                label: "Température",
                data: [],
                borderColor: "#2563eb",
                backgroundColor:
                    "rgba(37, 99, 235, 0.12)",
                tension: 0.4,
                fill: true
            }
        ]
    },

    options: {
        responsive: true,

        maintainAspectRatio: false
    }
});

🗺️ Carte interactive

La localisation est affichée avec Leaflet.

Exemple :

const map = L.map("weather-map")
    .setView([45.0, 4.8], 12);

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


Un marqueur peut ensuite être ajouté :

L.marker([latitude, longitude])
    .addTo(map)
    .bindPopup("Station météo")
    .openPopup();

🎨 Interface

Le design utilise principalement :

Une palette bleu / bleu nuit

Des cartes avec coins arrondis

Des ombres légères

Des dégradés

Des animations discrètes

Une interface responsive

Les couleurs principales sont :

--primary: #2563eb;
--primary-dark: #1d4ed8;
--success: #22c55e;
--danger: #ef4444;
--purple: #8b5cf6;

📱 Responsive Design

Le dashboard est adapté aux différentes tailles d'écran :

Ordinateur
    │
    ├── Dashboard en grille
    ├── Graphiques larges
    └── Carte large

Tablette
    │
    ├── Grille adaptée
    └── Graphiques redimensionnés

Mobile
    │
    ├── Cartes empilées
    ├── Boutons adaptés
    ├── Graphiques redimensionnés
    └── Carte adaptée à l'écran


Des media queries CSS permettent d'adapter automatiquement l'affichage.

🚀 Installation
1. Cloner le projet
git clone

2. Installer les requirements

3. Lancer le projet via run 'main.py'


🔧 Configuration

Selon l'installation, les paramètres de connexion à la station météo ou à l'API peuvent être définis dans le fichier JavaScript prévu à cet effet.

Exemple :

const API_URL = "/api/weather";


Modifier cette valeur selon l'adresse de l'API utilisée.

⚠️ Gestion des erreurs

L'application doit gérer les situations suivantes :

Station hors ligne

API inaccessible

Données invalides

Absence de données

Erreur réseau

Temps de réponse trop long

Exemple :

try {

    const response = await fetch(API_URL);

    if (!response.ok) {
        throw new Error("Erreur API");
    }

    const data = await response.json();

    displayWeatherData(data);

} catch (error) {

    console.error(
        "Erreur lors de la récupération des données :",
        error
    );
}

🔄 Mise à jour automatique

Les données peuvent être actualisées périodiquement.

Exemple :

getWeatherData();

setInterval(
    getWeatherData,
    60000
);


Dans cet exemple, les données sont récupérées toutes les 60 secondes.

📂 Données affichées
Donnée	Unité	Description
Température	°C	Température mesurée
Humidité	%	Humidité relative
Vent	km/h	Vitesse du vent
Pression	hPa	Pression atmosphérique
Latitude	°	Latitude de la station
Longitude	°	Longitude de la station
🔐 Sécurité

Si le projet utilise une API nécessitant une clé d'authentification, celle-ci ne doit pas être directement publiée dans le dépôt Git.

Ne pas faire :

const API_KEY = "ma-cle-secrete";


Préférer une variable d'environnement ou une configuration côté serveur.

🛠️ Améliorations possibles

Plusieurs fonctionnalités peuvent être ajoutées par la suite :

🌧️ Prévisions météorologiques

🌅 Lever et coucher du soleil

🌬️ Direction du vent

🌧️ Précipitations

☀️ Indice UV

📅 Historique plus détaillé

🔔 Alertes météorologiques

📱 Progressive Web App (PWA)

🌙 Mode sombre

📤 Export des données en CSV

📊 Comparaison de plusieurs mesures

🔌 Détection automatique de la station

📡 Indicateur de qualité de connexion

📌 Objectif du projet

L'objectif est de proposer une interface simple, moderne et responsive permettant de consulter facilement les données provenant d'une station météo ou d'un système de capteurs.

Le dashboard centralise les informations importantes afin de permettre une lecture rapide des conditions météorologiques actuelles et de leur évolution dans le temps.

👨‍💻 Auteur

Projet réalisé dans le cadre d'un projet de développement d'un dashboard de station météo connectée.

📄 Licence

Ce projet peut être distribué et modifié selon les conditions définies par la licence du projet.