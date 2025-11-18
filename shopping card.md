# Einkaufsliste (Hardware-Start)

Komponenten für 4 Heizkreisverteiler (1×8 Kreise, 3×5 Kreise) mit DS18B20-Bussen an GPIO4 und Bus-Abgriffen auf Streifenraster.

**Preise sind grobe Richtwerte (Stand: typisch Onlinepreise). Links als Beispiel/Produkt-Suche.**

| Position | Menge | Beschreibung | Reichelt (ca.) | Alibaba (ca.) | Amazon.de (ca.) |
|---|---|---|---|---|---|
| ESP32-DevKitC V4 (WROOM-32) | 4 | Mikrocontroller pro Verteiler | [~9 EUR](https://www.reichelt.de/esp32-development-board-esp32-devkitc-v4-p267759.html) | [~4–6 EUR](https://www.alibaba.com/trade/search?SearchText=ESP32+DevKitC+V4) | [~10–12 EUR](https://www.amazon.de/s?k=ESP32+DevKitC+V4) |
| DS18B20, wasserdicht, 1–2 m Leitung | 31 | 10 Sensoren für 8er, je 7 für die drei 5er | [~3 EUR/Stk](https://www.reichelt.de/temperatursensor-ds18b20-to-92-ds-18b20-p89615.html) | [~1–1.5 EUR/Stk](https://www.alibaba.com/trade/search?SearchText=DS18B20+waterproof) | [~2–3 EUR/Stk](https://www.amazon.de/s?k=DS18B20+wasserdicht) |
| Pull-up Widerstand 2.2 kOhm, 1/4 W | 4 | Einer pro Bus (3V3 ↔ GPIO4) | [~0.10 EUR/Stk](https://www.reichelt.de/widerstand-kohleschicht-2-2-kohm-250-mw-1-4w-5--1-4w-2-2k-p1147.html) | [~0.02 EUR/Stk](https://www.alibaba.com/trade/search?SearchText=2.2k+resistor+1%2F4w) | [~0.10 EUR/Stk](https://www.amazon.de/s?k=2.2k+Widerstand+1%2F4W) |
| Streifenrasterplatine ca. 5×7 cm | 4 | Je eine pro ESP32 für Sammelschienen | [~1.50 EUR](https://www.reichelt.de/lochrasterplatine-70x50mm-hartpapier-fr4-1-6mm-h25pr050-p8452.html) | [~0.30–0.50 EUR](https://www.alibaba.com/trade/search?SearchText=stripboard+5x7cm) | [~1–2 EUR](https://www.amazon.de/s?k=Streifenraster+5x7cm) |
| Stiftleisten 2×19 (oder 2×20) 2.54 mm | 4 Saetze | Zum Aufstecken des ESP32 auf das Board | [~0.40 EUR/Satz](https://www.reichelt.de/?ACTION=446&LA=446&nbc=1&q=stiftleiste+2x20+2%2C54) | [~0.05–0.10 EUR/Satz](https://www.alibaba.com/trade/search?SearchText=2x20+pin+header+2.54mm) | [~0.50–1 EUR/Satz](https://www.amazon.de/s?k=2x20+Pin+Header+2.54mm) |
| Schraubklemmen 3-polig, 3.5 mm Raster | 35 | 10× fuer 8er, je 7× fuer die drei 5er (GND/3V3/DATA parallel) | [~0.35 EUR/Stk](https://www.reichelt.de/?ACTION=446&LA=446&nbc=1&q=Printklemme+3+pol+3%2C5mm) | [~0.08–0.12 EUR/Stk](https://www.alibaba.com/trade/search?SearchText=3+pin+3.5mm+screw+terminal) | [~0.30–0.50 EUR/Stk](https://www.amazon.de/s?k=3+pol+Schraubklemme+3.5mm) |
| Litze 0.25–0.34 mm2 (AWG24–22), Silikon | 1 Rolle | Bus-Schienen (GND/3V3/GPIO4) zu den Klemmen | [~8 EUR/10 m](https://www.reichelt.de/?ACTION=446&LA=446&nbc=1&q=Silikonlitze+0%2C25) | [~3–5 EUR/10 m](https://www.alibaba.com/trade/search?SearchText=silicone+wire+24awg) | [~7–10 EUR/10 m](https://www.amazon.de/s?k=Silikonlitze+AWG24) |
| DIN-Schaltnetzteil 230V→5V (Mean Well HDR-15-5) | 4 | 5 V/3 A, 17.5 mm Breite, Hutschiene | [~11–13 EUR](https://www.reichelt.de/meanwell-hdr-15-5-schaltnetzteil-15-w-5-v-3-a-hdr-15-5-p233943.html) | [~7–9 EUR](https://www.alibaba.com/trade/search?SearchText=HDR-15-5) | [~12–15 EUR](https://www.amazon.de/s?k=HDR-15-5) |
| DIN-Schiene 35 mm + Endkappen | nach Bedarf | Fuer sichere Montage der Netzteile | [~6 EUR/1 m + 2 Endkappen](https://www.reichelt.de/?ACTION=446&LA=446&nbc=1&q=Hutschiene+35mm) | [~3–5 EUR](https://www.alibaba.com/trade/search?SearchText=din+rail+35mm) | [~6–10 EUR](https://www.amazon.de/s?k=Hutschiene+35mm+Endkappen) |
| Micro-USB- oder USB-C-Kabel (kurz) | 4 | 5 V vom Netzteil zum ESP32 | [~2–4 EUR/Stk](https://www.reichelt.de/?ACTION=446&LA=446&nbc=1&q=micro+usb+kabel+kurz) | [~0.50–1 EUR/Stk](https://www.alibaba.com/trade/search?SearchText=micro+usb+cable+short) | [~3–5 EUR/Stk](https://www.amazon.de/s?k=micro+usb+kabel+kurz) |

Optional nuetzlich:
- Schrumpfschlauch/Isolierband fuer Kabelfuehrung
- Waermeleitpaste + Kabelbinder fuer Sensorbefestigung
- Kleine Sicherung (z.B. 1 A trae­ge auf 5 V-Seite) wenn gewuenscht

## Stripboard-Skizze (ASCII)

Beispiel: Sammelschienen GND/3V3/DATA (GPIO4) und parallel abgegriffene Klemmen.

```
Ansicht von oben (Streifen laufen horizontal):

   [ESP32 Stiftleisten]
   VCC  GND  GPIO4 ... (weitere Pins ungenutzt)
   |    |    |
   |    |    +-----------------------+
   |    |                            |
   |    +------------------------+   |
   |                             |   |
   +-------------------------+   |   |
                               \ | /
Streifenraster (horizontal):
=======================================  <- DATA-Bus (GPIO4-Streifen, Pull-up 2.2k nach 3V3)
---------------------------------------  <- Trenner (Streifen auftrennen wo noetig)
=======================================  <- 3V3-Bus
=======================================  <- GND-Bus

Zu den Schraubklemmen (vertikal abgreifen):
DATA o o o o o o o o o o   (10 fuer 8er-Verteiler, je 7 fuer 5er)
3V3  o o o o o o o o o o
GND  o o o o o o o o o o

Pull-up: 2.2k Widerstand zwischen 3V3-Bus und DATA-Bus nahe am ESP32.
Streifen trennen: Unter den ESP32-Pins, die nicht verbunden sein sollen,
mit Entgrater/Bohrer die Kupferstreifen auftrennen.
```
