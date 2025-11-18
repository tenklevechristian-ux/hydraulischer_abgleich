### Problemstellung bzw. IST-Aufnahme:
In einem Einfamilienhaus wurde bei Kernsanierung eine Wärmepumpe und im gesamten Haus Fußbodenheizung verbaut. Auf Grund der Anzahl der Räume und deren Größe wurde in Summe vier Heizkreisverteiler verbaut, mit 1x 8 Heizkreisen und 3x 5 Heizkreisen. 
Der Initiale Hydraulische Abgleich gem. Berechnung des Sanitärfachmannes wurde der Art durchgeführt, dass alle berechneten Sollwerte kleiner gleich 0,5 auf 0,5 eingestellt wurden (da die Skala bei kleineren Werten nicht sinnvoll einstellbar ist). Das war insofern nicht zufriedenstellend, da damit der Abgleich nicht mehr vorhanden war.
Also wurde anschließend per 3-satz das ganze in der Art um einen Faktor hochgerechnet, dass der kleinste Wert 0,5 war und der größte dann 3,0. 

Diese hochskalierten Werte wurden an allen Heizkreisen eingestellt. 
Es existieren aktuell keine Stellantriebe, d.h. im gesamten Haus sind alle Heizkreise offen. 
Die Wärmepumpe steht auf ihrer initialen Heizkurve und der Nutzer hat die Raumsolltemperatur (Raumthermostat nicht vorhanden) am Innengerät der Heizung so eingestellt, dass in allen Räumen eine angenehme Temperatur herrscht. Lediglich der Wohnessbereich mit großer Fensterfront fühlt sich etwas zu kühl an, aber bei Erhöhung der Temperatur an der Wärmepumpe oder Erhöhung der Heizkurve wären alle anderen Räume dann zu warm. 

Ende IST-Aufnahme


### Der Plan:

Anschaffung von vier ESP32, sowie 31 stück DS18B20. An jeden zentralen Vorlauf und Rücklauf der vier Heizkreisverteiler kommt ein DS18B20 und an jedem Rücklauf jedes Heizkreises kommt auch ein DS18B20. Nun sollen die Temperaturen geloggt werden, idealerweise in einer zeitpunkt basierten datenbank wie influx DB v1 - z.B. über home assistant. 
Das soll dann genutzt werden um die Delta T der einzelnen Heizkreise zu erfassen und darüber einen Hydraulischen Abgleich final durchführen zu können. Natürlich exitieren Umwelteinflüsse in gewissen Bereichen des Hauses. Manche Räume haben mehr Fensterfläche andere weniger manche mehr ungedämmte aussenwand andere weniger, in manchen wird gekocht in anderen nicht. In der Theorie sollte das Delta T in allen Heizkreisen identicht sein, oder liege ich da falsch?
Mit der Aufnahme der Temperaturen in Home Assistant bzw. Influx kann über Grafana ausgerwertet werden und dann feinjustiert werden.

### Bonus:

Als Bonus dachte ich, kann man ein python script schreiben, welches die Daten analysiert und eine Empfehlung abgibt, welcher Heizkreis soll um wieviel umdrehungen geöffnet oder geschlossen werden. D.h.  Datenaufnahme-> Analyse -> Ausgabe empfehlung -> Datenaufnahme -> Anylse -> Ausgabe Empfehlung ->  .... so dass in wenigen zyklen ein perfekt abgestimmter hydraulischer abgleich entsteht. 
Bitte überlege und schreibe ein script, es soll täglich per webhook über discord die empfehlungen raussenden. 
