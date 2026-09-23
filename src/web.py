from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

from threading import Lock

from database import (
    get_latest_measurement,
    get_history,
    get_statistics
)


# ==========================================
# Flask
# ==========================================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# ==========================================
# Données actuelles
# ==========================================

latest_data = {}

data_lock = Lock()


# ==========================================
# Mise à jour des données
# ==========================================

def update_data(data):

    global latest_data

    with data_lock:

        latest_data = data.copy()


# ==========================================
# Récupération des données actuelles
# ==========================================

def get_data():

    with data_lock:

        memory_data = latest_data.copy()

    # Si Flask vient de démarrer mais que
    # la base contient déjà des mesures,
    # on récupère la dernière.

    if not memory_data:

        return get_latest_measurement()

    return memory_data


# ==========================================
# Page principale
# ==========================================

@app.route("/")
def index():

    data = get_data()

    return render_template(
        "index.html",
        data=data
    )


# ==========================================
# API dernière mesure
# ==========================================

@app.route("/api/data")
def api_data():

    return jsonify(
        get_data()
    )


# ==========================================
# API historique
# ==========================================

@app.route("/api/history")
def api_history():

    try:

        hours = float(
            request.args.get(
                "hours",
                24
            )
        )

    except ValueError:

        hours = 24

    # Limitation pour éviter des requêtes
    # énormes.

    hours = max(
        1,
        min(hours, 168)
    )

    history = get_history(
        hours
    )

    return jsonify(
        history
    )


# ==========================================
# API statistiques
# ==========================================

@app.route("/api/statistics")
def api_statistics():

    try:

        hours = float(
            request.args.get(
                "hours",
                24
            )
        )

    except ValueError:

        hours = 24

    hours = max(
        1,
        min(hours, 168)
    )

    statistics = get_statistics(
        hours
    )

    return jsonify(
        statistics
    )


# ==========================================
# Serveur Flask
# ==========================================

def start_web():

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )