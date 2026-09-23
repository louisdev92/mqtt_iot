import sqlite3
import os
from datetime import datetime, timezone


# ==========================================
# CHEMIN DE LA BASE
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

DB_PATH = os.path.join(
    DATA_DIR,
    "weather.db"
)


# ==========================================
# CRÉATION DU DOSSIER DATA
# ==========================================

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


# ==========================================
# CONNEXION SQLITE
# ==========================================

def get_connection():

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# INITIALISATION
# ==========================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_name TEXT,

            device_type TEXT,

            temperature REAL,

            humidity REAL,

            wind_speed REAL,

            wind_direction REAL,

            peak_wind REAL,

            uv_index REAL,

            illumination REAL,

            rainfall REAL,

            rain_accumulation REAL,

            air_pressure REAL,

            rssi INTEGER,

            snr REAL,

            latitude REAL,

            longitude REAL,

            measured_at TEXT,

            created_at TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()

    print(
        f"✓ Base de données initialisée : "
        f"{DB_PATH}"
    )


# ==========================================
# ENREGISTRER UNE MESURE
# ==========================================

def save_measurement(data):

    connection = get_connection()

    cursor = connection.cursor()

    measured_at = data.get(
        "time"
    )

    if not measured_at:

        measured_at = datetime.now(
            timezone.utc
        ).isoformat()


    cursor.execute(
        """
        INSERT INTO measurements (

            device_name,
            device_type,

            temperature,
            humidity,
            wind_speed,

            wind_direction,
            peak_wind,

            uv_index,
            illumination,

            rainfall,
            rain_accumulation,

            air_pressure,

            rssi,
            snr,

            latitude,
            longitude,

            measured_at,
            created_at

        )

        VALUES (

            ?, ?,

            ?, ?, ?,

            ?, ?,

            ?, ?,

            ?, ?,

            ?,

            ?, ?,

            ?, ?,

            ?, ?

        )
        """,
        (

            data.get(
                "device_name"
            ),

            data.get(
                "device_type"
            ),

            data.get(
                "temperature"
            ),

            data.get(
                "humidity"
            ),

            data.get(
                "wind_speed"
            ),

            data.get(
                "wind_direction"
            ),

            data.get(
                "peak_wind"
            ),

            data.get(
                "uv_index"
            ),

            data.get(
                "illumination"
            ),

            data.get(
                "rainfall"
            ),

            data.get(
                "rain_accumulation"
            ),

            data.get(
                "air_pressure"
            ),

            data.get(
                "rssi"
            ),

            data.get(
                "snr"
            ),

            data.get(
                "latitude"
            ),

            data.get(
                "longitude"
            ),

            measured_at,

            datetime.now(
                timezone.utc
            ).isoformat()

        )
    )

    connection.commit()

    connection.close()

    print(
        "✓ Mesure enregistrée dans SQLite."
    )


# ==========================================
# DERNIÈRE MESURE
# ==========================================

def get_latest_measurement():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM measurements

        ORDER BY id DESC

        LIMIT 1
        """
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return None

    return dict(row)


# ==========================================
# ALIAS
# ==========================================

def get_last_measurement():

    return get_latest_measurement()


# ==========================================
# HISTORIQUE
# ==========================================

def get_history(
    hours=24
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM measurements

        WHERE datetime(measured_at)
        >= datetime('now', ?)

        ORDER BY datetime(measured_at) ASC
        """,
        (
            f"-{hours} hours",
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ==========================================
# DERNIÈRES MESURES
# ==========================================

def get_latest_measurements(
    limit=100
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM measurements

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            limit,
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in reversed(rows)
    ]


# ==========================================
# MESURES DEPUIS X HEURES
# ==========================================

def get_measurements_since(
    hours=24
):

    return get_history(
        hours
    )


# ==========================================
# STATISTIQUES
# ==========================================

def get_statistics(
    hours=24
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            MIN(temperature)
                AS temperature_min,

            MAX(temperature)
                AS temperature_max,

            AVG(temperature)
                AS temperature_avg,

            MIN(humidity)
                AS humidity_min,

            MAX(humidity)
                AS humidity_max,

            AVG(humidity)
                AS humidity_avg,

            MIN(wind_speed)
                AS wind_min,

            MAX(wind_speed)
                AS wind_max,

            AVG(wind_speed)
                AS wind_avg

        FROM measurements

        WHERE datetime(measured_at)
        >= datetime('now', ?)
        """,
        (
            f"-{hours} hours",
        )
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return {}

    return dict(row)


# ==========================================
# NOMBRE DE MESURES
# ==========================================

def get_measurement_count():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count

        FROM measurements
        """
    )

    row = cursor.fetchone()

    connection.close()

    return row["count"]


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    init_database()

    print()

    print(
        "Base SQLite prête."
    )

    print(
        f"Fichier : {DB_PATH}"
    )

    print()

    print(
        "Nombre de mesures :",
        get_measurement_count()
    )
