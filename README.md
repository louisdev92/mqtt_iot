# test_app_iot, goudot
projet IoT goudot dÃ©montration...

```mermaid
flowchart TD

    Cap[Capteur IoT] -->|LoRa| SoM2M
    SoM2M -->|MQTT| BAL[test.mosquitto.org]
    BAL -->|MQTT| Appli[Appli visualisation]
```
