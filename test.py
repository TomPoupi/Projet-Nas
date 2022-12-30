import tkinter as tk
import json
import functools

def submit_NbRouteurs(tab):
    
    if tab[0].get() == '' or tab[1].get() == '' or tab[2].get() == '' or tab[3].get() == '':
        window1()
        
    else :
        num_pe_routers = int(tab[3].get())
        num_ce_routers = int(tab[1].get())
        num_c_routers = int(tab[0].get())
        num_p_routers = int(tab[2].get())

        # Ouvrir le fichier en mode écriture
        with open('network.json', 'w') as f:
            # Écrire les données dans le fichier sous forme de dictionnaire
            data = {
                'nombre de routeurs PE': num_pe_routers,
                'nombre de routeurs CE': num_ce_routers,
                'nombre de routeurs C': num_c_routers,
                'nombre de routeurs P': num_p_routers
            }
            json.dump(data, f)

        print(f'Vous avez indiqué vouloir {num_pe_routers} routeurs PE, {num_ce_routers} routeurs CE, {num_c_routers} routeurs C, et {num_p_routers} routeurs P.')
        print(f'Les données ont été enregistrées dans le fichier "network.json".')
        
        # Effacement du contenu de la fenêtre
        for widget in root.winfo_children():
            widget.destroy()

        tab = [num_c_routers, num_ce_routers, num_p_routers, num_pe_routers]
        # Ajout d'un nouveau label pour demander à l'utilisateur comment les routeurs sont reliés entre eux
        window2(tab)

def window1():
    
    # Création d'un frame pour contenir la première ligne du formulaire
    first_row_frame = tk.Frame(root)
    first_row_frame.pack(pady=10)

    # Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
    num_pe_routers_label = tk.Label(first_row_frame, text="Indiquez le nombre de routeurs PE que vous souhaitez :")
    num_pe_routers_label.pack()

    # Création d'une zone de saisie pour que l'utilisateur puisse entrer son nombre de routeurs PE
    num_pe_routers_entry = tk.Entry(first_row_frame)
    num_pe_routers_entry.pack()

    # Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
    num_ce_routers_label = tk.Label(root, text="Indiquez le nombre de routeurs CE que vous souhaitez :")
    num_ce_routers_label.pack()

    # Création d'une zone de saisie pour que l'utilisateur puisse entrer son nombre de routeurs CE
    num_ce_routers_entry = tk.Entry(root)
    num_ce_routers_entry.pack()

    # Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
    num_c_routers_label = tk.Label(root, text="Indiquez le nombre de routeurs C que vous souhaitez :")
    num_c_routers_label.pack()

    # Création d'une zone de saisie pour que l'utilisateur puisse entrer son nombre de routeurs C
    num_c_routers_entry = tk.Entry(root)
    num_c_routers_entry.pack()

    # Création d'un label pour indiquer à l'utilisateur ce qu'il doit faire
    num_p_routers_label = tk.Label(root, text="Indiquez le nombre de routeurs P que vous souhaitez :")
    num_p_routers_label.pack()

    # Création d'une zone de saisie pour que l'utilisateur puisse entrer son nombre de routeurs P
    num_p_routers_entry = tk.Entry(root)
    num_p_routers_entry.pack()

    tab_entry = [num_c_routers_entry, num_ce_routers_entry, num_p_routers_entry, num_pe_routers_entry]
    
    # Création d'un bouton de soumission
    submit_button = tk.Button(root, text="Soumettre", command=functools.partial(submit_NbRouteurs,tab_entry))
    submit_button.pack()

    # On essaye de rendre ça un peu plus joli (c'est relatif)
    num_pe_routers_entry.pack_configure(padx=10, pady=5)
    num_ce_routers_entry.pack_configure(padx=10, pady=5)
    num_c_routers_entry.pack_configure(padx=10, pady=5)
    num_p_routers_entry.pack_configure(padx=10, pady=5)
    num_pe_routers_label.pack_configure(padx=10, pady=5)
    num_ce_routers_label.pack_configure(padx=10, pady=5)
    num_c_routers_label.pack_configure(padx=10, pady=5)
    num_p_routers_label.pack_configure(padx=10, pady=5)
    submit_button.pack_configure(padx=10, pady=5)

def back1():
    
    for widget in root.winfo_children():
        widget.destroy()
        
    # On retourne à la première fenêtre
    window1()

def window2(tab):
    
    #on demande les voisins de chaque routeur C
    for i in range(1, tab[0]+1):
        voisinCrouter = tk.Label(root, text=f"routeur C{i}")
        voisinCrouter.pack_configure(padx=10, pady=5)
        
    back_button = tk.Button(root, text="Précédent", command=back1)
    back_button.pack()
    
    
# Création de la fenêtre principale
root = tk.Tk()
root.title("Formulaire de commande de routeurs")
root.geometry("600x300")

window1()


# Affichage de la fenêtre
root.mainloop()

