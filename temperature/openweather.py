"""
Example Open Weathermap API onecall call

https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=hourly,daily&appid={API key}

"""

import sys
from signal import SIGTERM, signal
import logging

import requests
import time

import prometheus_client as PrometheusClient

class TemperatureClient(object):
    def __init__(self):
        self.onecall_url = 'https://api.openweathermap.org/data/2.5/onecall'
        self.onecall_params = {
            'lat': 51.685550,
            'lon': 5.298640,
            'appid': 'e1a3a17c5355826f12a697385aed7530'
        }

        self.temperture_gauge = PrometheusClient.Gauge(
            'temperature_reading', 'temperature reading', ['lat', 'lon'])
        self.humidity_gauge = PrometheusClient.Gauge(
            'humidity_reading', 'humidity reading', ['lat', 'lon'])
        self.pressure_gauge = PrometheusClient.Gauge(
            'pressure_reading', 'pressure reading', ['lat', 'lon'])

    def fetch(self):
        data = requests.get(self.onecall_url, params=self.onecall_params).json()

        temp = data['current']['temp']
        humidity = data['current']['humidity']
        pressure = data['current']['pressure']

        return (temp, humidity, pressure)

    def store(self, metrics):
        self.temperature_reading_gauge.labels(
            lat=self.lat, lon=self.lon
        ).set(metrics.temp)
        self.humidity_reading_gauge.labels(
            lat=self.lat, lon=self.lon
        ).set(metrics.humidity)
        self.pressure_reading_gauge.labels(
            lat=self.lat, lon=self.lon
        ).set(metrics.pressure)

    def run(self):
        while (True):
            time.sleep(60);
            self.store(self.fetch());

if __name__ == '__main__':
    def sigterm_handler(_signo, _stack_frame):
        """When sysvinit sends the TERM signal, cleanup before exiting."""
        logging.info('received signal %d, exiting...', _signo)
        logging.debug(_stack_frame)
        sys.exit(0)

    signal(SIGTERM, sigterm_handler)

    logging.info('running temperature')
    TemperatureClient().run()
