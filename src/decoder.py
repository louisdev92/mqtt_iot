def decode_signed(hex_string, divisor=1):
    """
    Convertit une valeur hexadécimale signée en nombre.
    Les données SenseCAP sont encodées en big-endian.
    """

    value = int(hex_string, 16)

    # Conversion en entier signé
    bits = len(hex_string) * 4

    if value & (1 << (bits - 1)):
        value -= 1 << bits

    return value / divisor


def decode_unsigned(hex_string, divisor=1):
    """
    Convertit une valeur hexadécimale non signée.
    """

    value = int(hex_string, 16)

    return value / divisor


def decode_s2120(payload):
    """
    Décode le payload LoRaWAN d'un SenseCAP S2120.

    Le S2120 peut utiliser les blocs :
        4A : température, humidité, luminosité, UV, vent
        4B : direction du vent, pluie, pression
        4C : rafale maximale, pluie accumulée

    Retourne un dictionnaire contenant les mesures.
    """

    payload = payload.lower().replace(" ", "")

    if not payload:
        raise ValueError("Payload vide")

    if len(payload) % 2 != 0:
        raise ValueError("Payload hexadécimal invalide")

    measurements = {}

    position = 0

    while position < len(payload):

        data_id = payload[position:position + 2]

        # --------------------------------------------------
        # 4A
        # Température
        # Humidité
        # Luminosité
        # UV
        # Vitesse du vent
        # --------------------------------------------------

        if data_id == "4a":

            # 4A + 20 caractères hexadécimaux
            data = payload[position + 2:position + 22]

            if len(data) != 20:
                raise ValueError("Bloc 4A incomplet")

            temperature = decode_signed(
                data[0:4],
                10
            )

            humidity = decode_unsigned(
                data[4:6]
            )

            illumination = decode_unsigned(
                data[6:14]
            )

            uv_index = decode_signed(
                data[14:16],
                10
            )

            wind_speed = decode_signed(
                data[16:20],
                10
            )

            measurements["temperature"] = temperature
            measurements["humidity"] = humidity
            measurements["illumination"] = illumination
            measurements["uv_index"] = uv_index
            measurements["wind_speed"] = wind_speed

            position += 22

        # --------------------------------------------------
        # 4B
        # Direction du vent
        # Pluviométrie
        # Pression atmosphérique
        # --------------------------------------------------

        elif data_id == "4b":

            # 4B + 16 caractères hexadécimaux
            data = payload[position + 2:position + 18]

            if len(data) != 16:
                raise ValueError("Bloc 4B incomplet")

            wind_direction = decode_signed(
                data[0:4]
            )

            rainfall = decode_signed(
                data[4:12],
                1000
            )

            # La valeur du protocole est en dixième
            # d'unité de pression.
            air_pressure = decode_signed(
                data[12:16],
                0.1
            )

            measurements["wind_direction"] = wind_direction
            measurements["rainfall"] = rainfall

            # Conversion en hPa
            measurements["air_pressure"] = air_pressure / 100

            position += 18

        # --------------------------------------------------
        # 4C
        # Rafale maximale
        # Pluie accumulée
        # --------------------------------------------------

        elif data_id == "4c":

            # 4C + 12 caractères hexadécimaux
            data = payload[position + 2:position + 14]

            if len(data) != 12:
                raise ValueError("Bloc 4C incomplet")

            peak_wind = decode_signed(
                data[0:4],
                10
            )

            rain_accumulation = decode_signed(
                data[4:12],
                1000
            )

            measurements["peak_wind"] = peak_wind
            measurements["rain_accumulation"] = rain_accumulation

            position += 14

        # --------------------------------------------------
        # 01 / 02 / 03
        # Anciens formats SenseCAP
        # --------------------------------------------------

        elif data_id == "01":

            data = payload[position + 2:position + 22]

            if len(data) != 20:
                raise ValueError("Bloc 01 incomplet")

            measurements["temperature"] = decode_signed(
                data[0:4],
                10
            )

            measurements["humidity"] = decode_unsigned(
                data[4:6]
            )

            measurements["illumination"] = decode_unsigned(
                data[6:14]
            )

            measurements["uv_index"] = decode_signed(
                data[14:16],
                10
            )

            measurements["wind_speed"] = decode_signed(
                data[16:20],
                10
            )

            position += 22

        elif data_id == "02":

            data = payload[position + 2:position + 18]

            if len(data) != 16:
                raise ValueError("Bloc 02 incomplet")

            measurements["wind_direction"] = decode_signed(
                data[0:4]
            )

            measurements["rainfall"] = decode_signed(
                data[4:12],
                1000
            )

            air_pressure = decode_signed(
                data[12:16],
                0.1
            )

            measurements["air_pressure"] = air_pressure / 100

            position += 18

        elif data_id == "03":

            data = payload[position + 2:position + 4]

            if len(data) != 2:
                raise ValueError("Bloc 03 incomplet")

            measurements["battery"] = decode_unsigned(data)

            position += 4

        else:

            raise ValueError(
                f"Identifiant de données inconnu : {data_id}"
            )

    return measurements