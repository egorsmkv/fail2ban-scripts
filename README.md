# Fail2ban API

## Usage

This script tries to get the banned list of IP addresses by Fail2ban for service `freeswitch`.
You can modify the service name if you want to.

```bash
python ./banned_list.py
```

In the response you will get JSON output with the following:

```json
{"currently_banned": 11, "total_banned": 15, "banned_ips": ["185.108.106.105", "193.46.255.195", "193.46.255.214", "196.196.203.86", "52.232.132.24", "103.145.13.81", "23.148.145.210", "103.145.13.247", "141.98.10.188", "45.34.5.54", "40.86.206.158"]}
```
