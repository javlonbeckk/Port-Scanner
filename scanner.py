#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
import socket
import optparse
from datetime import datetime
from termcolor import colored


#local imports
import web, ftp, ssh, redisinfo


start_time = datetime.now()
targets = []
open_ports = []


def get_arguments():
    usage = "python3 scanner.py -t <IP-address> [options] "
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-t", dest="target", 
                      help="IP address of target")
    parser.add_option("-p", dest="ports", 
                      help="Scan specific port/ports")
    parser.add_option("-r", dest="range",
                      help="Scan range of ports. Default: 1-10000",)
    parser.add_option("-l", dest="list",
                      help="List of IP addresses to scan")
    (options, arguments) = parser.parse_args()


    if options.list and options.target:
        parser.error("[+] Specify either target IP(1) or list of IP addresses, not both of them")

    elif not options.target and not options.list:
        parser.error("[+] Please specify an IP Address of target")
    
    if options.target:
        targets.append(options.target)

    if options.list:
        file = open(options.list, "r")
        for i in file.readlines():
            targets.append(i[:-1])


    if options.range and "-" not in options.range:
        parser.error("[+] Please specify a range.\nEx: 1-25")
    if options.ports and "," not in options.ports and not options.ports.isdigit():
        parser.error("[+] Please specify ports.\n Ex: -p 4 or -p 3,5")
    ports = []
    if not options.range and not options.ports:
        ports = list(range(1, 10001))

    if options.range:
        borders = options.range.split("-")
        if int(borders[0]) < 1 or int(borders[1]) > 65535:
            parser.error("[+] Incorrect range! Max port range: 1-65535")
        else:
            ports += list(range(int(borders[0]), int(borders[1])+1))

    if options.ports:
        ports_str = options.ports.split(",")
        ports_int = [int(i) for i in ports_str]
        maximum = max(ports_int)
        minimum = min(ports_int)
        if maximum > 65535 or minimum < 1:
            parser.error("[+] Incorrect ports! Range of ports: 1-65535")
        else:
            ports += ports_int
    
    ports = list(set(ports))
    ports.sort()
    return options.target, ports


def get_detailed_info(target, port):
    if port == 21:
        version = ftp.get_version(target)
        anonymous = ftp.check_anonymous(target)
        return ["ftp", version, anonymous]
    if port == 22:
        version = ssh.get_openssh_version(target)
        return ["ssh", version, ""]
    if port == 80:
        info = web.get_technologies(target, port, "http")
        return ["http"] + info
    if port == 443:
        info = web.get_technologies(target, port, "https")
        return ["https"] + info  
    if port == 6379:
        info = redisinfo.get_redis_info(target)
        return ["redis"] + info
    else:
        try:  
            service = socket.getservbyport(port)
            return [service, "", ""]
        except:
            s = web.check(target, port)

            if s == "":
                service = "unknown"
                return [service, "", ""]
            else:
                info = web.get_technologies(target, port, s)
                return [s] + info 


def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        connection = s.connect((target, port))
        open_ports.append(port)
        print(f"Open {target}:{port}")
        connection.close()
    except Exception as e:
        pass


def get_time(duration):
    duration = str(duration)
    duration = duration.split(":")

    hours = int(duration[0])
    minutes = int(duration[1])
    seconds = int(duration[2].split(".")[0])
    miniseconds = duration[2].split(".")[1][:2]

    res = str(hours*3600 + minutes*60 + seconds) + "."+ miniseconds
    return res


ports = get_arguments()[1]


if targets:
    for i in targets:
        target = i
        print(colored(f"Scanning {target}", "green"))
        with ThreadPoolExecutor(max_workers=500) as pool:
            
            pool.map(scan, ports)
            pool.shutdown()
        print()
        open_ports.sort()
        print("PORT       SERVICE          VERSION")
        for port in open_ports:
            res = get_detailed_info(i, port)
            service = res[0]
            version = res[1]
            other_data = res[2]

            l = 6 - len(str(port))
            ls = 17 - len(service)
            out = f"{port}/tcp " + " " * l + service + " "*ls + version
            print(out)
            if other_data:
                print(other_data)

        open_ports = []

        print("------------------------------------")
        print()



end_time = datetime.now()
run_time = get_time(end_time - start_time)

address = "addresses" if len(targets) > 1 else "address"

print(colored("Done: ","green") + f"{len(targets)} {address} " 
      f"scanned in {run_time} seconds")
