from format_config.interfaces_c7200 import interfaces_c7200

def formatageHostName(entete,router):
	S = entete + "\n"+"hostname "+router["name"]+"\n"
	return S

def formatageCorp1(config,corp1):
	S = config + corp1 +"\n"
	return S

def formatageCorp2(config,corp2):
	S = config + corp2 +"\n"
	return S

def formatageInterface(config,router):
	S = config
	for i in range(0,len(router["interfaces"])):
		S = S + "interface "+router["interfaces"][i]["name"]+"\n"+"ip address "+router["interfaces"][i]["ipv4"]+"\n"+"!"+"\n"	
	return S

def formatageCorp3(config,corp3):
	S = config + corp3 +"\n"
	return S

def formatageFin(config,fin):
	S = config + fin 
	return S

def formatageRouter(router):

	entetefilename = "./format_config/entete.txt"
	corp1filename = "./format_config/corp1.txt"
	corp2filename = "./format_config/corp2.txt"
	corp3filename = "./format_config/corp3.txt"
	finfilename = "./format_config/fin.txt"
	a = open(entetefilename, 'r')
	entete = a.read()
	a.close()

	b = open(corp1filename, 'r')
	corp1 = b.read()
	b.close()

	c = open(corp2filename, 'r')
	corp2 = c.read()
	c.close()

	d = open(corp3filename, 'r')
	corp3 = d.read()
	d.close()

	e = open(finfilename, 'r')
	fin = e.read()
	e.close()

	A = formatageHostName(entete,router)
	B = formatageCorp1(A,corp1)
	# C = formatageCorp2(B,corp2)
	D = formatageInterface(B,router)
	# E = formatageCorp3(D,corp3)
	F = formatageFin(D,fin)
	return F




	# S = config
	# for i in range(0,len(interfaces_c7200)):
	# 	inter =""
	# 	for j in range(0,len(router["interface"]))  :
	# 		if  interfaces_c7200[i]["name"] == router["interface"][j]["name"] : 
	# 			inter = "interface "+router["interface"][j]["name"]+"\n"+"ip address "+router["interface"][j]["ipv4"]+"\n"
	# 			break
	# 		# else :
	# 		# 	inter = "interface "+interfaces_c7200[i]["name"]+"\n"+"no ip address"+"\n"+"shutdown"+"\n"+"duplex full"+"\n"+"negotiation auto"+"\n"+"!"+"\n"
	# 		#inter = "interface "+router["interface"][j]["name"]+"\n"+"ip address "+router["interface"][j]["ipv4"]+"\n"+"negotiation auto"+"\n"+"!"+"\n"
	# 	S = S + inter