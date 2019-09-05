## Rapsberry Pi Zero Slimmemeter installation

Slimmemeter:
- P1-data client --> collects the P1-data from the Slimmemeter and exposes this data as 'Prometheus metrics'.
- [prometheus](https://prometheus.io/docs/introduction/overview/) --> scrapes the metrics. 
- [grafana](https://grafana.com/docs/) --> presents the overview of the energy consumption.

The process are controlled/monitored via [Supervisor: A Process Control system](http://supervisord.org/)

###P1-data client installation
```shell script
cd src && pip install -r requirements.txt
```

###Prometheus installation
- Download (and unpack) Prometheus ARMv6 binary from: https://prometheus.io/download/
- Configure Prometheus to scrape the P1-data metrics (exposed on fixed port 8000)

### Grafana installation
- Download (and unpack) Grafana ARMv6 binary from: https://grafana.com/grafana/download?platform=arm
- Import the dashboard for the P1-data

### Supervisor installation
- Install the Supervisor package 
```shell script
sudo apt install supervisor

sudo cp conf/p1dataclint.conf /etc/supervisor/conf.d/
sudo cp conf/prometheus.conf /etc/supervisor/conf.d/
sudo cp conf/grafana.conf /etc/supervisor/conf.d/
```
- Restart the supervisor service to load the configuration files


