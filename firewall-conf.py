import paramiko
			
ip_adresi = input("IP adresi: ")
kullanici_adi = input("Kullanıcı adı: ")
sifre = input("Şifre: ")
port = input("Port numarası: ")
girdiler = [ip_adresi, kullanici_adi, sifre, port]
print("""# Cisco ASAv 8.4.2 SSH baglantisi icin kullanici bilgileri""")
print("IP Adresi: {0}\nKullanıcı Adı: {1}\nParola: {2}\nPort: {3}\n".format(*girdiler))			

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip_adresi, port, kullanici_adi, sifre, timeout = 10)

secim = ""

while(True): 

	print("(1) Yönetim")
	print("(2) Kontrol")
	print("(3) Veri")
	print("q) Çıkış")
	
	secim = input("Lütfen bir seçim yapınız: ")
	
	if(secim == "1"):
		print("a) HTTP kaynaklarını yetkili bir IP adresine eşitle")
		print("b) HTTPS erişimi için TLS versiyonunu ayarla ve SSL AES-256 şifrelemesini ayarla")
		secim = input("Lütfen bir seçim yapınız: ")
			if(secim == "a"):
				stdin,stdout,stderr = ssh.exec_command("sh run http | i http_[0-9]|[0-9]|[0-9]") 
				sonuc = stdout.read()
				print(sonuc.decode("utf-8"))
			if(secim == "b"):
				stdin,stdout,stderr = ssh.exec_command("sh run ssl | in encryption.aes256-sha1$")
				sonuc = stdout.read()
				print(sonuc.decode("utf-8"))

	if(secim == "2"):
		print("a) DNS Guard aktif et")
		print("b) DHCP hizmetini devre dışı bırak")
		print("c) ICMP kısıtlaması")
		secim = input("Lütfen bir seçim yapınız: ")
			if(secim == "a"):
				stdin,stdout,stderr = ssh.exec_command("dns-guard | show running-config dns-guard") 
				sonuc = stdout.read()
				print(sonuc.decode("utf-8"))
			if(secim == "b"):
				stdin,stdout,stderr = ssh.exec_command("sh run | in dhcpd.enable.outside")
				sonuc = stdout.read()
				print(sonuc.decode("utf-8"))				
			if(secim == "c"):
				stdin,stdout,stderr = ssh.exec_command("sh run icmp | in deny.any.Outside")
				sonuc = stdout.read()
				print(sonuc.decode("utf-8"))	

	if (secim == "q"):
		break

ssh.close()

