#configuring multiple routers
import getpass
import telnetlib

#Ask for username and password

HOST = "192.168.99.1"
user = input("Enter your username: ")
password = getpass.getpass() #equivalent à input(), utilisé pr les mdp pr pas afficher ce qu'on saisit
count=0 
ips=open("myrouters.txt") #créé une var ips= contenu du fichier spécifié
#le fichier contient les @ip de nos routeurs->à remplacer par un json
"As you add IPs to this file, ensure you have no spaces between the contents or at the end of the file as Python will read this as well and experience an error"
for IP in ips:
	count +=1
	counter=bytes((str(count)).encode())
	routerid=bytes((str(count) +"."+str(count) +"."+str(count)+"."+str(count)).encode())
	IP=IP.strip()
	print("Currently configuring router" +(IP))
	HOST=IP
	tn=telnetlib.Telnet(HOST)
	tn.read_until(b"Username:")
	tn.write(user.encore('ascii') +b"\n")
	if password:
		tn.read_until(b"Password: ")
		tn.write(password.encode('ascii')+b"\n")
	tn.write(b"enable\n")
	tn.write(b"class\n")
	tn.write(b"config t\n")
	tn.write(b"router ospf 1\n")
	tn.write(b"network 0.0.0.0 255.255.255.255 area 0\n")
	tn.write(b"router-id")
	tn.write(routerid)
	tn.write(b"\n")
	tn.write(b"exit\n")
	tn.write(b"interface gi0/0\n")
	tn.write(b"ip address 172.168.1."+str(count).encode('ascii')+b"255.255.255.0\n")
	tn.write(b"no shut\n")	
	tn.write(b"do write\n")	
	tn.write(b"exit\n")
	for n in range (100,110):	
		tn.write(b"interface loopback"+str(n).encode('ascii')+b"\n")	
		tn.write(b"ip address "+str(count).encode('ascii')+b"."+str(count).encode('ascii')+b"."+str(count).encode('ascii')+b"."+str(n).encode('ascii') +b"255.255.255.255\n")
	tn.write(b"end\n")
	tn.write(b"exit\n")
	printf(tn.read_all().decode('ascii'))
		
