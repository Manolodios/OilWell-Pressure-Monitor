import random
import time
import logging
import smtplib
from email.mime.text import MIMEText

# Configurar logging
logging.basicConfig(filename='well_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class OilWellMonitor:
    def __init__(self, well_id, threshold=2500, alert_email=None):
        self.well_id = well_id
        self.threshold = threshold
        self.alert_email = alert_email
        self.pressure_history = []

    def get_pressure_reading(self):
        # Simular lectura de presión con variabilidad realista
        base_pressure = 2200
        variation = random.randint(-200, 300)
        return max(1500, min(3000, base_pressure + variation))

    def check_pressure(self, pressure):
        if pressure > self.threshold:
            return "⚠️ ALERT: HIGH PRESSURE"
        elif pressure < 1800:
            return "⚠️ ALERT: LOW PRESSURE"
        else:
            return "NORMAL"

    def send_alert(self, message):
        if self.alert_email:
            try:
                msg = MIMEText(f"Alert for Well {self.well_id}: {message}")
                msg['Subject'] = f"Oil Well Alert: {self.well_id}"
                msg['From'] = 'monitor@oilwell.com'
                msg['To'] = self.alert_email

                # Simulación de envío (en producción, configurar servidor SMTP real)
                print(f"Simulating email send to {self.alert_email}: {message}")
                logging.warning(f"Alert sent: {message}")
            except Exception as e:
                logging.error(f"Failed to send alert: {e}")
        else:
            print(f"Alert: {message}")
            logging.warning(f"Alert: {message}")

    def monitor(self):
        print(f"--- Monitoring Started for Well: {self.well_id} ---")
        logging.info(f"Monitoring started for well {self.well_id}")

        try:
            while True:
                pressure = self.get_pressure_reading()
                self.pressure_history.append(pressure)
                status = self.check_pressure(pressure)

                print(f"Well {self.well_id} - Current Pressure: {pressure} PSI | Status: {status}")

                if status != "NORMAL":
                    self.send_alert(f"Pressure: {pressure} PSI - {status}")

                # Mantener solo las últimas 100 lecturas
                if len(self.pressure_history) > 100:
                    self.pressure_history.pop(0)

                time.sleep(2)
        except KeyboardInterrupt:
            print(f"\nMonitoring stopped for Well {self.well_id}.")
            logging.info(f"Monitoring stopped for well {self.well_id}")

    def get_statistics(self):
        if not self.pressure_history:
            return "No data available."
        avg = sum(self.pressure_history) / len(self.pressure_history)
        max_p = max(self.pressure_history)
        min_p = min(self.pressure_history)
        return f"Average: {avg:.2f} PSI, Max: {max_p} PSI, Min: {min_p} PSI"

if __name__ == "__main__":
    # Ejemplo de uso con múltiples pozos
    wells = [
        OilWellMonitor("UNERMB-ZULIA-01", threshold=2500, alert_email="maintenance@oilcompany.com"),
        OilWellMonitor("UNERMB-ZULIA-02", threshold=2400)
    ]

    # Para CV, demostrar monitoreo concurrente (usando threading)
    import threading

    threads = []
    for well in wells:
        t = threading.Thread(target=well.monitor)
        threads.append(t)
        t.start()

    # Esperar a que se detengan (en producción, manejar mejor)
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Stopping all monitors...")