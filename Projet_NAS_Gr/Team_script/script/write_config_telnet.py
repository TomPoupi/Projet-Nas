import telnetlib
import time
# import json

# #data test pour la fonction
# f = open("./data.json",'r')
# data = json.loads(f.read())
# f.close()



def config_telnet(router,i,port) :

    print(router["name"]+" : start to work")

    HOST = "127.0.0.1"
    PORT = str(port)

    tn = telnetlib.Telnet(HOST,PORT)

    #read_until fait d'office de while, càd tant que je n'ai pas lu ça : "%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down" j'att,
    # du coup ça permet de dire exactement au process ce qu'il doit faire avant d'écrire sur le terminal du router
    tn.read_until(b"%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down")


    # cette partie vérifie si c'est ta 1er connection 
    # en gros si c'est ta 1er connection sur le router tu ne vas pas voir R1#
    time.sleep(5)
    senquence = str(tn.read_very_eager())
    word = router["name"]+'#'
    if not(word in senquence):
        # permet de faire comme si tu appuyais sur la touche "entré"
        tn.write(b"\r\n")
   

    # le b de b"\r\n" est essentielle pour convertir ton string en byte et ainsi écrire sur le terminal du router 
    tn.write(b"\r\n")

    #le process att tant qu'il a pas vu "R1#"
    tn.read_until(router["name"].encode('ascii')+b"#")
   

    
    tn.write(b"conf t\r\n")
    tn.read_until(router["name"].encode('ascii')+b"(config)#")

    #pour chaque interface de la data.json concernant le router du process je config ipv4 
    for interface in router["interfaces"] :
        #print("interface : "+ interface["name"])


        #même idée que le b"" , le var.encode('ascii') permet d'encoder ta variable pour l'envoyer sur le terminal du router
        tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
        tn.write(b"ip address "+ interface["ipv4"].encode('ascii') + b"\r\n")
        tn.write(b"no shutdown\r\n")

        # j'att que l'interface soit bien up avant de leave
        tn.read_until(b"Line protocol on Interface "+ interface["name"].encode('ascii') + b", changed state to up")
        tn.write(b"exit\r\n")

   

    tn.write(b"exit\r\n")

    #j'att que la modification soit bien prise en compte avant leave la connection avec tn.close()
    tn.read_until(router["name"].encode('ascii')+b"#")
    tn.read_until(b"Configured from console by console")
    tn.close()

    print(router["name"]+" : all work done")





def config_telnet_R(router,i,port) :

    print(router["name"]+" : start to work")

    HOST = "127.0.0.1"
    PORT = str(port)

    tn = telnetlib.Telnet(HOST,PORT)

    #read_until fait d'office de while, càd tant que je n'ai pas lu ça : "%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down" j'att,
    # du coup ça permet de dire exactement au process ce qu'il doit faire avant d'écrire sur le terminal du router
    tn.read_until(b"%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down")


    # cette partie vérifie si c'est ta 1er connection 
    # en gros si c'est ta 1er connection sur le router tu ne vas pas voir R1#
    time.sleep(5)
    senquence = str(tn.read_very_eager())
    word = router["name"]+'#'
    if not(word in senquence):
        # permet de faire comme si tu appuyais sur la touche "entré"
        tn.write(b"\r\n")
   

    # le b de b"\r\n" est essentielle pour convertir ton string en byte et ainsi écrire sur le terminal du router 
    tn.write(b"\r\n")

    #le process att tant qu'il a pas vu "R1#"
    tn.read_until(router["name"].encode('ascii')+b"#")
   

    
    tn.write(b"conf t\r\n")
    tn.read_until(router["name"].encode('ascii')+b"(config)#")

    #pour chaque interface de la data.json concernant le router du process je config ipv4 
    for interface in router["interfaces"] :
        #print("interface : "+ interface["name"])


        #même idée que le b"" , le var.encode('ascii') permet d'encoder ta variable pour l'envoyer sur le terminal du router
        tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
        tn.write(b"ip address "+ interface["ipv4"].encode('ascii') + b"\r\n")
        tn.write(b"no shutdown\r\n")

        # j'att que l'interface soit bien up avant de leave
        tn.read_until(b"Line protocol on Interface "+ interface["name"].encode('ascii') + b", changed state to up")
        tn.write(b"exit\r\n")

    #partie OSPF
    tn.write(b"router ospf "+router["ospf"][0]["process"].encode('ascii')+b"\r\n")
    tn.write(b"router-id "+router["ospf"][0]["router-id"].encode('ascii')+b"\r\n")
    tn.write(b"exit\r\n")

    for interface in router["interfaces"] :
        tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
        tn.write(b"ip ospf "+router["ospf"][0]["process"].encode('ascii')+b" area "+router["ospf"][0]["area"].encode('ascii')+b"\r\n")
        tn.write(b"exit\r\n")


    #partie MPLS
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")

    tn.write(b"interface " + b"Loopback1" + b"\r\n")
    tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
    tn.write(b"mpls ldp router-id Loopback1\r\n")

    for interface in router["interfaces"] :
        if not(interface["name"]=="Loopback1") :
            tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
            tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
            tn.write(b"mpls ip\r\n")
            tn.write(b"exit\r\n")


    tn.write(b"exit\r\n")
    #j'att que la modification soit bien prise en compte avant leave la connection avec tn.close()
    tn.read_until(router["name"].encode('ascii')+b"#")
    tn.read_until(b"Configured from console by console")
    tn.close()

    print(router["name"]+" : all work done")





def config_telnet_PE(router,i,port,CE_neighbors, PE_neighbors) :

    print(router["name"]+" : start to work")

    HOST = "127.0.0.1"
    PORT = str(port)

    tn = telnetlib.Telnet(HOST,PORT)

    #read_until fait d'office de while, càd tant que je n'ai pas lu ça : "%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down" j'att,
    # du coup ça permet de dire exactement au process ce qu'il doit faire avant d'écrire sur le terminal du router
    tn.read_until(b"%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down")


    # cette partie vérifie si c'est ta 1er connection 
    # en gros si c'est ta 1er connection sur le router tu ne vas pas voir R1#
    time.sleep(5)
    senquence = str(tn.read_very_eager())
    word = router["name"]+'#'
    if not(word in senquence):
        # permet de faire comme si tu appuyais sur la touche "entré"
        tn.write(b"\r\n")
   

    # le b de b"\r\n" est essentielle pour convertir ton string en byte et ainsi écrire sur le terminal du router 
    tn.write(b"\r\n")

    #le process att tant qu'il a pas vu "R1#"
    tn.read_until(router["name"].encode('ascii')+b"#")
   

    
    tn.write(b"conf t\r\n")
    tn.read_until(router["name"].encode('ascii')+b"(config)#")

    #pour chaque interface de la data.json concernant le router du process je config ipv4 
    for interface in router["interfaces"] :
        #print("interface : "+ interface["name"])


        #même idée que le b"" , le var.encode('ascii') permet d'encoder ta variable pour l'envoyer sur le terminal du router
        tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
        tn.write(b"ip address "+ interface["ipv4"].encode('ascii') + b"\r\n")
        tn.write(b"no shutdown\r\n")

        # j'att que l'interface soit bien up avant de leave
        tn.read_until(b"Line protocol on Interface "+ interface["name"].encode('ascii') + b", changed state to up")
        tn.write(b"exit\r\n")

    #partie OSPF
    tn.write(b"router ospf "+router["ospf"][0]["process"].encode('ascii')+b"\r\n")
    tn.write(b"router-id "+router["ospf"][0]["router-id"].encode('ascii')+b"\r\n")
    tn.write(b"exit\r\n")

    for interface in router["interfaces"] :
        if interface["config_ospf_mpls"] == True :
            tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
            tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
            tn.write(b"ip ospf "+router["ospf"][0]["process"].encode('ascii')+b" area "+router["ospf"][0]["area"].encode('ascii')+b"\r\n")
            tn.write(b"exit\r\n")


    #partie MPLS
    tn.write(b"mpls ip\r\n")
    tn.write(b"mpls label protocol ldp\r\n")

    tn.write(b"interface " + b"Loopback1" + b"\r\n")
    tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
    tn.write(b"mpls ldp router-id Loopback1\r\n")

    for interface in router["interfaces"] :
        if not(interface["name"]=="Loopback1") :
            if interface["config_ospf_mpls"] == True :
                tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
                tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
                tn.write(b"mpls ip\r\n")
                tn.write(b"exit\r\n")

    #partie VRF
    for ce in CE_neighbors:
        tn.write(b"ip vrf "+ce["vrf"][0]["name"].encode('ascii')+b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-vrf)#")
        tn.write(b"rd "+ce["vrf"][0]["rd"].encode('ascii')+b"\r\n")
        # tn.write(b"route-target import "+ce["vrf"][0]["rd"].encode('ascii')+b"\r\n")
        # tn.write(b"route-target export "+ce["vrf"][0]["rd"].encode('ascii')+b"\r\n")
        if ce["vrf"][0]["route"]!= None :
            for i in range(len(ce["vrf"][0]["route"])):
                tn.write(b"route-target import "+ce["vrf"][0]["route"][i]["name"].encode('ascii')+b"\r\n")
                tn.write(b"route-target export "+ce["vrf"][0]["route"][i]["name"].encode('ascii')+b"\r\n")

        tn.write(b"exit\r\n")
    
    for interface in router["interfaces"] :
        if (interface["config_ospf_mpls"] == False) :
            tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
            tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
            for ce in CE_neighbors:
                if interface["neighbor"] == ce["name"]:
                    tn.write(b"ip vrf forwarding "+ce["vrf"][0]["name"].encode('ascii')+b"\r\n")
                    tn.write(b"ip address "+ interface["ipv4"].encode('ascii') + b"\r\n")
                    tn.write(b"no shutdown\r\n")

                    # j'att que l'interface soit bien up avant de leave
                    # tn.read_until(b"Line protocol on Interface "+ interface["name"].encode('ascii') + b", changed state to up")
                    tn.write(b"exit\r\n")

    #là c'est robuste
    for ce in CE_neighbors:
        for i in range(len(ce["interfaces"])):
            if ce["interfaces"][i]["name"]=="Loopback1":
                Loopback=ce["interfaces"][i]["ipv4"]

            if ce["interfaces"][i]["neighbor"]==router["name"]:
                Int=ce["interfaces"][i]["ipv4"]
                myInt = Int.split( )
        tn.write(b"ip route vrf "+ce["vrf"][0]["name"].encode('ascii')+b" "+Loopback.encode('ascii')+b" "+myInt[0].encode('ascii') + b"\r\n")

    #Partie BGP
    tn.write(b"router bgp "+router["bgp"][0]["process"].encode('ascii')+ b"\r\n")
    tn.read_until(router["name"].encode('ascii')+ b"(config-router)#")
    tn.write(b"bgp router-id "+router["bgp"][0]["router-id"].encode('ascii')+b"\r\n")

    for pe in PE_neighbors:
        tn.write(b"neighbor "+pe["bgp"][0]["router-id"].encode('ascii')+b" remote-as "+router["bgp"][0]["process"].encode('ascii')+ b"\r\n")
        tn.write(b"neighbor "+pe["bgp"][0]["router-id"].encode('ascii')+b" update-source loopback1\r\n")
        tn.write(b"address-family vpnv4\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-router-af)#")
        tn.write(b"neighbor "+pe["bgp"][0]["router-id"].encode('ascii')+b" activate\r\n")
        tn.write(b"neighbor "+pe["bgp"][0]["router-id"].encode('ascii')+b" next-hop-self\r\n")
        tn.write(b"neighbor "+pe["bgp"][0]["router-id"].encode('ascii')+b" send-community both\r\n")
        tn.write(b"exit\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-router)#")

    for ce in CE_neighbors:
        tn.write(b"address-family ipv4 vrf "+ce["vrf"][0]["name"].encode('ascii')+b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-router-af)#")
        tn.write(b"redistribute static\r\n")
        tn.write(b"redistribute connected\r\n")
        for interface in ce["interfaces"] :
            if interface["neighbor"]==router["name"]:
                Int=interface["ipv4"]
                myInt = Int.split( )
                tn.write(b"neighbor "+myInt[0].encode('ascii')+b" remote-as "+ce["bgp"][0]["process"].encode('ascii')+b"\r\n")
                tn.write(b"neighbor "+myInt[0].encode('ascii')+b" activate"+b"\r\n")
        tn.write(b"exit\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-router)#")

    tn.write(b"exit\r\n")
    tn.write(b"exit\r\n")
    #j'att que la modification soit bien prise en compte avant leave la connection avec tn.close()
    tn.read_until(router["name"].encode('ascii')+b"#")
    tn.read_until(b"Configured from console by console")
    tn.close()

    print(router["name"]+" : all work done")



def config_telnet_CE(router,i,port,PE_neighbors) :

    print(router["name"]+" : start to work")

    HOST = "127.0.0.1"
    PORT = str(port)

    tn = telnetlib.Telnet(HOST,PORT)

    #read_until fait d'office de while, càd tant que je n'ai pas lu ça : "%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down" j'att,
    # du coup ça permet de dire exactement au process ce qu'il doit faire avant d'écrire sur le terminal du router
    tn.read_until(b"%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet6/0, changed state to down")


    # cette partie vérifie si c'est ta 1er connection 
    # en gros si c'est ta 1er connection sur le router tu ne vas pas voir R1#
    time.sleep(5)
    senquence = str(tn.read_very_eager())
    word = router["name"]+'#'
    if not(word in senquence):
        # permet de faire comme si tu appuyais sur la touche "entré"
        tn.write(b"\r\n")
   

    # le b de b"\r\n" est essentielle pour convertir ton string en byte et ainsi écrire sur le terminal du router 
    tn.write(b"\r\n")

    #le process att tant qu'il a pas vu "R1#"
    tn.read_until(router["name"].encode('ascii')+b"#")
   

    
    tn.write(b"conf t\r\n")
    tn.read_until(router["name"].encode('ascii')+b"(config)#")

    #pour chaque interface de la data.json concernant le router du process je config ipv4 
    for interface in router["interfaces"] :
        #print("interface : "+ interface["name"])


        #même idée que le b"" , le var.encode('ascii') permet d'encoder ta variable pour l'envoyer sur le terminal du router
        tn.write(b"interface " + interface["name"].encode('ascii') + b"\r\n")
        tn.read_until(router["name"].encode('ascii')+ b"(config-if)#")
        tn.write(b"ip address "+ interface["ipv4"].encode('ascii') + b"\r\n")
        tn.write(b"no shutdown\r\n")

        # j'att que l'interface soit bien up avant de leave
        tn.read_until(b"Line protocol on Interface "+ interface["name"].encode('ascii') + b", changed state to up")
        tn.write(b"exit\r\n")
    
    #BGP
    tn.write(b"router bgp "+router["bgp"][0]["process"].encode('ascii')+ b"\r\n")
    tn.read_until(router["name"].encode('ascii')+ b"(config-router)#")
    tn.write(b"bgp router-id "+router["bgp"][0]["router-id"].encode('ascii')+b"\r\n")
    tn.write(b"address-family ipv4\r\n")
    tn.read_until(router["name"].encode('ascii')+ b"(config-router-af)#")

    for pe in PE_neighbors:
        for i in range(len(pe["interfaces"])):
            if pe["interfaces"][i]["neighbor"]==router["name"]:
                Int=pe["interfaces"][i]["ipv4"]
                myInt = Int.split( )
                tn.write(b"neighbor "+myInt[0].encode('ascii')+b" remote-as "+pe["bgp"][0]["process"].encode('ascii')+b"\r\n")
                tn.write(b"neighbor "+myInt[0].encode('ascii')+b" activate"+b"\r\n")  

    tn.write(b"exit\r\n")
    tn.write(b"exit\r\n")
    tn.write(b"exit\r\n")

    #j'att que la modification soit bien prise en compte avant leave la connection avec tn.close()
    tn.read_until(router["name"].encode('ascii')+b"#")
    tn.read_until(b"Configured from console by console")
    tn.close()

    print(router["name"]+" : all work done")








#test
#config_telnet_PE(data['data'][5],5,5005)