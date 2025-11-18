# Hydraulischer Abgleich - Projektdokumentation

## Problemstellung / IST-Aufnahme

### Ausgangssituation

In einem Einfamilienhaus wurde bei einer Kernsanierung eine Wärmepumpe und im gesamten Haus Fußbodenheizung verbaut.

**Heizkreisverteiler:**
- 1x 8 Heizkreise
- 3x 5 Heizkreise
- **Gesamt: 23 Heizkreise**

### Bisherige Abgleichversuche

#### Erster Versuch (Sanitärfachmann)
Der initiale hydraulische Abgleich gemäß Berechnung des Sanitärfachmannes wurde so durchgeführt, dass alle berechneten Sollwerte ≤ 0,5 auf 0,5 eingestellt wurden, da die Skala bei kleineren Werten nicht sinnvoll einstellbar ist.

> [!warning] Problem
> Der Abgleich war damit faktisch nicht mehr vorhanden.

#### Zweiter Versuch (Hochskalierung)
Anschließend wurde per Dreisatz das Ganze so hochgerechnet, dass:
- Kleinster Wert = 0,5
- Größter Wert = 3,0

Diese hochskalierten Werte wurden an allen Heizkreisen eingestellt.

### Aktueller Zustand

- **Stellantriebe:** Nicht vorhanden – alle Heizkreise sind permanent offen
- **Wärmepumpe:** Steht auf initialer Heizkurve
- **Raumthermostat:** Nicht vorhanden
- **Temperaturregelung:** Erfolgt über Raumsolltemperatur am Innengerät

> [!note] Beobachtung
> In allen Räumen herrscht eine angenehme Temperatur. Lediglich der Wohn-/Essbereich mit großer Fensterfront fühlt sich etwas zu kühl an. Bei Erhöhung der Temperatur an der Wärmepumpe oder Erhöhung der Heizkurve wären jedoch alle anderen Räume zu warm.

---

## Der Plan

### Hardware-Komponenten

| Komponente | Anzahl | Verwendung |
|------------|--------|------------|
| ESP32 | 4 | Je ein ESP32 pro Heizkreisverteiler |
| DS18B20 | 31 | Temperatursensoren |

### Sensorplatzierung

**Pro Heizkreisverteiler:**
- 1x DS18B20 am zentralen Vorlauf
- 1x DS18B20 am zentralen Rücklauf

**Pro Heizkreis:**
- 1x DS18B20 am Rücklauf

### Datenerfassung

Die Temperaturen sollen geloggt werden in:
- **Datenbank:** InfluxDB v1 (zeitpunktbasiert)
- **Integration:** Home Assistant
- **Visualisierung:** Grafana

### Ziel: Delta-T-Analyse

Die erfassten Daten werden genutzt, um das Delta T (Temperaturdifferenz zwischen Vor- und Rücklauf) der einzelnen Heizkreise zu erfassen und darüber einen hydraulischen Abgleich durchführen zu können.

> [!info] Theorie
> In der Theorie sollte das Delta T in allen Heizkreisen identisch sein.

**Berücksichtigung von Umwelteinflüssen:**
- Unterschiedliche Fensterflächen
- Unterschiedliche ungedämmte Außenwände
- Unterschiedliche Nutzung (z.B. Kochen)

---

## Bonus: Automatisierte Empfehlungen

### Konzept

Ein Python-Script soll die Daten analysieren und Empfehlungen ausgeben, welcher Heizkreis um wie viele Umdrehungen geöffnet oder geschlossen werden soll.

### Workflow

```
Datenaufnahme → Analyse → Empfehlung → Anpassung → Datenaufnahme → ...
```

**Ziel:** In wenigen Zyklen einen perfekt abgestimmten hydraulischen Abgleich erreichen.

### Benachrichtigung

Die Empfehlungen sollen täglich per Webhook über Discord versendet werden.
