import socket
import sys
from thread import *

max_conn = 100
buffer_size = 4096
listening_port = 8888


# start the connection
def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', listening_port))
        s.listen(max_conn)
        print("[*]Server Started Succesfully [%d]\n" % (listening_port))
    except:
        print "ERROR"
        s.close()
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn, data, addr))
        except:
            s.close()
            print "ERROR"
            sys.exit(1)
    s.close()


# find and customize webserver / url / data
def conn_string(conn, data, addr):
    try:
        first_line = data.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        if str(webserver) == "localhost" or str(webserver) == "127.0.0.1":  # customization for our server
            data = "GET " + str(data)[25:]

        proxy_server(webserver, port, conn, addr, data)
    except Exception, e:
        pass


# create proxy server
def proxy_server(webserver, port, conn, addr, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        print "[*] ws: %s \n port: %s \n data %s \n" % (str(webserver), str(port), str(data))
        s.send(data)
        while 1:
            reply = s.recv(buffer_size)
            if len(reply) > 0:
                conn.send(reply)
                print "[*] Request done: %s" % (str(addr[0]))
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)


start()
