# Hydraulischer Abgleich mit ESP32 und DS18B20 Temperatursensoren

## Projektübersicht

Dieses Projekt ermöglicht die Durchführung eines hydraulischen Abgleichs einer Fußbodenheizung durch kontinuierliche Temperaturmessung aller Heizkreise mittels DS18B20 Sensoren und ESP32 Mikrocontrollern.

---

## Ist das Ganze Sinnvoll? - Technische Validierung

### Kurze Antwort: Ja, absolut!

Die Messung der Temperaturdifferenz (Delta T / Spreizung) zwischen Vor- und Rücklauf ist eine **etablierte Methode** zur Überprüfung und Optimierung des hydraulischen Abgleichs.

### Wissenschaftliche Grundlage

1. **Delta T als Indikator**: Die Temperaturspreizung zeigt direkt, wie viel Wärme ein Heizkreis aufnimmt
2. **Gleiches Delta T = Abgeglichenes System**: Wenn alle Heizkreise das gleiche Delta T aufweisen, fließt durch jeden Kreis proportional zu seiner Heizlast Wasser
3. **Ungleiches Delta T = Hydraulische Probleme**:
   - Zu niedriges Delta T → Zu viel Durchfluss (überversorgt)
   - Zu hohes Delta T → Zu wenig Durchfluss (unterversorgt)

### Optimale Werte für Wärmepumpe mit Fußbodenheizung

| Parameter | Optimaler Wert |
|-----------|----------------|
| **Vorlauftemperatur** | 28-35°C |
| **Rücklauftemperatur** | 23-30°C |
| **Delta T (Spreizung)** | **5-7 Kelvin** |

> **Wichtig**: Bei Wärmepumpen ist eine niedrige Spreizung (5K) effizienter als bei Gas-/Ölheizungen (15-20K), da jedes Kelvin höhere Vorlauftemperatur ca. 2,5% mehr Stromverbrauch bedeutet.

### Korrektur der Zielsetzung

**Ursprüngliche Annahme**: "Delta T im gesamten Haus normalisieren"

**Korrekte Zielsetzung**:
- **Alle Heizkreise sollten ein ähnliches Delta T aufweisen** (z.B. alle bei 5K ± 0,5K)
- Das Delta T muss NICHT in jedem Raum identisch sein, aber sollte sich in einem engen Band bewegen
- Räume mit höherem Wärmebedarf (große Fenster) haben automatisch mehr Durchfluss, aber das gleiche Delta T

### Grenzen der Methode

Diese DIY-Lösung kann:
- ✅ Ungleichmäßige Durchflussverteilung aufdecken
- ✅ Über-/Unterversorgung einzelner Kreise identifizieren
- ✅ Iterative Optimierung ermöglichen

Diese Lösung kann NICHT:
- ❌ Die absolute Heizlast eines Raumes berechnen
- ❌ Einen vollständigen Abgleich nach VDI 2073 ersetzen
- ❌ Fehlende Stellventile kompensieren

---

## Hardware-Auswahl

### ESP32 Board-Vergleich

| Eigenschaft | ESP32-32D (CP2102) | ESP32-DevKitC V4 (WROOM-32) | ESP32-S3 (N8R2/N16R8) |
|-------------|--------------------|-----------------------------|------------------------|
| **Prozessor** | Dual-Core LX6 @ 240MHz | Dual-Core LX6 @ 240MHz | Dual-Core LX7 @ 240MHz |
| **RAM** | 520 KB | 520 KB | 512 KB + PSRAM |
| **GPIOs** | ~26 | ~34 | 45 |
| **USB** | CP2102 (Seriell) | CP2102/CH340 (Seriell) | USB OTG nativ |
| **Bluetooth** | 4.2 + BLE | 4.2 + BLE | 5.0 (LE) |
| **Preis** | ~5-8€ | ~8-12€ | ~12-18€ |
| **Empfehlung** | ⭐⭐⭐ Budget | ⭐⭐⭐⭐ **Empfohlen** | ⭐⭐ Overkill |

### Empfehlung: ESP32-DevKitC V4 (WROOM-32)

**Warum:**
- Ausreichend GPIOs für 8+ DS18B20 Sensoren
- Gute Community-Unterstützung und ESPHome-Kompatibilität
- Zuverlässiger CP2102 USB-Chip
- Beste Preis-Leistung für dieses Projekt

**ESP32-S3 ist Overkill weil:**
- USB OTG wird nicht benötigt
- AI-Beschleunigung wird nicht genutzt
- Mehr GPIOs als nötig
- Höherer Preis ohne Mehrwert

### Einkaufsliste

| Komponente | Anzahl | Beschreibung |
|------------|--------|--------------|
| ESP32-DevKitC V4 | 4 | Je einer pro Heizkreisverteiler |
| DS18B20 (wasserdicht) | 31 | Mit Kabel (mind. 1m) |
| Widerstand 2.2kΩ | 4 | Pull-up Widerstand (1 pro ESP32) |
| Streifenrasterplatine | 4 | Ca. 5x7cm |
| Stiftleisten | 4 | Zum Aufstecken des ESP32 |
| USB-Kabel Micro/Type-C | 4 | Stromversorgung |
| USB-Netzteil 5V/2A | 4 | Oder vorhandene Netzteile |
| Schraubklemmen 3-polig | Nach Bedarf | Für einfache Verdrahtung |

---

## Verkabelung

### Pull-up Widerstand

**Standard-Wert: 4.7kΩ**

Für dieses Projekt empfehle ich **2.2kΩ** weil:
- Bis zu 8 Sensoren pro Bus
- Kabellängen von 1-3m
- 3.3V Logik des ESP32

> Bei Problemen mit Messfehlern: Widerstand auf 1.8kΩ reduzieren

### DS18B20 Pinbelegung

```
┌─────────────────┐
│    DS18B20      │
│   (Vorderseite) │
│                 │
│  GND  DQ  VDD   │
│   │   │    │    │
└───┼───┼────┼────┘
    │   │    │
  Schwarz Gelb Rot
    │   │    │
   GND Data VCC
```

### Schaltplan für Stripboard

```
                    ESP32 DevKitC V4
                   ┌─────────────────┐
                   │                 │
              GND ─┤GND         3V3 ├─ VCC (3.3V)
                   │                 │
             GPIO4─┤GPIO4            │
                   │                 │
                   └─────────────────┘
                        │
                        │ DATA (GPIO4)
                        │
                   ┌────┴────┐
                   │         │
              ┌────┴─────────┴────┐
              │    2.2kΩ          │
              │    Pull-up        │
              └─────────┬─────────┘
                        │
                       VCC (3.3V)


    Stripboard Layout (Sternverkabelung):

    ═══════════════════════════════════════════════════
    VCC  ●───●───●───●───●───●───●───●───● (alle VCC verbunden)
    ═══════════════════════════════════════════════════
    DATA ●───●───●───●───●───●───●───●───● (alle DATA verbunden)
    ═══════════════════════════════════════════════════
    GND  ●───●───●───●───●───●───●───●───● (alle GND verbunden)
    ═══════════════════════════════════════════════════
         │   │   │   │   │   │   │   │
        S1  S2  S3  S4  S5  S6  S7  S8

    S1 = Vorlauf zentral
    S2 = Rücklauf zentral
    S3-S8 = Rückläufe der einzelnen Heizkreise
```

### Detaillierte Verdrahtung

1. **Stripboard vorbereiten**:
   - 3 horizontale Leiterbahnen für VCC, DATA, GND
   - Lötpunkte für jeden Sensor vorbereiten

2. **ESP32 anschließen**:
   - GND → GND-Leitung
   - 3V3 → VCC-Leitung
   - GPIO4 → DATA-Leitung

3. **Pull-up Widerstand**:
   - 2.2kΩ zwischen VCC-Leitung und DATA-Leitung
   - **Nur EIN Widerstand pro Bus!**

4. **Sensoren anschließen**:
   - Jeder DS18B20: VCC, DATA, GND parallel verbinden
   - Kabel ggf. mit Schraubklemmen für einfaches Tauschen

### GPIO-Empfehlungen

| Verwendung | GPIO | Hinweis |
|------------|------|---------|
| 1-Wire Bus | GPIO4 | Gut geeignet, keine Einschränkungen |
| Alternative | GPIO14, GPIO13, GPIO27 | Ebenfalls problemlos |
| **NICHT verwenden** | GPIO0, GPIO2, GPIO15 | Boot-Pins |
| **NICHT verwenden** | GPIO6-11 | Flash-Speicher |

---

## Software-Installation

### Methode 1: ESPHome (Empfohlen)

ESPHome ist die beste Lösung für Home Assistant Integration und einfache Wartung.

#### Schritt 1: ESPHome installieren

```bash
# Mit pip
pip install esphome

# Oder als Home Assistant Add-on
# Settings → Add-ons → ESPHome
```

#### Schritt 2: Erstkonfiguration erstellen

```yaml
# heizkreis_og.yaml
esphome:
  name: heizkreis-og
  friendly_name: "Heizkreisverteiler OG"

esp32:
  board: esp32dev
  framework:
    type: arduino

# WiFi-Konfiguration
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Fallback-Hotspot bei Verbindungsproblemen
  ap:
    ssid: "Heizkreis-OG-Fallback"
    password: "fallback123"

# API für Home Assistant
api:
  encryption:
    key: !secret api_key

# OTA Updates
ota:
  - platform: esphome
    password: !secret ota_password

# Logging
logger:
  level: DEBUG

# 1-Wire Bus definieren
one_wire:
  - platform: gpio
    pin: GPIO4

# Sensoren werden später hinzugefügt
```

#### Schritt 3: Erstes Flashen via USB

```bash
# Kompilieren und Flashen
esphome run heizkreis_og.yaml

# Wähle den seriellen Port (z.B. /dev/ttyUSB0)
```

#### Schritt 4: Sensor-Adressen ermitteln

Nach dem Flashen zeigt das Log alle gefundenen Sensoren:

```
[12:34:56][D][dallas.sensor:084]: Found sensors:
[12:34:56][D][dallas.sensor:086]:   0x1c0000031edd2a28
[12:34:56][D][dallas.sensor:086]:   0x500000031eddff28
[12:34:56][D][dallas.sensor:086]:   0x7a0000031ede1228
...
```

#### Schritt 5: Vollständige Konfiguration

```yaml
# heizkreis_og.yaml - Vollständig
esphome:
  name: heizkreis-og
  friendly_name: "Heizkreisverteiler OG"

esp32:
  board: esp32dev
  framework:
    type: arduino

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
    ssid: "Heizkreis-OG-Fallback"
    password: "fallback123"

api:
  encryption:
    key: !secret api_key

ota:
  - platform: esphome
    password: !secret ota_password

logger:
  level: INFO

# 1-Wire Bus
one_wire:
  - platform: gpio
    pin: GPIO4

# Temperatursensoren
sensor:
  # Zentrale Sensoren
  - platform: dallas_temp
    address: 0x1c0000031edd2a28  # ANPASSEN!
    name: "OG Vorlauf"
    id: og_vorlauf
    unit_of_measurement: "°C"
    accuracy_decimals: 2

  - platform: dallas_temp
    address: 0x500000031eddff28  # ANPASSEN!
    name: "OG Rücklauf Zentral"
    id: og_ruecklauf_zentral
    unit_of_measurement: "°C"
    accuracy_decimals: 2

  # Heizkreis 1 - Bad
  - platform: dallas_temp
    address: 0x7a0000031ede1228  # ANPASSEN!
    name: "OG HK1 Bad Rücklauf"
    id: og_hk1_bad
    unit_of_measurement: "°C"
    accuracy_decimals: 2

  # Heizkreis 2 - Schlafzimmer
  - platform: dallas_temp
    address: 0x8b0000031ede3428  # ANPASSEN!
    name: "OG HK2 Schlafzimmer Rücklauf"
    id: og_hk2_schlafzimmer
    unit_of_measurement: "°C"
    accuracy_decimals: 2

  # Weitere Heizkreise analog hinzufügen...

  # Berechnete Delta-T Werte
  - platform: template
    name: "OG HK1 Bad Delta T"
    id: og_hk1_delta_t
    unit_of_measurement: "K"
    accuracy_decimals: 2
    lambda: |-
      return id(og_vorlauf).state - id(og_hk1_bad).state;
    update_interval: 60s

  - platform: template
    name: "OG HK2 Schlafzimmer Delta T"
    id: og_hk2_delta_t
    unit_of_measurement: "K"
    accuracy_decimals: 2
    lambda: |-
      return id(og_vorlauf).state - id(og_hk2_schlafzimmer).state;
    update_interval: 60s

  # WiFi Signal
  - platform: wifi_signal
    name: "OG WiFi Signal"
    update_interval: 60s
```

### Methode 2: Tasmota

Falls ESPHome nicht gewünscht:

1. **Web-Installer**: https://tasmota.github.io/install/
2. **Konfiguration**: `Configuration → Configure Module → DS18B20`

> **Hinweis**: Tasmota unterstützt standardmäßig nur 8 DS18B20 Sensoren.

---

## Home Assistant & InfluxDB Integration

### Home Assistant

Die ESPHome-Geräte werden automatisch erkannt. Aktiviere InfluxDB-Export:

```yaml
# configuration.yaml
influxdb:
  api_version: 1
  host: localhost
  port: 8086
  database: home_assistant
  default_measurement: state
  include:
    entities:
      - sensor.og_vorlauf
      - sensor.og_ruecklauf_zentral
      - sensor.og_hk1_bad_ruecklauf
      - sensor.og_hk1_bad_delta_t
      # Alle weiteren Sensoren...
  tags:
    source: homeassistant
```

### Grafana Dashboard

Beispiel-Query für Delta T Vergleich:

```sql
SELECT mean("value") FROM "°C"
WHERE ("entity_id" =~ /delta_t/)
AND time >= now() - 24h
GROUP BY time(5m), "entity_id" fill(null)
```

---

## Inbetriebnahme-Workflow

### Phase 1: Hardware-Aufbau

1. [ ] Alle Komponenten beschaffen
2. [ ] Stripboards für jeden Verteiler vorbereiten
3. [ ] DS18B20 Sensoren an Leitungen anschließen
4. [ ] Pull-up Widerstände einlöten
5. [ ] ESP32 aufstecken und verkabeln

### Phase 2: Software-Setup

1. [ ] ESPHome installieren
2. [ ] Basis-Konfiguration erstellen
3. [ ] Erstes Flashen durchführen
4. [ ] Sensor-Adressen aus Log notieren
5. [ ] Vollständige Konfiguration mit Adressen erstellen
6. [ ] OTA-Update durchführen

### Phase 3: Montage

1. [ ] DS18B20 am Vorlauf des Verteilers befestigen (mit Kabelbinder + Wärmeleitpaste)
2. [ ] DS18B20 am zentralen Rücklauf befestigen
3. [ ] DS18B20 an jedem Heizkreis-Rücklauf befestigen
4. [ ] **Wichtig**: Sensoren isolieren (Armaflex o.ä.) um Umgebungseinflüsse zu minimieren
5. [ ] ESP32 an USB-Netzteil anschließen

### Phase 4: Datenerfassung

1. [ ] 24-48 Stunden Daten sammeln
2. [ ] In Grafana visualisieren
3. [ ] Plausibilität prüfen (Vorlauf > alle Rückläufe)

### Phase 5: Analyse & Optimierung

1. [ ] Python-Script ausführen
2. [ ] Empfehlungen umsetzen
3. [ ] Erneut 24-48h messen
4. [ ] Iterieren bis alle Delta T ähnlich sind

---

## Troubleshooting

### Sensor wird nicht erkannt

- [ ] Verkabelung prüfen (VCC, GND, DATA)
- [ ] Pull-up Widerstand vorhanden?
- [ ] Widerstandswert reduzieren (2.2kΩ → 1.8kΩ)
- [ ] Kabellänge reduzieren zum Testen

### Fehlerhafte Messwerte

- [ ] "85°C" = Sensor nicht korrekt initialisiert → Neustart
- [ ] "-127°C" = Kommunikationsfehler → Verkabelung
- [ ] Schwankende Werte = EMV-Störungen → Kabel besser verlegen

### WiFi-Verbindung instabil

- [ ] Signal prüfen (< -80dBm ist problematisch)
- [ ] WiFi-Repeater in Nähe des ESP32
- [ ] Externe Antenne (bei ESP32-WROOM-32U)

---

## Physikalischer Hintergrund

### Formel für Wärmeleistung

```
Q = ṁ × c × ΔT

Q  = Wärmeleistung [W]
ṁ  = Massenstrom [kg/s]
c  = Spezifische Wärmekapazität Wasser (4186 J/kg·K)
ΔT = Temperaturdifferenz [K]
```

### Interpretation

Bei **konstantem Delta T** (z.B. 5K) liefern alle Heizkreise proportional zu ihrem Durchfluss Wärme. Wenn alle Kreise gleichmäßig abgeglichen sind, haben sie alle das gleiche Delta T.

| Beobachtung | Bedeutung | Maßnahme |
|-------------|-----------|----------|
| Delta T zu hoch (>7K) | Zu wenig Durchfluss | Ventil öffnen |
| Delta T zu niedrig (<4K) | Zu viel Durchfluss | Ventil schließen |
| Delta T optimal (5-6K) | Richtig eingestellt | Beibehalten |

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
