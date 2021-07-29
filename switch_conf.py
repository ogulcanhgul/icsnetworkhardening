from netmiko import ConnectHandler
import getpass

cihaz_puan = 100


def getpasswd():
    password = getpass.getpass()
    return password


def getusername():
    username = input("SSH Kullanici Adiniz : ")
    return username


def getip():
    ip_add = input("IP Adresi : ")
    return ip_add


username = getusername()

iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': getip(),
    'username': username,
    'password': getpasswd()
}

net_connect = ConnectHandler(**iosv_l2)

# ************************************************************AAA RULES START*****************************************************************************

def aaarulescheck():

    tacacs = False
    radius = False
    localssh = False

    output = net_connect.send_command('show run tacacs')
    if str.__contains__(output, "Invalid"):
        tacacs = False
    else:
        tacacs = True

    output = net_connect.send_command('sho running-config radius')

    if str.__contains__(output, "radius-server host"):
        radius = True
    else:
        radius = False

    output = net_connect.send_command('sho run | i sshkey')
    if(str.__contains__(output,"username "+username)):
        localssh = True
    else:
        localssh = False

    if tacacs == False:
        a = input("Cihaz üzerinde tacacs+ konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_tacacs_config()

    if(radius==False):
        a = input("Cihaz üzerinde radius konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_radius_config()
    if(localssh==False):
        a = input("Cihaz üzerinde yerel ssh anahtarı konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_localssh_config()

def do_localssh_config():

    try:
        ssh_public_key = input("SSH public anahtarinizi giriniz : ")
        config_commands = ['username '+str(username)+" sshkey "+str(ssh_public_key)]
        net_connect.send_config_set(config_commands)

    except:
        print("SSH anahtar yapılandırılması başarılı")


def do_radius_config():
    a = input("Kaç adet radius server kullanacaksiniz?")

    for i in range(0,int(a)):
        radius_serv_ip = input("RADIUS server "+str(i+1)+" ip adresi : ")
        radius_group_name=input("RADIUS server grup adi : ")
        radius_serv_pass = input("RADIUS server şifresi  : ")
        config_commands = ['radius-server host '+str(radius_serv_ip)+" key " + radius_serv_pass + " authentication accounting"]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa group server radius '+radius_group_name,'server '+radius_serv_ip]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa authentication login default group '+radius_group_name,'aaa authentication login console group '+radius_group_name]
        net_connect.send_config_set(config_commands)
    print("RADIUS server yapılandırılması başarılı.")
def do_tacacs_config():

    a = input("Kaç adet tacacs+ server kullanacaksiniz?")

    for i in range(0,int(a)):
        tacacs_serv_ip = input("TACACS server "+str(i+1)+" ip adresi : ")
        tacacs_group_name=input("TACACS server grup adi : ")
        tacacs_serv_pass = input("TACACS server şifresi  : ")
        config_commands = ['feature tacacs+','tacacs-server host '+str(tacacs_serv_ip)+" key "+tacacs_serv_pass]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa group server tacacs+ '+tacacs_group_name,'server '+tacacs_serv_ip]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa authentication login default group '+tacacs_group_name,'aaa authentication login console group '+tacacs_group_name]
        net_connect.send_config_set(config_commands)
    print("TACACS server yapılandırılması başarılı")

# ************************************************************AAA RULES END************************************************************************************


# ************************************************************TIMEOUT CONTROL START****************************************************************************

def do_console_timeout():
    a = input("Konsol zaman aşımını kaç dakikaya ayarlamak istersiniz? (5-10 dakika önerilir)")
    b = int(a)*60
    config_commands = ['line console', 'exec-timeout '+str(b)]
    net_connect.send_config_set(config_commands)

def do_ssh_timeout():
    a = input("Uzak oturumlar için zaman aşımını kaç dakikaya ayarlamak istersiniz? (5-10 dakika önerilir)")
    config_commands = ['line vty', 'exec-timeout '+str(a)]
    net_connect.send_config_set(config_commands)


def audit_for_lines():
    console = False
    sshses = False
    output = net_connect.send_command('sho run | section console')
    if(str.__contains__(output,"exec-timeout")):
        console = True

    output = net_connect.send_command('sho run | section vty')
    if(str.__contains__(output,"exec-timeout")):
        sshses = True

    if(console==False):
        a = input("Cihaz üzerinde konsol bağlantıları için zaman aşımı konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_console_timeout()

    if(sshses==False):
        a = input("Cihaz üzerinde uzak bağlantılar için zaman aşımı konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_ssh_timeout()


# ************************************************************TIMEOUT CONTROL END*****************************************************************************


# ************************************************************VTY ACCESS RESTRICTION START********************************************************************

def do_vty_acl():
    name = input("Oluşturulacak acl için isim giriniz : ")
    remark= input("Oluşturulacak acl için açıklama giriniz : ")
    permitted_hosts = input("Izin vereceginiz adresi [IP]/[MASK] şeklinde giriniz. (192.168.122.13/24) : ")
    config_commands = ['ip access-list '+str(name),'remark access-class '+str(remark),'permit ip '+str(permitted_hosts)+" any",'deny ip any any log']
    net_connect.send_config_set(config_commands)
    config_commands = ['line vty','access-class '+name+" in"]
    net_connect.send_config_set(config_commands)



def audit_for_vty_acl():

    acl_conf = False
    output = net_connect.send_command('sho run | section vty')
    if(str.__contains__(output,"access-class")):
        acl_conf = True

    if acl_conf == False:
        a = input("Uzak terminal oturumları için access list konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_vty_acl()


# ************************************************************VTY ACCESS RESTRICTION END***********************************************************************


# ************************************************************PASSWORD RULES START*****************************************************************************

def do_password_strength():
    config_commands = ['password strength-check']
    net_connect.send_config_set(config_commands)
    print("Güçlü şifre gereksinimleri etkinlestirildi.")

def audit_password_strenght():

    pass_strength = False
    output = net_connect.send_command('show password strength-check')
    if(str.__contains__(output,"enabled")):
        pass_strength=True

    if pass_strength==False:
        a = input("Güçlü şifre gereksinimleri konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_password_strength()


def do_userdef_lifetime():
    sifre_omru = input("Bir sifrenin kullanım ömrünü gün olarak giriniz. ")
    uyari = input("Sifrenin kullanım omru dolmadan kac gun onceden uyarılmaya baslamak istersiniz? ")
    grace=input("Kullanım omru dolduktan sonra kac gune kadar girise izin verilmesini istersiniz? ")
    config_commands = ['username '+username+' passphrase lifetime '+sifre_omru+' warntime '+uyari+' gradetime '+grace]
    net_connect.send_config_set(config_commands)
    print("Giris yaptiginiz kullanici icin sifre kullanim konfigürasyonu basariyla gerceklesti.")

def do_default_lifetime():
    sifre_omru = input("Bir sifrenin kullanım ömrünü gün olarak giriniz. ")
    uyari = input("Sifrenin kullanım omru dolmadan kac gun onceden uyarılmaya baslamak istersiniz? ")
    grace=input("Kullanım omru dolduktan sonra kac gune kadar girise izin verilmesini istersiniz? ")

    config_commands = ['userpassphrase default-warntime '+uyari,'userpassphrase default-gracetime '+grace,'userpassphrase default-lifetime '+sifre_omru]
    net_connect.send_config_set(config_commands)
    print("Default sifre kullanim konfigürasyonu basariyla gerceklesti.")

def audit_password_lifetime():

    output = net_connect.send_command('sho username '+str(username)+' passphrase timevalues')
    if str.__contains__(output, "99999"):
        a = input("Giris yaptiginiz kullanici icin sifre ömrü konfigüre edilmemis. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_userdef_lifetime()

    output = net_connect.send_command('show userpassphrase timevalues')
    if str.__contains__(output, "99999"):
        a = input("Her kullanici icin(Default) sifre ömrü konfigüre edilmemis. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a==str(1):
            do_default_lifetime()

# ************************************************************PASSWORD RULES END*******************************************************************************


# ************************************************************SNMP RULES START*********************************************************************************

def do_complex_community_str():

    cstring = input("Lütfen karmasik bir community string giriniz. ")
    config_commands = [' snmp-server community '+cstring+' ro']
    net_connect.send_config_set(config_commands)
    print("Community string başarıyla konfigüre edildi")


def audit_snmp_version():

    output = net_connect.send_command('sho snmp community')
    snmpversion=0

    if str.__contains__(output, "SNMPv1"):
        snmpversion=1
    elif str.__contains__(output, "SNMPv2"):
        snmpversion=2
    elif str.__contains__(output, "SNMPv3"):
        snmpversion=3

    if(snmpversion==2):
        a = input("SnmpV2 kullaniyorsunuz. Yeni ve karmasik bir community string ayarlamak ister misiniz? EVET[1] HAYIR[2] ")
        if(a==1):
            do_complex_community_str()
        elif a==2:
            pass
        else:
            print("Gecersiz komut.")


# ************************************************************SNMP RULES END*********************************************************************************


# ************************************************************LOGGING RULES START****************************************************************************

def do_log_server_conf():

    server_ip = input("Kayıt sunucusunun ip veya ismini giriniz. ")
    service_name = input("Kayıt altına alınacak servis isimleri giriniz. (snmpd, xml,aaa) gibi. ")
    log_level = input("0-7 arası bir log derecesi girin. ")

    config_commands = ['logging server '+server_ip,'logging level '+service_name+' '+log_level]
    net_connect.send_config_set(config_commands)
    print("Log sunucusu basariyla ayarlandi.")


def audit_logging():

    output = net_connect.send_command('sho logging server')
    if str.__contains__(output, "disabled"):
        a = input("Kayıtlar(loglar) bir sunucuya gönderilmiyor. Sunucu konfigürasyonu yapmak ister misiniz? EVET[1] HAYIR[2] ")
        if a == str(1):
            do_log_server_conf()


# ************************************************************LOGGING RULES END**********************************************************************


# ************************************************************LAYER2 RULES START*********************************************************************


def do_dhcp_trust():

    vlans = input("Etkinleştirmek istediginiz vlanleri giriniz. (100 veya 200-202 gibi) ")
    trusted = input("Güvenilir port-channel giriniz (1-4096")
    config_commands = ['ip dhcp snooping','ip dhcp snooping vlan '+vlans]
    net_connect.send_config_set(config_commands)
    config_commands = ['interface port-channel '+trusted,'ip dhcp snooping trust']
    net_connect.send_config_set(config_commands)


def audit_dhcp_trust():

    output = net_connect.send_command('show running-config dhcp')
    if str.__contains__(output, "service dhcp"):
        if str.__contains__(output, "ip dhcp snooping"):
            pass
        else:
            a = input("DHCP Trust konfigüre edilmemis. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
            if a == str(1):
                do_dhcp_trust()

# ************************************************************LAYER2 RULES END************************************************************************


# ************************************************************BACKUPS START***************************************************************************

def do_local_backup():

    isim = input("İsim giriniz. ")
    sure = input("Aylik yedekleme[1] Haftalik yedekleme[2] : ")

    if sure==str(1):
        ay = input("Her ay ayin kacinci gunu yedekleme yapmak istersiniz? (1-30)")
        config_commands = ['feature scheduler','scheduler job name '+isim,'copy running-config startup-config']
        net_connect.send_config_set(config_commands)
        config_commands = ['scheduler schedule name '+isim,'time monthly '+ay]
        net_connect.send_config_set(config_commands)

    elif sure==str(2):
        gun = input("Her hafta kacinci gun yedekleme yapmak istersiniz? (1-7) ")
        config_commands = ['feature scheduler','scheduler job name '+isim,'copy running-config startup-config']
        net_connect.send_config_set(config_commands)
        onfig_commands = ['scheduler schedule name '+isim,'time weekly '+gun]
        net_connect.send_config_set(config_commands)
    else:
        print("Gecersiz komut.")



def local_backup_audit():

    output = net_connect.send_command('sho scheduler job')
    if str.__contains__(output,"Invalid"):
        a = input("Yerel yedekleme konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
        if a == str(1):
            do_local_backup()
    else:
        if str.__contains__(output,"copy running-config startup-config"):
            pass
        else:
            a = input("Yerel yedekleme konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2] ")
            if a == str(1):
                do_local_backup()



# ************************************************************BACKUPS END**********************************************************************

# ************************************************************VLAN SECURITY START**************************************************************

def do_move_ports():

    output = net_connect.send_command('show vlan br | section default')
    print("**********************************************************************")
    print(output)
    print("**********************************************************************")
    a = input("Yukarida default vlande gorunen portlari giriniz. (Eth2/2,Eth2/3...) ")
    a = a.split(",")
    vlan_num = input("Kullanilmayan bir vlan numarasi giriniz. ")
    shut = input("Bu portları shutdown durumuna getirmek ister misiniz? EVET[1] HAYIR[2] ")

    config_commands = ['vlan '+vlan_num,'no sh']
    net_connect.send_config_set(config_commands)

    for i in range(len(a)):
        config_command1 = ['int '+a[i],'switchport access vlan '+vlan_num]
        net_connect.send_config_set(config_command1)
        if shut == str(1):
            config_command2 = ['int '+a[i],'sh']
            net_connect.send_config_set(config_command2)



def audit_empty_ports():
    output = net_connect.send_command('show vlan br | section default')
    if str.__contains__(output,"Eth"):
        a = input("Defaul vlan 1 de acik portlariniz bulunmakta. Baska vlan'e tasimak ister misiniz? EVET[1] HAYIR[2] ")
        if a ==str(1):
            do_move_ports()


def do_trunk_native():

    output = net_connect.send_command('show int trunk | grep next 5 Native')
    print("**********************************************************************")
    print(output)
    print("**********************************************************************")
    a = input("Native vlan 1 de bulunan arayüzleri giriniz. (Eth3/4,Eth2/1 gibi) ")
    newNative = input("Yeni bir native vlan giriniz. ")

    a = a.split(",")

    for i in range(len(a)):

        config_command2 = ['int '+a[i],'switchport trunk native vlan '+newNative]
        net_connect.send_config_set(config_command2)





def audit_trunk_natives():

    output = net_connect.send_command('show int trunk | grep next 5 Native | section trunking')
    liste = output.split("   ")
    newList = []
    a = ""
    for i in range(len(liste)):
        newList.append(liste[i].lstrip())

    for i in range(len(newList)):
        if newList[i]=='1':
            a=input("Trunk portlardan native vlan'i 1 olarak yapılandirilmis portlar bulunmakta. Degistirmek ister misiniz? EVET[1] HAYIR[2] ")

    if a==str(1):
        do_trunk_native()



# ************************************************************VLAN SECURITY END****************************************************************


# ************************************************************TELNET DISABLING START*********************************************************************


def do_disable_telnet():

    config_commands = ['no feature telnet']
    net_connect.send_config_set(config_commands)
    print("Telnet erisimi kapatildi.")


def audit_telnet():

    output = net_connect.send_command('show feature | i telnetServer')
    if str.__contains__(output,"enabled"):
        a = input("Cihaza telnet erişimi açık durumda. Kapatmak ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_disable_telnet()
        else:
            pass


# ************************************************************TELNET DISABLING END*********************************************************************



