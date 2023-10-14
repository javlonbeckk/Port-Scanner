# Port-Scanner
Simple port scanner which scans for open ports of a given host and returns detailed information about some of running services(FTP, REDIS, HTTP, SSH)

Usage:
```python3 scanner.py -r PORT_RANGE -t TARGET```
![image](https://github.com/javlonbeckk/Port-Scanner/assets/80503011/075d54a8-b6e0-4af5-a3c8-716e4f56df4a)

It is possible to scan multiple hosts: 
```python3 scanner.py -r PORT_RANGE -l HOSTS_FILE```

To scan exact port:
```python3 scanner.py -p PORT(S) -t TARGET```

It is possible to scan exact port and range of ports simultaneously:
```python3 scanner.py -p PORTS(S) -r RANGE -t TARGET```
![image](https://github.com/javlonbeckk/Port-Scanner/assets/80503011/e2433248-e545-42fc-8a7a-811f5478ec27)
