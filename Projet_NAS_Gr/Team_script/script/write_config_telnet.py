import telnetlib
import time
# import json

#data test pour la fonction
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
    sentence = str(tn.read_very_eager())
    word = router["name"]+'#'
    if not(word in sentence):
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



#test
# config(data['data'][1],1)