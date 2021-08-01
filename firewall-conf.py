import time
import requests
import urllib3
import sys
import os
import pfsense_vshell

from fpdf import FPDF

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

parametreler = ["img/NetLancer.png"]

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

    if smtp_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "Sifrelenmis SMTP Trafigi (SSL/TLS)", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: Email Spoofing", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C") 

    #8

    if dns_renk == "g": 
        pdf.set_text_color(0, 255, 0) 
    else:
        pdf.set_text_color(255, 0, 0)
    pdf.cell(200, 10, txt = "DNS Re-binding", ln = 8, align = "L")      
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt = "Risk Durumu: Orta", ln = 8, align = "L")
    pdf.cell(200, 10, txt = "Olasi Saldirilar: DNS Re-binding Saldirisi", ln = 8, align = "L")

    pdf.cell(200, 10, txt = "", ln = 7, align = "C") 

    pdf.output("Rapor.pdf")

flag = {
    'PHPSESSID' : '', 
    '__csrf_magic' : ''
}

ip = input("IP Adresi: ")
kullanici_adi = input("Kullanici Adi: ")
parola = input("Parola: ")

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
""" vshell = pfsense_vshell.PFClient(ip, kullanici_adi, parola, verify=False)
    vshell.run_command() """

vshell = pfsense_vshell.PFClient(ip, kullanici_adi, parola, verify=False)

def config_xml():
    xml_string = vshell.run_command("cat /cf/conf/config.xml")    
    f = open("config.xml", "x")
    f.close()
    f = open("config.xml", "a")
    f.write(xml_string)
    f.close()

config_xml()

def parse_xml(string):
    with open("config.xml") as f:
        if string in f.read():
            parametreler.append('g')
        else:
            parametreler.append('0')

def parse_xml_reverse(string):
    with open("config.xml") as f:
        if string in f.read():
            parametreler.append('0')
        else:
            parametreler.append('g')

parse_xml_reverse("<ssh></ssh>")

if parola == "pfsense":
    parametreler.append("0")
else:
    parametreler.append("g")

parse_xml("<protocol>https</protocol>")

print(parametreler)

""" animation = "|/-\\"

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush() """

print("\n")
