# Speed Monitor Pi

Ansible playbook to provisions a Raspberry Pi 4 for the purpose of monitoring internet speed.

- Tested with Raspberry Pi OS Lite (64-bit) on a Raspberry Pi 4 Model B.
- Using OS version: `2022-09-22-raspios-bullseye-arm64-lite.img.xz`

![./screenshots/dashboard-past-year.png](Dashboard past year)

### Requirements
- [Raspberry Pi][https://www.raspberrypi.org/] 3 Model B+ or 4 Model B (Gigabit capable)
- [Docker][docker] >= v20.10.17
- [GNU Make][make] >= 4.3

### Services Installed
- [InfluxDB](https://portal.influxdata.com/downloads/) v2.4.0
- [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) v9.2.0
- Cron job for running `speedtest.py` script
    - [Speedtest CLI](https://www.speedtest.net/apps/cli) v1.2.0
    - [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) v1.33.0

### Setup

1. Install [Docker](https://docs.docker.com/get-docker/)

2. Install GNU Make (*if your OS doesn't provide it by default*)

3. Generate a SSH key to access the Raspberry Pi with.

```shell
$ ssh-keygen
```

4. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to install Raspberry Pi OS Lite (64-bit) to your SD card.

    ![./screenshots/pi-imager-1.png](OS selection)

5. Ensure you have `Enable SSH` and `Allow public-key authentication only` options set with your SSH key's public key.

    ![./screenshots/pi-imager-2.png](Enable SSH option)

6. Install the SD card into your Pi.

7. Connect your Pi to the same LAN as your PC.

8. Run the Ansible playbook to provision your Pi.

```shell
$ make
```

9. Access your **Internet Speed Monitor** Grafana dashboard here.

    - http://raspberrypi.local:3000/d/internet-speed-monitor/internet-speed-monitor?orgId=1

10. You should see new data points every 15 minutes.

    ![./screenshots/dashboard.png](Dashboard)

[rpi]: https://www.raspberrypi.org/
[docker]: https://docs.docker.com/get-docker/
[make]: https://www.gnu.org/software/make/