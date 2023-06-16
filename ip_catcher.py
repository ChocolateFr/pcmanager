import socket

def get_router_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))  # connect to Google DNS server
    router_ip = s.getsockname()[0]
    s.close()
    return router_ip

