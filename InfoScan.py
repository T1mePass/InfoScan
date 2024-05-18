import argparse
import tcpscanner.portscanner as portscanner
import WebDirScan.WebDirScan as dirscan
class InfoScan:

    def __init__(self,target_url,thread_num,delay,proxy):

        self.target = target_url
        self.thread_num = thread_num
        self.delay = delay
        self.proxy = proxy
    
    def port_scan(self):

        port_scanner = portscanner.PortScanner()
        port_scanner.set_delay(self.delay)
        port_scanner.set_thread_limit(self.thread_num)
        port_scanner.scan(self.target)

    def dir_scan(self):

        dir_scanner = dirscan.DirScan(proxy=self.proxy,target_url=self.target,filename='php.txt')
        dir_scanner.set_delay(delay=self.delay)
        dir_scanner.set_thread_limit(thread_num=self.thread_num)
        dir_scanner.run()

    def finger_scan(self):
        return

    def run(self):
        '''
        2. 对url进行目录和端口扫描
        3. 进行指纹识别


        target :  https://www.baidu.com

        开放的端口有:
        80,122,21
        目录扫描结果如下:
        https://
        https://
        https://

        -------------------------------

        指纹识别结果如下
        '''
        print('运行成功')
        self.port_scan()
        self.dir_scan()


def main():

    banner = r"""
 _____ __   _ _______  _____  _______ _______ _______ __   _
   |   | \  | |______ |     | |______ |       |_____| | \  |
 __|__ |  \_| |       |_____| ______| |_____  |     | |  \_|
                                                            
"""
    print(banner)

    """
    参数设置

    -u , --url  , target_url
    -t, --thread , thread_num
    -d , --delay , delay
    -p , --proxy , proxy
    
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-u','--url',dest="target_url",required=True, help="set the target_url")
    parser.add_argument('-t','--thread',dest="thread_num",default=10,type=int)
    parser.add_argument('-d','--delay',default=5,dest="delay",type=int)
    parser.add_argument('-p','--p',dest="proxy",default=0, type=int)

    # parser.add_argument('-h','--help',dest="help",action="print_help")

    args = parser.parse_args()

    if args.target_url:
        
        scanner = InfoScan(target_url=args.target_url,delay=args.delay,thread_num=args.thread_num,proxy=args.proxy)
        scanner.run()
    else:
        
        parser.print_help()


if __name__ == "__main__":
    main()