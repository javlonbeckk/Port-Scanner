import socket

def get_redis_info(ip_address):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip_address, 6379))
        connection.sendall(b"INFO\r\n")
        response = connection.recv(1024)

        all_data = response.decode("utf-8").split("\n")
        res = ""
        version = ""
        for i in all_data:
            if "redis_version" in i:
                version = i.split(":")[1][:-1]
            else:
                res += f"    | {i}\n"
        
        return [version, res]
        

    except Exception as e:
        return ["", ""]

