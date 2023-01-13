import tkinter as tk
import json
import functools
		
def AjoutR():
	for widget in root.winfo_children():
            widget.destroy()
	# Création d'un frame pour contenir la première ligne du formulaire
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
	
	tab_entry = [ospf_entry, routerid_entry, X_entry, Y_entry]
    
	# Création d'un bouton de soumission
	submit_button = tk.Button(root, text="Soumettre", command=functools.partial(submit_NbRouteurs,tab_entry))
	submit_button.pack()
	
	name="R"
	with open('exemple.json', 'r') as f:
		js = json.load(f)
		x=len(js['data'])
		x=x+1
		name=name+str(x)
		print(name)
		
		#with open("ospf.json", "w") as outfile:
	    	#	json.dumps(ospf, outfile)
	    		
		
		#ospf_object = json.dumps(ospf)
		#tab = [ospf_object]
		# Data to be written
		data= {
		    "name": name,
		    "role": "R",
		    "ospf": {"process":str(x), "area":"0" , "router-id": "1.1.1.1"},
		    "X":-2,
		    "Y":-2,
		    "interfaces": [{"name": "Loopback1", "ipv4": "1.1.1.1 255.255.255.255","neighbor":"No"}]
		
		}
		
		#js['data'][x-1].append({"process":str(x), "area":"0" , "router-id": "1.1.1.1"})
		# Serializing json
		json_object = json.dumps(data, indent=4)
	       # Writing in json
	with open('exemple.json', 'w') as f1:
		f1.write(json_object)
    

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

def window2():
        
    back_button = tk.Button(root, text="Précédent", command=back1)
    back_button.pack()
    
    
# Création de la fenêtre principale
root = tk.Tk()
"""with open('exemple.json', 'w') as f1:
	ex={
		"data":[]
	}
	# Serializing json
	json_object = json.dumps(ex)
	# Writing in json
	f1.write(json_object)"""
root.title("Formulaire de commande de routeurs")
root.geometry("600x300")
window1()


# Affichage de la fenêtre
root.mainloop() 
