import unittest

from .p1datametrics import P1DataMetrics

class TestP1DataMetrics(unittest.TestCase):
    """p1dataparser module tests"""

    def setUp(self):
        raw = '\
/KFM5KAIFA-METER\r\n\
\r\n\
1-3:0.2.8(42)\r\n\
0-0:1.0.0(161129002535W)\r\n\
0-0:96.1.1(4530303236303030303331313138333136)\r\n\
1-0:1.8.1(000458.330*kWh)\r\n\
1-0:1.8.2(000364.935*kWh)\r\n\
1-0:2.8.1(000000.000*kWh)\r\n\
1-0:2.8.2(000000.000*kWh)\r\n\
0-0:96.14.0(0001)\r\n\
1-0:1.7.0(00.513*kW)\r\n\
1-0:2.7.0(00.000*kW)\r\n\
0-0:96.7.21(00001)\r\n\
0-0:96.7.9(00001)\r\n\
1-0:99.97.0(1)(0-0:96.7.19)(000101000014W)(2147483647*s)\r\n\
1-0:32.32.0(00000)\r\n\
1-0:52.32.0(00000)\r\n\
1-0:72.32.0(00102)\r\n\
1-0:32.36.0(00000)\r\n\
1-0:52.36.0(00000)\r\n\
1-0:72.36.0(00000)\r\n\
0-0:96.13.1()\r\n\
0-0:96.13.0()\r\n\
1-0:31.7.0(000*A)\r\n\
1-0:51.7.0(001*A)\r\n\
1-0:71.7.0(000*A)\r\n\
1-0:21.7.0(00.171*kW)\r\n\
1-0:41.7.0(00.330*kW)\r\n\
1-0:61.7.0(00.012*kW)\r\n\
1-0:22.7.0(00.000*kW)\r\n\
1-0:42.7.0(00.000*kW)\r\n\
1-0:62.7.0(00.000*kW)\r\n\
0-1:24.1.0(003)\r\n\
0-1:96.1.0(4730303235303033343137303833333136)\r\n\
0-1:24.2.1(161129000000W)(00528.862*m3)\r\n\
!D21C\r\n'
        self.metrics = P1DataMetrics(raw)

    def test_elec_eid(self):
        eid = self.metrics.elec_eid()
        self.assertEqual(eid, '4530303236303030303331313138333136', 'invalid elec_eid')

    def test_gas_eid(self):
        eid = self.metrics.gas_eid()
        self.assertEqual(eid, '4730303235303033343137303833333136', 'invalid gas_eid')

    def test_tarrif1_delivered_reading(self):
        tariff = self.metrics.tarrif1_delivered_reading()
        self.assertEqual(tariff, (458.330, 'kWh'), 'invalid tariff 1 delivered reading')

    def test_tarrif2_delivered_reading(self):
        tariff = self.metrics.tarrif2_delivered_reading()
        self.assertEqual(tariff, (364.935, 'kWh'), 'invalid tariff 2 delivered reading')

    def test_tariff_indicator(self):
        indicator = self.metrics.tariff_indicator()
        self.assertEqual(indicator, 1, 'invalid tariff indicator')

    def test_power_delivered(self):
        power = self.metrics.power_delivered()
        self.assertEqual(power, (0.513, 'kW'), 'invalid power delivered')

    def test_gas_delivered_reading(self):
        gas = self.metrics.gas_delivered_reading()
        self.assertEqual(gas, (528.862, 'm3'), 'invalid gas delivered reading')

if __name__ == '__main__':
    unittest.main()
