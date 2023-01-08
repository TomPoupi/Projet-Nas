import gns3fy
from write_config_telnet import *
import json
import multiprocess

# pip install pydantic=1.9
#fichier .json data des routers
f = open("./data.json",'r')
data = json.loads(f.read())
f.close()

#ouverture et connection du projet de l'app gns3

gns3_server = gns3fy.Gns3Connector("http://localhost:3090")
lab = gns3fy.Project(name="script", connector=gns3_server)
lab.get()
project_id = lab.project_id
lab.open()


# fonction qui del tous les routers de mon projet
def delete_node(lab) :
    for node in lab.nodes:
        node.delete()


# fonction qui créer les routers en fonction de la data.json, les places sur le schéma 
def create_node(routers) :
    norme_coor = 100
    for i in range(0,len(routers)):
        router = i
        X = routers[i]["X"] * norme_coor
        Y = routers[i]["Y"] * norme_coor
   
        router = gns3fy.Node(name=routers[i]["name"],connector=gns3_server, project_id=project_id,template="c7200",x=X,y=Y)
        router.create()

        # config=formatageRouter(routers[i])
        # router.write_file(path='./configs/i'+str(i+1)+'_startup-config.cfg',data=config)

# fonction qui prend les routers de la data.json et fait un tableau de dictionnaire. key :interface, element : couple de router
# pour le moment la data.json fera en sorte que pour un lien on utilisera une même interface dans les 2 routers 
def tab_de_tab_link(routers) :
    tab_link = []
    tab_link_final =[]
    for i in range(0,len(routers)) :
        lien=[]
        inter1=[]
        inter2=[]
        for j in range(0,len(routers[i]["interfaces"])) :
            if routers[i]["interfaces"][j]["neighbor"] != "No" :
                inter1 = [routers[i]["name"],routers[i]["interfaces"][j]["name"]]
                inter2 = [routers[i]["interfaces"][j]["neighbor"],"Null"]
                lien = [inter1,inter2]
                
                for k in range(0,len(tab_link)) :
                    if tab_link[k][0][0] == routers[i]["interfaces"][j]["neighbor"] and tab_link[k][1][0] == routers[i]["name"] :
                        tab_link[k][1][1] = routers[i]["interfaces"][j]["name"]

                tab_link.append(lien)

    # pour éliminer les doublons
    for k in range(0,len(tab_link)) :
        if tab_link[k][1][1] != "Null" :
            tab_link_final.append(tab_link[k])
                  
    return tab_link_final

#fonction qui créer les liens sur gns3 à partir du tab de lien 
def create_link(tab_link) :
    for i in range(0,len(tab_link)) :
        lab.create_link(tab_link[i][0][0], tab_link[i][0][1], tab_link[i][1][0], tab_link[i][1][1])

#fonction qui reccupere les voisins CE des PE
def PE_neighbor (router):
    tab_CE=[]
    for j in range (0,len(router['interfaces'])):
        for i in range (0,len(data['data'])):
            if (data['data'][i]['name']==router['interfaces'][j]['neighbor']):
                if (data['data'][i]['role'] == "CE"):
                    tab_CE.append(data['data'][i])

    return tab_CE
#print(PE_neighbor(data['data'][5]))

def other_PE(router):
    tab_PE=[]
    for i in range (0,len(data['data'])):
        if not(data['data'][i]['name']==router['name']):
            if (data['data'][i]['role'] == "PE"):
                tab_PE.append(data['data'][i])

    return tab_PE
#print(other_PE(data['data'][5]))

# fonction qui configure en telnet les routers
def config_router(i,router):
    r = lab.get_node("R"+str(i+1))
    
    # on attend que le router est bien up avant de les configs en telnet
    while True :
        if r.status == "started":
            break
    #fonction config en telnet, r.console = port tcp , pour connection avec le router
    if router["role"]=="PE" :
        config_telnet_PE(router,i,r.console,PE_neighbor(router),other_PE(router))
    elif router["role"]=="R" :
        config_telnet_R(router,i,r.console)
    elif router["role"]=="CE" :
        config_telnet_CE(router,i,r.console,other_PE(router))
    else:
        config_telnet(router,i,r.console)
#print(tab_dictionnaire_link(data['data']))

if __name__ == '__main__':

    delete_node(lab)
    create_node(data['data'])
    lab.get()
    create_link(tab_de_tab_link(data['data']))
    lab.get()
    lab.start_nodes()

    # start des process pour config les routers, 1 process/ router
    processes = [multiprocess.Process(target=config_router, args=(i, data['data'][i])) for i in range(len(data['data']))]


    for process in processes:
       process.start()


    for process in processes:
       process.join()



