"""
Receive P1-data from slimmemeter via UART and forward the P1-data AWS.
"""

import os
import sys
import signal
import logging

from datetime import datetime

from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

#from influxdb import InfluxDBClient
from p1datametrics import P1DataMetrics

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class P1DataClient(object):
    """P1DataClient class"""

    def __init__(self, serial):
        self.serial = Serial(serial, 115200,
                             bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)

        self.influx_client = InfluxDBClient(ssl=True, host='sm-data.zifzaf.com', port=8086,
                                            username='p1dataclient', password='pRxyz456',
                                            database='slimmemeterkast')

    def receive(self):
        """receive p1 data"""

        p1data = ''
        while True:
            p1data_line = self.serial.readline()
            if len(p1data) == 0:
                if p1data_line[0] == '/':
                    p1data = p1data_line
                else:
                    pass
            else:
                p1data += p1data_line
                if p1data_line[0] == '!':
                    logging.debug('received raw p1data:\n%s', p1data)
                    return p1data
                else:
                    pass

    def store(self, metrics):
        """store metrics in influxdb"""
        now = str(datetime.now())

        points = [
            {
                'measurement': 'elec',
                'tags': {
                    'elec_eid': metrics.elec_eid()
                },
                'time': now,
                'fields': {
                    'tarrif1_delivered_reading': metrics.tarrif1_delivered_reading()[0],
                    'tarrif2_delivered_reading': metrics.tarrif2_delivered_reading()[0],
                    'tariff_indicator': metrics.tariff_indicator(),
                    'power_delivered': metrics.power_delivered()[0],
                    'l1_power_delivered': metrics.l1_power_delivered()[0],
                    'l2_power_delivered': metrics.l2_power_delivered()[0],
                    'l3_power_delivered': metrics.l3_power_delivered()[0]
                }
            },
            {
                'measurement': 'gas',
                'tags': {
                    'gas_eid': metrics.gas_eid()
                },
                'time': now,
                'fields': {
                    'gas_delivered_reading': metrics.gas_delivered_reading()[0]
                }
            }
        ]
        self.influx_client.write_points(points)

        logging.debug('stored p1data points:\n%s', points)


    def run(self):
        """receive p1 data and post the data to the influxdb endpoint and again and again ..."""
        while True:
            self.store(P1DataMetrics(self.receive()))


if __name__ == '__main__':
    def sigterm_handler(_signo, _stack_frame):
        """When sysvinit sends the TERM signal, cleanup before exiting."""
        logging.info('received signal %d, exiting...', _signo)
        logging.debug(_stack_frame)
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)

    SERIAL = sys.argv[1]

    logging.info('running p1dataclient (%s)', SERIAL)
    P1DataClient(SERIAL).run()
