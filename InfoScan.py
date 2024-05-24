import argparse
from datetime import datetime

import tcpscanner.portscanner as portscanner
import WebDirScan.WebDirScan as dirscan
import FingerScan.FingerScan as finger_scan
import re

# colour
W = '\033[0m'
G = '\033[1;32m'
R = '\033[1;31m'
O = '\033[1;33m'
B = '\033[1;34m'
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


#  指纹扫描模块
    def fin_scan(self):
        # if re.match(r'^https?://{2}\w.+$',self.target):
        #     print()
        # else:
        #     print('当前url格式不符合')
        #     exit(0)

        print(f'指纹扫描开始，当前扫描的url为{self.target}')
        cms = finger_scan.Cmsscanner(self.target)
        fofa_finger = cms.run()
        banner = []

        for x in fofa_finger:
            banner.append(x)
 # todo 通过wappalyzer添加指纹信息
        try:
            Wappalyzer = finger_scan.useWappalyzer(self.target)

            for x in Wappalyzer :
                x = str(x).replace('\\;condfidence:50','')
                banner.append(x)

        except Exception as e:
            print("Wappalayzer check error",e)
            pass


        try:

            update = False
            webanalyzer_banner = finger_scan.webanalyzer.check(self.target,update)

            for x in webanalyzer_banner:
                banner.append(x)
        except Exception as e:
            print('Webanalyzer check error:',e)
            pass

        print("-"*50)

        banner_tmp = []
        # print("banner:",banner)
        banner.sort()
        banner_ = set(list(banner))
        # print("banner_:",banner_)

        for x in banner_:
            if x:
                flag = 0
                for y in banner_tmp:
                    if str(x).lower() in str(y).lower() or str(y).lower() in str(x):
                        flag = 1
                        continue
                if flag == 0:
                    banner_tmp.append(x)

        banner = banner_tmp

        banner_all = ''
        cms_name = ''
        cms_name_flag = 0
        for banner_tmp2 in banner:
            banner_all = banner_all + ' | ' + banner_tmp2
            if banner_tmp2.lower() in finger_scan.cms_finger_list:
                cms_name = banner_tmp2
                cms_name_flag = 1
        banner_all = banner_all.strip()
        if banner_all.startswith('| '):
            banner_all = banner_all[1:]
        if banner_all:
            print(R, "Banner:", W, G, banner_all, W)

        # if not cms_name_flag:
        #     if finger_scan.dir_mode == 1:
        #         cms_name_tmp = finger_scan.finger_query(self.target)
        #         if cms_name_tmp:
        #             cms_name = cms_name_tmp['cms_name']
        if not cms_name:
            cms_name = 'Not Found'
        print(R, "CMS_finger:", W, G, cms_name, W)
        end = datetime.now()
        print("-" * 50)




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
        self.fin_scan()


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