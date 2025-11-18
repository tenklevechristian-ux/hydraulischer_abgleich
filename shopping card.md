# Einkaufsliste (Hardware-Start)

Komponenten für 4 Heizkreisverteiler (1×8 Kreise, 3×5 Kreise) mit DS18B20-Bus an GPIO4 und durchverbundenen Klemmblöcken (keine Lötarbeit nötig).

**Preise sind grobe Richtwerte (Online, Stand heute).**

| Position | Menge | Beschreibung | Stückpreis (ca.) | Gesamt (ca.) |
|---|---|---|---|---|
| ESP32-DevKitC V4 (WROOM-32) | 4 | Mikrocontroller pro Verteiler | 10 € | 40 € |
| DS18B20, wasserdicht, 1–2 m Leitung | 31 | 10 Sensoren für 8er, je 7 für die drei 5er | 2.50 € | 77.50 € |
| Pull-up Widerstand 2.2 kOhm, 1/4 W | 4 | Einer pro Bus (3V3 ↔ GPIO4) | 0.10 € | 0.40 € |
| DIN-Schaltnetzteil 230V→5V (Mean Well HDR-15-5) | 4 | 5 V/3 A, 17.5 mm Breite, Hutschiene | 12 € | 48 € |
| DIN-Schiene 35 mm + Endkappen | 2 m | Fuer 4 Netzteile + Klemmblöcke | 6 €/m | 12 € |
| Micro-USB- oder USB-C-Kabel (kurz) | 4 | 5 V vom Netzteil zum ESP32 | 4 € | 16 € |
| Push-in Verteilerblock (PTFIX-Style), 12-fach, DIN-Schiene | 12 | Je Verteiler 3 Blöcke (GND/3V3/DATA), werkseitig gebrueckt | 6 € | 72 € |

**Zwischensumme grob:** ~266 € (ohne Reserven/Versand).

Optional nuetzlich:
- Schrumpfschlauch/Isolierband fuer Kabelfuehrung
- Waermeleitpaste + Kabelbinder fuer Sensorbefestigung
- Kleine Sicherung (z.B. 1 A trae­ge auf 5 V-Seite) wenn gewuenscht

## 12-fach Klemm-Option (ohne Löten, ab Werk gebrueckt)

Ziel: je drei Leisten (GND/3V3/DATA), pro Leiste 12 Abgaenge. Du kannst pro Bus eine 12-polige “Barrier Strip”/“Lüsterklemme mit Brücke” nutzen.

- **Barrier Strip 12-polig mit Bruecken**: Schraubklemme, wird mit Metall-Jumpern durchverbunden.  
  - Reichelt: [AKL 102-12](https://www.reichelt.de/steckbare-klemme-12-polig-90-akl-102-12-p164761.html) (~3–4 €) + Bruecken [AKL 12-BR](https://www.reichelt.de/bruecke-12-polig-fuer-akl-akl-12-br-p164763.html) (~1–2 €).  
  - Alibaba: [12 position barrier strip](https://www.alibaba.com/trade/search?SearchText=12+position+barrier+strip+jumper) (~1–2 € inkl. Bruecken).  
  - Amazon.de: [“12 pol barrier strip mit jumper”](https://www.amazon.de/s?k=barrier+strip+12+jumper) (~5–8 € inkl. Bruecken).
- Pro Bus (GND/3V3/DATA) eine 12er-Leiste + ein Jumper-Set; drei Leisten decken alle Sensor-Abgaenge ab.
- Vorteil: keine Einzelklemmen, klar beschriftbar, schraubbar, sofort durchverbunden.
- **Push-in Verteilerblock (PTFIX-Style), DIN-Schiene, 12-fach**: Federzug, ab Werk durchgeschleift (ein Eingang, 11 Ausgänge), kein Löten/Schrauben.  
  - Beispiel AliExpress-Suche: [“PTFIX 12 push in din rail”](https://www.aliexpress.com/wholesale?SearchText=PTFIX+12+push+in+din+rail) (~3–6 € pro 12er-Block, oft Farben wählbar).  
- Vorteil: sehr schnell zu verkabeln, kompakt auf DIN-Schiene, kein Werkzeug außer Abisolierzange.  
- Drei Blöcke (GND/3V3/DATA) decken alle Abgänge.
- **Menge je Heizkreisverteiler**: 3 Blöcke (1× GND, 1× 3V3, 1× DATA). Bei 4 Verteilern also 12 Blöcke gesamt.

## Hinweis zur Verkabelung mit Push-in-Blöcken

- Je Verteiler drei Blöcke: GND, 3V3, DATA (GPIO4). Eingang vom ESP32 auf den gemeinsamen Eingang des Blocks, alle Sensorabgänge in die übrigen Klemmen.  
- Pull-up (2.2 kOhm) zwischen 3V3 und DATA nahe am ESP32 (kann direkt an die Leitungen gecrimpt/isteckt werden).  
- Falls Litze verwendet wird: Aderendhülsen setzen, damit die Federklemmen sauber greifen.
