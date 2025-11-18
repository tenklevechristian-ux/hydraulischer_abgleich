# Einkaufsliste (Hardware-Start)

Komponenten für 4 Heizkreisverteiler (1×8 Kreise, 3×5 Kreise) mit DS18B20-Bussen an GPIO4 und Bus-Abgriffen auf Streifenraster.

| Position | Menge | Beschreibung | Hinweis |
|---|---|---|---|
| ESP32-DevKitC V4 (WROOM-32) | 4 | Mikrocontroller pro Verteiler | Bewährt, 3V3-Logik, genug GPIOs |
| DS18B20, wasserdicht, 1–2 m Leitung | 31 | 10 Sensoren für 8er-Verteiler, je 7 Sensoren für die drei 5er-Verteiler | Optional 2–3 Stück Reserve mitbestellen |
| Pull-up Widerstand 2.2 kΩ, 1/4 W | 4 | Einer pro Bus (3V3 ↔ GPIO4) | Wert passt für 7–10 Sensoren |
| Streifenrasterplatine ca. 5×7 cm | 4 | Je eine pro ESP32 für die Sammelschiene (GND, 3V3, GPIO4) | Streifen längs trennen, Bus-Schienen brücken |
| Stiftleisten 2×19 (oder 2×20) 2,54 mm | 4 Sätze | Zum Aufstecken des ESP32 auf die Streifenrasterplatine | Gerade oder gewinkelt nach Platzwahl |
| Schraubklemmen 3-polig, 3.5 mm Raster | 35 | Verteilt auf 4 Boards: 10× für den 8er-Verteiler, je 7× für die drei 5er-Verteiler (für GND/3V3/DATA parallel) | Ein paar extra für Reserve |
| Litze 0.25–0.34 mm² (AWG24–22) | 1 Rolle | Zum Verbinden der Bus-Schienen (GND/3V3/GPIO4) zu den Klemmen | Silikonlitze lässt sich gut löten |
| DIN-Schaltnetzteil 230 V→5 V | 4 | Empfohlen: Mean Well HDR-15-5 (5 V/3 A, 17.5 mm Breite, Hutschiene) | Kompakt, günstig, überall verfügbar |
| DIN-Schienen-Endkappen/Tragschiene | nach Bedarf | Für sichere Montage der 5 V-Netzteile im Verteiler | 35 mm Hutschiene + 2 Endkappen |
| Micro-USB- oder USB-C-Kabel (passend zum ESP32) | 4 | Für die Stromversorgung von 5 V-Netzteil zum ESP32 | Möglichst kurz halten |

Optional nützlich:
- Schrumpfschlauch/Isolierband für Kabelführung
- Wärmeleitpaste + Kabelbinder für Sensorbefestigung
- Kleine Sicherung (z.B. 1 A träge auf 5 V-Seite) wenn gewünscht
