import gns3fy
from write_config import *
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
#lab.open()


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
def tab_dictionnaire_link(routers) :
    tab_link = []
    for i in range(0,len(routers)) :
        link={}
        couple=[]
        for j in range(0,len(routers[i]["interfaces"])) :
            if routers[i]["interfaces"][j]["neighbor"] != "No" :
                couple = [routers[i]['name'],routers[i]["interfaces"][j]["neighbor"]]
                
                #pour éviter d'avoir des doublons
                s=0
                for k in range(0,len(tab_link)) :
                    for lien in tab_link[k]:
                        if tab_link[k][lien] == couple or tab_link[k][lien] == couple[::-1]:
                            s = s + 1
                if s == 0 :
                    link[routers[i]["interfaces"][j]["name"]] = couple
        if len(link)!= 0 :
            tab_link.append(link)
    return tab_link

#fonction qui créer les liens sur gns3 à partir du tab de lien 
def create_link(tab_link) :
    for i in range(0,len(tab_link)) :
        for key ,interface in tab_link[i].items():
                lab.create_link(interface[0], key, interface[1],key)



# fonction qui configure en telnet les routers
def config_router(i,router):
    r = lab.get_node("R"+str(i+1))
    # on attend que le router est bien up avant de les configs en telnet
    while True :
        if r.status == "started":
            break
    #fonction config en telnet
    config_telnet(router,i)


if __name__ == '__main__':

    delete_node(lab)
    create_node(data['data'])
    lab.get()
    create_link(tab_dictionnaire_link(data['data']))
    lab.get()
    lab.start_nodes()

    # start des process pour config les routers, 1 process/ router
    processes = [multiprocess.Process(target=config_router, args=(i, data['data'][i])) for i in range(len(data['data']))]


    for process in processes:
        process.start()


    for process in processes:
        process.join()



