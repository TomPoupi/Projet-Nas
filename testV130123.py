import tkinter as tk
import json
import functools
import numpy as np


def submit_interface(tab, resultat):
    name="R"
    with open('exemple.json', 'r') as f:
        js = json.load(f)
        #num=len(js['data'])
        num=0
        num=num+1
        name=name+str(num)
        
        ospf=tab[0]
        id_router=tab[1]
        x = tab[2]
        y = tab[3]
        nb_voisins = tab[4]
        
        ip_loopback = str(num) + "." + str(num) + "." + str(num) + "." + str(num) + " 255.255.255.255"
        interface_tab = [{"name": "Loopback1", "ipv4": ip_loopback,"neighbor":"No"}]
        
        name="R"
        for v in range(int(nb_voisins)):
            interf = str(resultat[v][0])
            ip = str(resultat[v][1])
            neighbor = name + str(resultat[v][2])
            
            interface = {
				"name": interf,
				"ipv4": ip,
				"neighbor": neighbor
			}
            
            json_object = json.dumps(interface, indent=4)
            interface_tab.append(interface)
        
        json_object = json.dumps(interface_tab, indent=4)
         
        data= {
		    "name": name,
		    "role": "R",
		    "ospf": [{"process":str(num), "area": ospf, "router-id": id_router}],
		    "X":x,
		    "Y":y,
		    "interfaces": interface_tab
		}
        #js['data'][x-1].append({"process":str(x), "area":"0" , "router-id": "1.1.1.1"})
		# Serializing json
        json_object = json.dumps(data, indent=4)
        
        with open('exemple.json', 'w') as f1:
            f1.write(json_object)
            
def submit_R(tab):
    
       
        ospf = str(tab[0].get())
        id_router = str(tab[1].get())
        x = str(tab[2].get())
        y = str(tab[3].get())
        nb_voisins = str(tab[4].get())
        tab = [ospf, id_router, x, y, nb_voisins]
            
        Def_interface(tab)
    
def AjoutR():
    
	for widget in root.winfo_children():
		widget.destroy()
    
	first_row_frame = tk.Frame(root)
	first_row_frame.pack(pady=10)
	# Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
	label = tk.Label(first_row_frame, text="Remplir le formulaire:")
	label.pack()
	
	# Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
	ospf_label = tk.Label(first_row_frame, text="ospf area:")
	ospf_label.pack()

	ospf_entry = tk.Entry(first_row_frame)
	ospf_entry.pack()

	# Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
	routerid_label = tk.Label(root, text="router-id:")
	routerid_label.pack()
	
	routerid_entry = tk.Entry(root)
	routerid_entry.pack()
	
	# Création d'un label pour indiquer à l'utilisateur de saisir X
	X_label = tk.Label(root, text="X=")
	X_label.pack()
	
	X_entry = tk.Entry(root)
	X_entry.pack()
	
	# Création d'un label pour indiquer à l'utilisateur de saisir Y
	Y_label = tk.Label(root, text="Y=")
	Y_label.pack()

	# Création d'une zone de saisie pour que l'utilisateur puisse entrer son nombre de routeurs CE
	Y_entry = tk.Entry(root)
	Y_entry.pack()

	voisins_label = tk.Label(root, text="Combien de voisins a-t-il ?")
	voisins_label.pack()
	
	voisins_entry = tk.Entry(root)
	voisins_entry.pack()
	
	tab_entry = [ospf_entry, routerid_entry, X_entry, Y_entry, voisins_entry]
    
	# Création d'un bouton de soumission
	submit_button = tk.Button(root, text="Soumettre", command=functools.partial(submit_R,tab_entry))
	submit_button.pack()
    

def window1():
    
    # Création d'un frame pour contenir la première ligne du formulaire
    first_row_frame = tk.Frame(root)
    first_row_frame.pack(pady=10)

    # Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
    num_pe_routers_label = tk.Label(first_row_frame, text="Choisir une option:")
    num_pe_routers_label.pack()

      
    # Création d'un bouton de soumission
    submit_button = tk.Button(root, text="Ajouter un Routeur R", command=AjoutR)
    submit_button.pack()
    # Création d'un bouton de soumission
    submit_button = tk.Button(root, text="Ajouter un Routeur PE", command=AjoutR)
    submit_button.pack()
    # Création d'un bouton de soumission
    submit_button = tk.Button(root, text="Ajouter un Routeur CE", command=AjoutR)
    submit_button.pack()
    # Création d'un bouton de soumission
    submit_button = tk.Button(root, text="Supprimer un Routeur", command=AjoutR)
    submit_button.pack()


def back1():
    
    for widget in root.winfo_children():
        widget.destroy()
        
    # On retourne à la première fenêtre
    window1()

def Def_interface(tab):

	nb_voisins = tab[4]
	resultat = [['0']*3]*int(nb_voisins)
	
	for widget in root.winfo_children():
		widget.destroy()
    
	for i in range(int(nb_voisins)):
		first_row_frame = tk.Frame(root)
		first_row_frame.pack(pady=10)

		# Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
		id_voisin_label = tk.Label(root, text="Numéro du routeur voisin :")
		id_voisin_label.pack()
		id_voisin_entry = tk.Entry(root)
		id_voisin_entry.pack()
  
		interface_label = tk.Label(root, text="Nom de l'interface :")
		interface_label.pack()
		interface_entry = tk.Entry(root)
		interface_entry.pack()
  
		ip_label = tk.Label(root, text="adresse ip liée à l'interface :")
		ip_label.pack()
		ip_entry = tk.Entry(root)
		ip_entry.pack()

	for i in range(nb_voisins):
		id_voisin=str(id_voisin_entry.get())
		interface=str(interface_entry.get())
		ip=str(ip_entry.get())
		resultat[i][0] = interface 
		resultat[i][1] = ip
		resultat[i][2] = id_voisin
  
	submit_button = tk.Button(root, text="Soumettre", command=functools.partial(submit_interface,tab, resultat))
	submit_button.pack()
    

    
    
# Création de la fenêtre principale
root = tk.Tk()
with open('exemple.json', 'w') as f1:
	ex={
		"data":[]
	}
	# Serializing json
	json_object = json.dumps(ex)
	# Writing in json
	f1.write(json_object)
root.title("Formulaire de commande de routeurs")
root.geometry("600x300")
window1()


# Affichage de la fenêtre
root.mainloop() 
