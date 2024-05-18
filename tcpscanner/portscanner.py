import socket
import time
import threading
import argparse
import re

class PortScanner:
    __port_list = [1,3,6,9,13,17,19,20,21,22,23,24,25,30,32,37,42,49,53,70,79,80,81,82,83,84,88,89,99,106,109,110,113,119,125,135,139,143,146,161,163,179,199,211,222,254,255,259,264,280,301,306,311,340,366,389,406,416,425,427,443,444,458,464,481,497,500,512,513,514,524,541,543,544,548,554,563]
    __thread_limit = 1000
    __delay = 10

    target_ports = []

    def __init__ (self,target_ports = 0):
        

        if target_ports == 0 :
            self.target_ports = self.__port_list
        
        # ! 这里如何一次处理多个传递进来的端口
        else:
            self.target_ports = target_ports
            print(f"port list is {self.target_ports}")

    
    def __usage(self):
        print("Python3 Port Scanner")
        print('input the hostname')

    def scan(self,host_name,message=''):
        
        # todo  use regex next
        if "http://" in host_name or "https://" in host_name:
            host_name = host_name[host_name.find('://') + 3 : ]

        print('*'*60+'\n')

        print('端口扫描开始 websites: ' + str(host_name))

        try:
            server_ip = socket.gethostbyname(str(host_name))
            print("server ip is : " + str(server_ip))

        except socket.error as e:
            print(f"hostname {host_name} unknown !")

            self.__usage()

            return {}

        start_time = time.time()

        output = self.__scan_ports_manage(server_ip, self.__delay,message)

        stop_time = time.time()

        print(f"host {host_name} scanner in {stop_time-start_time} seconds")
        print('端口扫描结束')

        return output
    
    def set_thread_limit(self,thread_num):
        
        thread_num = int(thread_num)

        if thread_num < 0 or thread_num > 50000:
            print("invalid thread number limit")
            print("will use the dedault limit")
            return
        
        self.__thread_limit = thread_num
    
    def set_delay(self,delay):
        delay = int(delay)

        if delay <= 0 or delay > 100:
            print("invalid delay")
            print("will use default delay")
            return
        
        self.__delay = delay
    
    def show_target_ports(self):
        print("Current Port List is : ")
        print(self.target_ports)

    def show_delay(self):
        print(f'current timeout is {self.__delay}')

    def show_thread_limit(self):
        print(f"current max thread num is {self.__thread_limit}")

    def __thread_scan_ports(self,ip,delay,output,message):
        port_index = 0

        while port_index < len(self.target_ports):
            
            while threading.active_count() < self.__thread_limit and port_index < len(self.target_ports):

                thread = threading.Thread(target=self.__TCP_connect,args=(ip,self.target_ports[port_index],delay,output,message))
                thread.start()
                port_index += 1


        
    def __scan_ports_manage(self,ip,delay,message):
        output = {}

        thread = threading.Thread(target=self.__thread_scan_ports,args=(ip,delay,output,message))
        thread.start()

        while len(output) < len(self.target_ports):
            continue

        for port in self.target_ports:
            if output[port] == "OPEN":
                print(f'{port} : {output[port]}')
        
        return output

    def __TCP_connect(self,ip,port_number,delay,output,message):
        tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # in linux use SO_REUSEPORT
        tcp_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        tcp_sock.settimeout(delay)

        if message != '':
            UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDP_sock.sendto(message.encode(), (ip, int(port_number)))

        try:
            result = tcp_sock.connect_ex((ip,int(port_number)))

            if message != "":
                tcp_sock.sendall(message.encode())
            
            if result == 0:
                output[port_number] = 'OPEN'
            else:
                output[port_number] = 'CLOSE'
            
            tcp_sock.close()

        except socket.error as e:
            output[port_number]  = 'CLOSE'
            pass


# todo 检测输入的端口是否合法， 不合法就默认使用自带端口列表
def convert_port(port_input):

    if re.match(r'^\d+(,\d+)*$',port_input):

        port_list = [ int(port) for port in port_input.split(',')]
        port_list = [port for port in port_list if 0 <= port <= 65535]

        return port_list
    else:
        print("输入格式不正确，将使用默认端口")
        return  0

if __name__ == "__main__":
    print("""
     ______  ____     ____        ____                  __      
    /\__  _\/\  _`\  /\  _`\     /\  _`\               /\ \__   
    \/_/\ \/\ \ \/\_\\\\ \ \L\ \   \ \ \L\ \ ___    _ __ \ \ ,_\  
       \ \ \ \ \ \/_/_\ \ ,__/    \ \ ,__// __`\ /\`'__\\\\ \ \/  
        \ \ \ \ \ \L\ \\\\ \ \/      \ \ \//\ \L\ \\ \ \/  \ \ \_ 
         \ \_\ \ \____/ \ \_\       \ \_\\\\ \____/ \ \_\   \ \__\\
          \/_/  \/___/   \/_/        \/_/ \/___/   \/_/    \/__/
     ____                                                         
    /\  _`\                                                       
    \ \,\L\_\     ___      __       ___      ___       __   _ __  
     \/_\__ \    /'___\  /'__`\   /' _ `\  /' _ `\   /'__`\/\`'__\\
       /\ \L\ \ /\ \__/ /\ \L\.\_ /\ \/\ \ /\ \/\ \ /\  __/\ \ \/ 
       \ `\____\\\\ \____\\\\ \__/.\_\\\\ \_\ \_\\\\ \_\ \_\\\\ \____\\\\ \_\ 
        \/_____/ \/____/ \/__/\/_/ \/_/\/_/ \/_/\/_/ \/____/ \/_/ 

        """)


    parser = argparse.ArgumentParser(description="A TCP Port Scanner")

    """
    param,   /    description  / required= True//False / default value
    -u , --url /  http://www.baidu.com , req=True
    -p , --port / 8080 / false / 0
    -t , --thread / thread num  / false / 1500
    -o , --timeout / timeout  / false / 15
    
    """

    parser.add_argument("-u","--url",dest="host_name", help="input the website to be scanned",required=True)
    parser.add_argument("-p","--port",dest="port",help="input the scanned port",default=0)
    parser.add_argument("-t","--thread",dest="thread_num",help="input the thread num",type=int)
    parser.add_argument("-o","--timeout",dest="timeout",help=" set the timeout",type=int)
    parser.add_argument("-m","--message",dest="message",help=" set the message when tcp send request",default='')

    args = parser.parse_args()

    if args.host_name:
        try:
            port_list = convert_port(args.port)
            scanner = PortScanner(port_list)
            if args.thread_num:
                scanner.set_thread_limit(thread_num=args.thread_num)
                scanner.show_thread_limit()
            if args.timeout:
                scanner.set_delay(delay=args.delay)
                scanner.show_delay()

            output = scanner.scan(args.host_name,args.message)

        except KeyboardInterrupt:
            print("User KeyBordInterrupt")

    else:
        parser.print_help()
        exit(1)
