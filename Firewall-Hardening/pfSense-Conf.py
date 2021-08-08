import time
import requests
import urllib3
import sys
import os
import pfsense_vshell
import ctypes
import tkinter as tk 
from tkinter import simpledialog

from fpdf import FPDF

import json

animation = [
"[        ]",
"[=       ]",
"[===     ]",
"[====    ]",
"[=====   ]",
"[======  ]",
"[======= ]",
"[========]",
"[ =======]",
"[  ======]",
"[   =====]",
"[    ====]",
"[     ===]",
"[      ==]",
"[       =]",
"[        ]",
"[        ]"
]

notcomplete = True

i = 0

while notcomplete:
    print(animation[i % len(animation)], end='\r')
    time.sleep(.1)
    i += 1
    if i == 50:
        break

print("\n")

print(""" _   _      _   _                                                      
| \ | |    | | | |                                                     
|  \| | ___| |_| |     __ _ _ __   ___ ___ _ __                        
| . ` |/ _ \ __| |    / _` | '_ \ / __/ _ \ '__|                       
| |\  |  __/ |_| |___| (_| | | | | (_|  __/ |                          
\_| \_/\___|\__\_____/\__,_|_| |_|\___\___|_|                          
                                                                       
                                                                       
 _____            _              _____  ___  _   _                     
/  __ \          | |            /  ___|/ _ \| | | |                    
| /  \/ ___ _ __ | |_ ___ _ __  \ `--./ /_\ \ | | |                    
| |    / _ \ '_ \| __/ _ \ '__|  `--. \  _  | | | |                    
| \__/\  __/ | | | ||  __/ |    /\__/ / | | | |_| |                    
 \____/\___|_| |_|\__\___|_|    \____/\_| |_/\___/                     
                                                                       """)

print("\n")
print("\n")

parametreler = ["0", "0", "0", "g", "0", "0", "0", "0"]

def pdf_yaz(yol, ssh_renk, parola_renk, https_renk, update_renk, backup_renk, trafik_renk, smtp_renk, dns_renk):

    pdf = FPDF()
    pdf.add_page()

    pdf.image(yol, x = 100, y = 15, w = 100)
    pdf.set_text_color(0 ,0 ,0)  
    pdf.set_font("courier", size = 24)
    pdf.cell(200, 10, txt = "- Firewall Sonuç Raporu - ", ln = 1, align = "C")

    pdf.cell(200, 10, txt = "", ln = 2, align = "C")
    pdf.cell(200, 10, txt = "", ln = 3, align = "C")
    pdf.cell(200, 10, txt = "", ln = 4, align = "C")
    pdf.cell(200, 10, txt = "", ln = 5, align = "C")   
    pdf.cell(200, 10, txt = "", ln = 6, align = "C")
    pdf.cell(200, 10, txt = "", ln = 7, align = "C")     

    pdf.set_font("courier", size = 16)

    #1

    if ssh_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "SSH Baglantisi", ln = 8, align = "L")
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Yüksek", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: MITM (Ortadaki Adam Saldirisi)", ln = 8, align = "L")    

    pdf.cell(200, 10, txt = "", ln = 7, align = "C")    

    #2

    if parola_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Varsayilan Parola", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: Brute-Force (Kaba Kuvvet Saldirisi)", ln = 8, align = "L")     
    
    pdf.cell(200, 10, txt = "", ln = 7, align = "C")  

    #3

    if https_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "HTTPS (SSL/TLS)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: Sniffing", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C")  

    #4

    if update_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Update Durumu (Guncellemeler)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: OSINT Zaafiyetleri", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C")      

    #5

    if backup_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Periyodik Yedekleme (Back Up)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Durumlar: Sistem Arizasi", ln = 8, align = "L")
    
    pdf.cell(200, 10, txt = "", ln = 7, align = "C")   

    #6

    if trafik_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Encrypted Traffic (Sifrelenmis Ag Trafigi)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Yuksek", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: Sniffing", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C") 

    #7

    if dns_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "DNS Re-binding", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: DNS Re-binding Saldirisi", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C") 
    
    #8

    if smtp_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Sifrelenmis SMTP Trafigi (SSL/TLS)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: Email Spoofing", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C") 

    pdf.output("Rapor.pdf")
    pdf.close()

flag = {
    'PHPSESSID' : 'c8d88cd638fbaef82273b7b91b753a72', 
    '__csrf_magic' : 'sid:f46cc2874695aa31ce79fa840d84f88d2770408f,1628454275'
}

ssh_flag = ""
password_flag = ""
https_flag = ""
update_flag = ""
backup_flag = ""
traffic_flag = ""
smtp_flag = ""
dns_flag = ""

from Giris import *

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
""" vshell = pfsense_vshell.PFClient(ip, kullanici_adi, parola, verify=False)
    vshell.run_command() """

json_dosyasi = open("sonuclar.json")
degiskenler = json.load(json_dosyasi)

ip_adresi = degiskenler['ip_adresi']
kullanici_adi = degiskenler['kullanici_adi']
parola = degiskenler['parola']

json_dosyasi.close()

vshell = pfsense_vshell.PFClient(ip_adresi, kullanici_adi, parola, verify=False)

def config_xml():
    xml_string = vshell.run_command("cat /cf/conf/config.xml")    
    f = open("config.xml", "x")
    f.close()
    f = open("config.xml", "a")
    f.write(xml_string)
    f.close()

config_xml()

def parse_xml_ssh():
    with open("config.xml") as f:
        if "<ssh></ssh>" in f.read():
            parametreler[0] = "0"
        else:
            parametreler[0] = "g"

parse_xml_ssh()

if parola == "pfsense":
    parametreler[1] = "0"
else:
    parametreler[1] = "g"       

def parse_xml_https():
    with open("config.xml") as f:
        if "<protocol>https</protocol>" in f.read():
            parametreler[2] = "g"  
        else:
            parametreler[2] = "0"

parse_xml_https()




pdf_yaz("img/NetLancer.png", parametreler[0], parametreler[1], parametreler[2], "g", "g", "g", "0", "0")

ctypes.windll.user32.MessageBoxW(0, "Otomatik düzeltme başlatılıyor.", 1)

cookies = {
    'PHPSESSID': flag['PHPSESSID'],
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://192.168.115.13',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://192.168.115.13/system_advanced_admin.php',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}

data = {
  '__csrf_magic': flag['__csrf_magic'],
  'webguiproto': 'https',
  'ssl-certref': '611022f974104',
  'webguiport': '443',
  'max_procs': '2',
  'loginautocomplete': 'yes',
  'althostnames': '',
  'enablesshd': 'yes',
  'sshdkeyonly': 'disabled',
  'sshport': '',
  'sshguard_threshold': '',
  'sshguard_blocktime': '',
  'sshguard_detection_time': '',
  'address0': '',
  'address_subnet0': '128',
  'serialspeed': '115200',
  'primaryconsole': 'serial',
  'save': 'Save'
}

requests.post('https://192.168.115.13/system_advanced_admin.php', headers=headers, cookies=cookies, data=data, verify=False)

ROOT = tk.Tk()

ROOT.withdraw()

USER_INP = simpledialog.askstring(title="Parola",
                                  prompt="Yeni Parolanızı Giriniz")

cookies = {
    'PHPSESSID': flag['PHPSESSID'],
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://192.168.115.13',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://192.168.115.13/system_usermanager.php?act=edit&userid=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}

params = (
    ('act', 'edit'),
    ('userid', '0'),
)

data = {
  '__csrf_magic': flag['__csrf_magic'],
  'usernamefld': 'admin',
  'passwordfld1': USER_INP,
  'passwordfld2': USER_INP,
  'expires': '',
  'webguicss': 'pfSense.css',
  'webguifixedmenu': '',
  'webguihostnamemenu': '',
  'dashboardcolumns': '2',
  'groups[]': 'admins',
  'authorizedkeys': '',
  'ipsecpsk': '',
  'act': '',
  'userid': '0',
  'privid': '',
  'certid': '',
  'utype': 'system',
  'oldusername': 'admin',
  'save': 'Save'
}

response = requests.post('https://192.168.115.13/system_usermanager.php', headers=headers, params=params, cookies=cookies, data=data, verify=False)

pdf_yaz("img/NetLancer.png", "g", "g", "g", "g", "g", "g", "g", "g")


 
print("\n")



 

