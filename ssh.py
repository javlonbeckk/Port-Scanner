import socket

def get_openssh_version(ip_address):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip_address, 22))
        connection.sendall(b"SSH-2.0-OpenSSH_7.9\r\n")
        response = connection.recv(1024)

        res = response.decode("utf-8").split()
        version = res[0]
        host = res[1]

        version_for_output = version.replace("-", " ")
        host_for_output = host.replace("-", " ")
        return f"{version_for_output}   {host_for_output}"
    except Exception as e:
        return ""



