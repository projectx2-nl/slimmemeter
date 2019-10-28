## Rapsberry Pi Zero Slimmemeter installation

Slimmemeter:
- P1-data client --> collects the P1-data from the Slimmemeter and exposes this data as 'Prometheus metrics'.
- [prometheus](https://prometheus.io/docs/introduction/overview/) --> scrapes the metrics. 
- [grafana](https://grafana.com/docs/) --> presents the overview of the energy consumption.

The process are controlled/monitored via [Supervisor: A Process Control system](http://supervisord.org/)

### P1-data client installation
```shell script
# if needed install pip for python version of Pi
# sudo apt install python-pip
cd src && pip install -r requirements.txt
sudo ln -s <src-dir> /opt/p1dataclient
```

### Prometheus installation
- Download (and unpack) Prometheus ARMv6 binary from: https://prometheus.io/download/
- Configure Prometheus to scrape the P1-data metrics (exposed on fixed port 8000)
```shell script
tar xvf prometheus-2.13.1.linux-armv6.tar.gz
sudo ln -s ./prometheus-2.13.1.linux-armv6 /opt/prometheus
sudo cp conf/prometheus.yml /opt/prometheus/
```

### Grafana installation
- Download (and unpack) Grafana ARMv6 binary from: https://grafana.com/grafana/download?platform=arm
- Import the dashboard for the P1-data
```shell script
tar xvf grafana-6.4.3.linux-armv6.tar.gz
sudo ln -s ./grafana-6.4.3 /opt/grafana
```

### Supervisor installation
- Install the Supervisor package 
```shell script
sudo apt install supervisor

sudo cp conf/p1dataclint.conf /etc/supervisor/conf.d/
sudo cp conf/prometheus.conf /etc/supervisor/conf.d/
sudo cp conf/grafana.conf /etc/supervisor/conf.d/
```
- Restart the supervisor service to load the configuration files


