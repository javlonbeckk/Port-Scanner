import socket
from ftplib import FTP

def get_version(ip_address):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip_address, 21))
        connection.sendall(b"USER anonymous\r\n")
        response = connection.recv(1024)

        
        service_version = response.decode("utf-8").split()
        service = service_version[1]
        version = service_version[2]
        service = service.replace("(", "")
        version = version.replace(")", "")
        return service + " " + version

    except Exception as e:
        return None


def check_anonymous(ip_address):
    ftp = FTP(ip_address)

    try:
        ftp.login() 
        ftp.quit()        
        return "    | anonymous login allowed"
    except Exception:
        return "    | anonymous login is NOT allowed"