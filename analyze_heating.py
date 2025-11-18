#!/usr/bin/env python3
"""
Hydraulischer Abgleich - Analyse und Empfehlungen

Dieses Script analysiert die Temperaturdaten aus InfluxDB und gibt
Empfehlungen für die Anpassung der Heizkreisventile aus.

Autor: Automatisch generiert
Version: 1.0.0
"""

# =============================================================================
# KONFIGURATION - BITTE ANPASSEN
# =============================================================================

# Discord Webhook URL für Benachrichtigungen
# Erstellen unter: Discord Server → Einstellungen → Integrationen → Webhooks
DISCORD_WEBHOOK_URL = ""  # z.B. "https://discord.com/api/webhooks/xxx/yyy"

# InfluxDB Verbindungseinstellungen
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = "home_assistant"
INFLUXDB_USERNAME = ""  # Leer lassen wenn keine Auth
INFLUXDB_PASSWORD = ""  # Leer lassen wenn keine Auth

# Analyse-Parameter
TARGET_DELTA_T = 5.0  # Ziel-Spreizung in Kelvin
DELTA_T_TOLERANCE = 0.5  # Toleranzbereich ± in Kelvin
ANALYSIS_HOURS = 24  # Analysezeitraum in Stunden
MIN_MEASUREMENTS = 100  # Mindestanzahl Messungen für valide Analyse

# Heizkreis-Konfiguration
# Format: "sensor_entity_id": ("Raumname", "Verteiler")
HEATING_CIRCUITS = {
    # Verteiler OG (8 Kreise)
    "sensor.og_hk1_bad_ruecklauf": ("Bad OG", "OG"),
    "sensor.og_hk2_schlafzimmer_ruecklauf": ("Schlafzimmer", "OG"),
    "sensor.og_hk3_kinderzimmer1_ruecklauf": ("Kinderzimmer 1", "OG"),
    "sensor.og_hk4_kinderzimmer2_ruecklauf": ("Kinderzimmer 2", "OG"),
    "sensor.og_hk5_flur_ruecklauf": ("Flur OG", "OG"),
    "sensor.og_hk6_ankleide_ruecklauf": ("Ankleide", "OG"),
    "sensor.og_hk7_gaeste_ruecklauf": ("Gäste WC", "OG"),
    "sensor.og_hk8_reserve_ruecklauf": ("Reserve OG", "OG"),

    # Verteiler EG (5 Kreise)
    "sensor.eg_hk1_wohnen_ruecklauf": ("Wohnzimmer", "EG"),
    "sensor.eg_hk2_essen_ruecklauf": ("Esszimmer", "EG"),
    "sensor.eg_hk3_kueche_ruecklauf": ("Küche", "EG"),
    "sensor.eg_hk4_flur_ruecklauf": ("Flur EG", "EG"),
    "sensor.eg_hk5_wc_ruecklauf": ("Gäste WC EG", "EG"),

    # Verteiler KG (5 Kreise)
    "sensor.kg_hk1_hobby_ruecklauf": ("Hobbyraum", "KG"),
    "sensor.kg_hk2_technik_ruecklauf": ("Technikraum", "KG"),
    "sensor.kg_hk3_flur_ruecklauf": ("Flur KG", "KG"),
    "sensor.kg_hk4_wasche_ruecklauf": ("Waschküche", "KG"),
    "sensor.kg_hk5_reserve_ruecklauf": ("Reserve KG", "KG"),

    # Verteiler DG (5 Kreise)
    "sensor.dg_hk1_studio_ruecklauf": ("Studio", "DG"),
    "sensor.dg_hk2_bad_ruecklauf": ("Bad DG", "DG"),
    "sensor.dg_hk3_buero_ruecklauf": ("Büro", "DG"),
    "sensor.dg_hk4_galerie_ruecklauf": ("Galerie", "DG"),
    "sensor.dg_hk5_reserve_ruecklauf": ("Reserve DG", "DG"),
}

# Vorlauf-Sensoren pro Verteiler
SUPPLY_SENSORS = {
    "OG": "sensor.og_vorlauf",
    "EG": "sensor.eg_vorlauf",
    "KG": "sensor.kg_vorlauf",
    "DG": "sensor.dg_vorlauf",
}

# =============================================================================
# AB HIER NICHTS ÄNDERN (es sei denn, du weißt was du tust)
# =============================================================================

import json
import sys
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass

try:
    from influxdb import InfluxDBClient
except ImportError:
    print("ERROR: influxdb-Paket nicht installiert!")
    print("Installation: pip install influxdb")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests-Paket nicht installiert!")
    print("Installation: pip install requests")
    sys.exit(1)


@dataclass
class HeatingCircuitAnalysis:
    """Analyseergebnis für einen Heizkreis"""
    entity_id: str
    room_name: str
    distributor: str
    avg_delta_t: float
    min_delta_t: float
    max_delta_t: float
    std_delta_t: float
    measurement_count: int
    avg_return_temp: float
    avg_supply_temp: float
    recommendation: str
    adjustment: float  # Positive = öffnen, Negative = schließen
    priority: int  # 1 = hoch, 2 = mittel, 3 = niedrig


class HeatingAnalyzer:
    """Hauptklasse für die Heizungsanalyse"""

    def __init__(self):
        self.client = None
        self.results: list[HeatingCircuitAnalysis] = []

    def connect_db(self) -> bool:
        """Verbindung zu InfluxDB herstellen"""
        try:
            self.client = InfluxDBClient(
                host=INFLUXDB_HOST,
                port=INFLUXDB_PORT,
                username=INFLUXDB_USERNAME if INFLUXDB_USERNAME else None,
                password=INFLUXDB_PASSWORD if INFLUXDB_PASSWORD else None,
                database=INFLUXDB_DATABASE
            )
            # Verbindung testen
            self.client.ping()
            print(f"✓ InfluxDB Verbindung hergestellt ({INFLUXDB_HOST}:{INFLUXDB_PORT})")
            return True
        except Exception as e:
            print(f"✗ InfluxDB Verbindungsfehler: {e}")
            return False

    def query_sensor_data(self, entity_id: str) -> list[dict]:
        """Sensordaten aus InfluxDB abfragen"""
        query = f'''
            SELECT mean("value") as value
            FROM "°C"
            WHERE "entity_id" = '{entity_id}'
            AND time > now() - {ANALYSIS_HOURS}h
            GROUP BY time(5m)
            fill(none)
        '''
        try:
            result = self.client.query(query)
            points = list(result.get_points())
            return points
        except Exception as e:
            print(f"  Fehler bei Abfrage {entity_id}: {e}")
            return []

    def calculate_statistics(self, values: list[float]) -> tuple[float, float, float, float]:
        """Statistische Kennwerte berechnen"""
        if not values:
            return 0.0, 0.0, 0.0, 0.0

        n = len(values)
        avg = sum(values) / n
        min_val = min(values)
        max_val = max(values)

        # Standardabweichung
        variance = sum((x - avg) ** 2 for x in values) / n
        std = variance ** 0.5

        return avg, min_val, max_val, std

    def generate_recommendation(self, delta_t: float) -> tuple[str, float, int]:
        """Empfehlung basierend auf Delta T generieren"""
        diff = delta_t - TARGET_DELTA_T

        if abs(diff) <= DELTA_T_TOLERANCE:
            return "✓ Optimal eingestellt", 0.0, 3

        if diff > 0:
            # Delta T zu hoch → zu wenig Durchfluss → öffnen
            if diff > 2.0:
                return "⚠ Stark unterversorgt - deutlich öffnen", diff, 1
            elif diff > 1.0:
                return "↑ Unterversorgt - öffnen", diff, 2
            else:
                return "↗ Leicht unterversorgt - etwas öffnen", diff, 3
        else:
            # Delta T zu niedrig → zu viel Durchfluss → schließen
            if diff < -2.0:
                return "⚠ Stark überversorgt - deutlich schließen", diff, 1
            elif diff < -1.0:
                return "↓ Überversorgt - schließen", diff, 2
            else:
                return "↘ Leicht überversorgt - etwas schließen", diff, 3

    def estimate_valve_turns(self, adjustment: float) -> str:
        """Schätze Ventil-Umdrehungen basierend auf Abweichung"""
        abs_adj = abs(adjustment)

        if abs_adj < 0.5:
            return "keine Anpassung"
        elif abs_adj < 1.0:
            turns = "¼"
        elif abs_adj < 1.5:
            turns = "½"
        elif abs_adj < 2.5:
            turns = "¾ - 1"
        else:
            turns = "1 - 1½"

        direction = "öffnen" if adjustment > 0 else "schließen"
        return f"{turns} Umdrehung(en) {direction}"

    def analyze_circuit(self, entity_id: str, room_name: str, distributor: str) -> Optional[HeatingCircuitAnalysis]:
        """Einzelnen Heizkreis analysieren"""
        print(f"  Analysiere: {room_name} ({distributor})...", end=" ")

        # Rücklauf-Daten holen
        return_data = self.query_sensor_data(entity_id)
        if len(return_data) < MIN_MEASUREMENTS:
            print(f"✗ Zu wenig Daten ({len(return_data)})")
            return None

        # Vorlauf-Daten holen
        supply_entity = SUPPLY_SENSORS.get(distributor)
        if not supply_entity:
            print(f"✗ Kein Vorlauf-Sensor für {distributor}")
            return None

        supply_data = self.query_sensor_data(supply_entity)
        if len(supply_data) < MIN_MEASUREMENTS:
            print(f"✗ Zu wenig Vorlauf-Daten")
            return None

        # Timestamps matchen und Delta T berechnen
        supply_dict = {p['time']: p['value'] for p in supply_data if p['value'] is not None}
        delta_t_values = []
        return_temps = []
        supply_temps = []

        for point in return_data:
            time = point['time']
            return_temp = point['value']

            if return_temp is None or time not in supply_dict:
                continue

            supply_temp = supply_dict[time]
            if supply_temp is None:
                continue

            delta_t = supply_temp - return_temp

            # Plausibilitätsprüfung
            if 0 < delta_t < 20:  # Delta T sollte zwischen 0 und 20K liegen
                delta_t_values.append(delta_t)
                return_temps.append(return_temp)
                supply_temps.append(supply_temp)

        if len(delta_t_values) < MIN_MEASUREMENTS // 2:
            print(f"✗ Zu wenig valide Messungen")
            return None

        # Statistik berechnen
        avg_dt, min_dt, max_dt, std_dt = self.calculate_statistics(delta_t_values)
        avg_return = sum(return_temps) / len(return_temps)
        avg_supply = sum(supply_temps) / len(supply_temps)

        # Empfehlung generieren
        recommendation, adjustment, priority = self.generate_recommendation(avg_dt)

        print(f"✓ ΔT={avg_dt:.1f}K")

        return HeatingCircuitAnalysis(
            entity_id=entity_id,
            room_name=room_name,
            distributor=distributor,
            avg_delta_t=avg_dt,
            min_delta_t=min_dt,
            max_delta_t=max_dt,
            std_delta_t=std_dt,
            measurement_count=len(delta_t_values),
            avg_return_temp=avg_return,
            avg_supply_temp=avg_supply,
            recommendation=recommendation,
            adjustment=adjustment,
            priority=priority
        )

    def analyze_all(self):
        """Alle Heizkreise analysieren"""
        print("\n" + "="*60)
        print("HYDRAULISCHER ABGLEICH - ANALYSE")
        print("="*60)
        print(f"Analysezeitraum: letzte {ANALYSIS_HOURS} Stunden")
        print(f"Ziel Delta T: {TARGET_DELTA_T}K (±{DELTA_T_TOLERANCE}K)")
        print("-"*60)

        for entity_id, (room_name, distributor) in HEATING_CIRCUITS.items():
            result = self.analyze_circuit(entity_id, room_name, distributor)
            if result:
                self.results.append(result)

        # Nach Priorität sortieren
        self.results.sort(key=lambda x: (x.priority, -abs(x.adjustment)))

    def print_summary(self):
        """Zusammenfassung ausgeben"""
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)

        if not self.results:
            print("Keine Analyseergebnisse verfügbar!")
            return

        # Statistik über alle Kreise
        all_delta_t = [r.avg_delta_t for r in self.results]
        avg_all = sum(all_delta_t) / len(all_delta_t)
        spread = max(all_delta_t) - min(all_delta_t)

        print(f"\nAnalysierte Heizkreise: {len(self.results)}")
        print(f"Durchschnittliches Delta T: {avg_all:.2f}K")
        print(f"Spreizung (max-min): {spread:.2f}K")

        # Kategorisierung
        optimal = sum(1 for r in self.results if abs(r.adjustment) < DELTA_T_TOLERANCE)
        needs_adjust = len(self.results) - optimal

        print(f"\nOptimal eingestellt: {optimal}")
        print(f"Anpassung nötig: {needs_adjust}")

        # Details pro Verteiler
        distributors = set(r.distributor for r in self.results)
        for dist in sorted(distributors):
            print(f"\n--- Verteiler {dist} ---")
            dist_results = [r for r in self.results if r.distributor == dist]

            for r in sorted(dist_results, key=lambda x: -abs(x.adjustment)):
                status = "●" if abs(r.adjustment) < DELTA_T_TOLERANCE else "○"
                print(f"  {status} {r.room_name}: ΔT={r.avg_delta_t:.1f}K")
                if abs(r.adjustment) >= DELTA_T_TOLERANCE:
                    print(f"      → {self.estimate_valve_turns(r.adjustment)}")

    def print_recommendations(self):
        """Empfehlungen ausgeben"""
        print("\n" + "="*60)
        print("HANDLUNGSEMPFEHLUNGEN")
        print("="*60)

        # Nur Kreise die Anpassung brauchen
        needs_work = [r for r in self.results if abs(r.adjustment) >= DELTA_T_TOLERANCE]

        if not needs_work:
            print("\n✓ Alle Heizkreise sind optimal eingestellt!")
            print("  Keine Anpassungen erforderlich.")
            return

        print(f"\n{len(needs_work)} Heizkreis(e) benötigen Anpassung:\n")

        for i, r in enumerate(needs_work, 1):
            priority_symbol = {1: "🔴", 2: "🟡", 3: "🟢"}.get(r.priority, "⚪")

            print(f"{i}. {priority_symbol} {r.room_name} ({r.distributor})")
            print(f"   Aktuell: ΔT = {r.avg_delta_t:.1f}K (Ziel: {TARGET_DELTA_T}K)")
            print(f"   {r.recommendation}")
            print(f"   Empfehlung: {self.estimate_valve_turns(r.adjustment)}")
            print()

        print("-"*60)
        print("ANLEITUNG:")
        print("1. Ventil am Heizkreisverteiler lokalisieren")
        print("2. Aktuelle Einstellung notieren")
        print("3. Ventil gemäß Empfehlung anpassen")
        print("4. 24-48h warten und erneut messen")
        print("5. Bei Bedarf iterieren")

    def format_discord_message(self) -> dict:
        """Discord Webhook Nachricht formatieren"""
        if not self.results:
            return {
                "content": "⚠️ **Hydraulischer Abgleich**: Keine Analysedaten verfügbar!"
            }

        # Statistik
        all_delta_t = [r.avg_delta_t for r in self.results]
        avg_all = sum(all_delta_t) / len(all_delta_t)
        spread = max(all_delta_t) - min(all_delta_t)

        needs_work = [r for r in self.results if abs(r.adjustment) >= DELTA_T_TOLERANCE]

        # Embed erstellen
        embed = {
            "title": "🌡️ Hydraulischer Abgleich - Täglicher Report",
            "color": 0x00ff00 if not needs_work else 0xffaa00,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {
                    "name": "📊 Übersicht",
                    "value": f"Analysierte Kreise: {len(self.results)}\n"
                             f"Ø Delta T: {avg_all:.1f}K\n"
                             f"Spreizung: {spread:.1f}K",
                    "inline": True
                },
                {
                    "name": "📈 Status",
                    "value": f"✓ Optimal: {len(self.results) - len(needs_work)}\n"
                             f"⚠ Anpassung: {len(needs_work)}",
                    "inline": True
                }
            ],
            "footer": {
                "text": f"Analysezeitraum: {ANALYSIS_HOURS}h | Ziel: {TARGET_DELTA_T}K"
            }
        }

        # Empfehlungen hinzufügen
        if needs_work:
            recommendations = []
            for r in needs_work[:5]:  # Max 5 anzeigen
                priority_emoji = {1: "🔴", 2: "🟡", 3: "🟢"}.get(r.priority, "⚪")
                recommendations.append(
                    f"{priority_emoji} **{r.room_name}** ({r.distributor}): "
                    f"ΔT={r.avg_delta_t:.1f}K → {self.estimate_valve_turns(r.adjustment)}"
                )

            embed["fields"].append({
                "name": "🔧 Empfehlungen",
                "value": "\n".join(recommendations),
                "inline": False
            })

            if len(needs_work) > 5:
                embed["fields"].append({
                    "name": "",
                    "value": f"*...und {len(needs_work) - 5} weitere*",
                    "inline": False
                })
        else:
            embed["fields"].append({
                "name": "✅ Ergebnis",
                "value": "Alle Heizkreise sind optimal eingestellt!",
                "inline": False
            })

        return {"embeds": [embed]}

    def send_discord_notification(self) -> bool:
        """Benachrichtigung an Discord senden"""
        if not DISCORD_WEBHOOK_URL:
            print("\n⚠ Discord Webhook nicht konfiguriert - überspringe Benachrichtigung")
            return False

        try:
            message = self.format_discord_message()
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                json=message,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 204]:
                print("\n✓ Discord Benachrichtigung gesendet")
                return True
            else:
                print(f"\n✗ Discord Fehler: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"\n✗ Discord Verbindungsfehler: {e}")
            return False

    def export_json(self, filename: str = "analysis_results.json"):
        """Ergebnisse als JSON exportieren"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "target_delta_t": TARGET_DELTA_T,
                "tolerance": DELTA_T_TOLERANCE,
                "analysis_hours": ANALYSIS_HOURS
            },
            "results": [
                {
                    "entity_id": r.entity_id,
                    "room_name": r.room_name,
                    "distributor": r.distributor,
                    "avg_delta_t": round(r.avg_delta_t, 2),
                    "min_delta_t": round(r.min_delta_t, 2),
                    "max_delta_t": round(r.max_delta_t, 2),
                    "std_delta_t": round(r.std_delta_t, 2),
                    "measurement_count": r.measurement_count,
                    "avg_return_temp": round(r.avg_return_temp, 2),
                    "avg_supply_temp": round(r.avg_supply_temp, 2),
                    "recommendation": r.recommendation,
                    "adjustment": round(r.adjustment, 2),
                    "priority": r.priority
                }
                for r in self.results
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Ergebnisse exportiert: {filename}")


def main():
    """Hauptfunktion"""
    print("\n" + "="*60)
    print("  HYDRAULISCHER ABGLEICH - ANALYSE TOOL")
    print("  Version 1.0.0")
    print("="*60)

    analyzer = HeatingAnalyzer()

    # Verbindung herstellen
    if not analyzer.connect_db():
        print("\nAbbruch: Keine Datenbankverbindung")
        sys.exit(1)

    # Analyse durchführen
    analyzer.analyze_all()

    # Ergebnisse ausgeben
    analyzer.print_summary()
    analyzer.print_recommendations()

    # JSON Export
    analyzer.export_json()

    # Discord Benachrichtigung
    analyzer.send_discord_notification()

    print("\n" + "="*60)
    print("Analyse abgeschlossen")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
