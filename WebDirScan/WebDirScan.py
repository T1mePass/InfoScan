import requests
import argparse
import sys
import threading
import re
import time
import urllib3
import ssl

from agent_proxy import ip_proxy, user_agent_list


urllib3.disable_warnings()
# Ignore ssl warning info.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


class DirScan:

    def __init__(self, proxy, filename, target_url):

        self.proxy = proxy
        self._delay = 10
        self.filename = filename
        self.target = target_url
        self.thread_limit = 100
        self.result = []

    def set_delay(self,delay):
        self._delay = delay

    def set_thread_limit(self,thread_num):
        self.thread_limit = thread_num


    def scan(self, path):

        try:

            if self.proxy:
                req = requests.get(url=path, headers=user_agent_list.get_user_agent(), timeout=self._delay,
                                   proxies=ip_proxy.get_ip_proxy())
            else:
                req = requests.get(url=path, headers=user_agent_list.get_user_agent(), timeout=self._delay)
            # print(url)

            if req.status_code == 200:
                print(f"[*] {path}")
                self.result.append(path)

        except Exception as e:
            print(e)
            pass

    def run(self):

        print('端口扫描开始')
        index = 0
        dicts = self.read_dicts()
        length = len(dicts)
        threads = []

        while index < length:

            while threading.active_count() < self.thread_limit and index < length:
                thread = threading.Thread(target=self.scan, args=(dicts[index],))
                thread.start()
                time.sleep(0.5)
                threads.append(thread)
                index += 1

            for thread in threads:
                thread.join()

        print('目录扫描结束')

    def read_dicts(self) -> dict:

        dicts = []

        try:
            with open(f"D:/tool_code/InfoScan/WebDirScan/dicts/{self.filename}", 'r') as f:
                for c in f:
                    str = self.target + '/' + c.strip('\n')
                    dicts.append(str)

            f.close()
            return dicts


        except FileNotFoundError:
            print(f"./dicts/{self.filename} 文件不存在!")
            sys.exit(0)


if __name__ == "__main__":
    print("""
__        __   _     ____  _      ____                  
\ \      / /__| |__ |  _ \(_)_ __/ ___|  ___ __ _ _ __  
 \ \ /\ / / _ \ '_ \| | | | | '__\___ \ / __/ _` | '_ \ 
  \ V  V /  __/ |_) | |_| | | |   ___) | (_| (_| | | | |
   \_/\_/ \___|_.__/|____/|_|_|  |____/ \___\__,_|_| |_|
""")

    parser = argparse.ArgumentParser(description="Web Directory Scanner")

    parser.add_argument("-u", "--url", dest="url", help="set target url", required=True)
    parser.add_argument("-f", "--file", dest="filename", help="target url ext", required=True)
    parser.add_argument("-t", "--thread", dest="thread_num", type=int, default=2, help="set scan thread count")
    # parser.add_argument("-random_proxy",dest="isRandomProxy",type=bool,default=0,help="use random proxy, use for True, not for False",required=False)
    parser.add_argument("-proxy", dest="proxy", default=0, help="set your own proxy, format is http://192.168.1.1:8080",
                        required=False)
    parser.add_argument("-d", '--delay', dest="delay", default=5, help="set the timeout")
    args = parser.parse_args()

    try:
        if args.url and args.filename:
            # start(args.url, args.filename, args.thread_num, args.proxy)
            scanner = DirScan(filename=args.filename, proxy=args.proxy, target_url=args.url)
            scanner.run()
            sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print('^c')
