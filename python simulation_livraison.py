import tkinter as tk
from tkinter import messagebox, simpledialog
from abc import ABC, abstractmethod

# ----- CLASSES POO -----

class Vehicule(ABC):
    def __init__(self, marque, modele, immatriculation):
        self._marque = marque
        self._modele = modele
        self._immatriculation = immatriculation

    @abstractmethod
    def livrer(self, commande):
        pass

    def __str__(self):
        return f"{self._marque} {self._modele} ({self._immatriculation})"

class Camion(Vehicule):
    def __init__(self, marque, modele, immatriculation, capacite):
        super().__init__(marque, modele, immatriculation)
        self.capacite = capacite

    def livrer(self, commande):
        if commande.poids <= self.capacite:
            commande.marquer_livree()
            return f"Commande {commande.id} livrée par camion."
        return "Poids trop élevé pour le camion."

class Moto(Vehicule):
    def __init__(self, marque, modele, immatriculation, vitesse_max):
        super().__init__(marque, modele, immatriculation)
        self.vitesse_max = vitesse_max

    def livrer(self, commande):
        if commande.poids <= 10:
            commande.marquer_livree()
            return f"Commande {commande.id} livrée par moto."
        return "Poids trop élevé pour la moto."

class Commande:
    def __init__(self, id, destination, poids):
        self.id = id
        self.destination = destination
        self.poids = poids
        self.statut = "en attente"

    def marquer_livree(self):
        self.statut = "livrée"

    @staticmethod
    def valider_poids(poids):
        return 0 < poids <= 100

    def __str__(self):
        return f"Commande {self.id} -> {self.destination}, {self.poids}kg, {self.statut}"

class Livreur:
    def __init__(self, nom, vehicule=None):
        self.nom = nom
        self.vehicule = vehicule
        self.commandes_en_cours = []

    def ajouter_commande(self, commande):
        self.commandes_en_cours.append(commande)

    def effectuer_livraison(self):
        resultats = []
        for c in self.commandes_en_cours:
            resultat = self.vehicule.livrer(c)
            resultats.append(resultat)
        self.commandes_en_cours = []
        return resultats

    @staticmethod
    def verifier_nom(nom):
        return nom.isalpha()

    @classmethod
    def depuis_dictionnaire(cls, data):
        return cls(data["nom"])
    
    def __str__(self):
        return f"Livreur {self.nom} avec {self.vehicule}"

class Depot:
    def __init__(self):
        self.vehicules_disponibles = []
        self.livreurs_disponibles = []

    def ajouter_vehicule(self, vehicule):
        self.vehicules_disponibles.append(vehicule)

    def ajouter_livreur(self, livreur):
        self.livreurs_disponibles.append(livreur)

    def attribuer_vehicule(self, livreur, vehicule):
        livreur.vehicule = vehicule
        if vehicule in self.vehicules_disponibles:
            self.vehicules_disponibles.remove(vehicule)

    def afficher_etat(self):
        print("---- Véhicules ----")
        for v in self.vehicules_disponibles:
            print(v)
        print("---- Livreurs ----")
        for l in self.livreurs_disponibles:
            print(l)

# ----- INTERFACE TKINTER -----

class AppLivraison:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation de Livraison")

        self.depot = Depot()
        self.commandes = []

        # Listes
        self.vehicules_listbox = tk.Listbox(root)
        self.vehicules_listbox.pack()

        self.livreurs_listbox = tk.Listbox(root)
        self.livreurs_listbox.pack()

        # Boutons
        tk.Button(root, text="Ajouter Véhicule", command=self.ajouter_vehicule).pack()
        tk.Button(root, text="Ajouter Livreur", command=self.ajouter_livreur).pack()
        tk.Button(root, text="Créer Commande", command=self.creer_commande).pack()
        tk.Button(root, text="Attribuer Véhicule", command=self.attribuer_vehicule).pack()
        tk.Button(root, text="Effectuer Livraison", command=self.effectuer_livraison).pack()

    def ajouter_vehicule(self):
        type_vehicule = simpledialog.askstring("Type", "Camion ou Moto ?")
        marque = simpledialog.askstring("Marque", "Entrer la marque :")
        modele = simpledialog.askstring("Modèle", "Entrer le modèle :")
        immat = simpledialog.askstring("Immatriculation", "Entrer l'immatriculation :")

        if type_vehicule and type_vehicule.lower() == "camion":
            capacite = float(simpledialog.askstring("Capacité", "Capacité (tonnes) :"))
            v = Camion(marque, modele, immat, capacite)
        else:
            vitesse = float(simpledialog.askstring("Vitesse", "Vitesse max :"))
            v = Moto(marque, modele, immat, vitesse)

        self.depot.ajouter_vehicule(v)
        self.vehicules_listbox.insert(tk.END, str(v))

    def ajouter_livreur(self):
        nom = simpledialog.askstring("Nom", "Nom du livreur :")
        if Livreur.verifier_nom(nom):
            l = Livreur(nom)
            self.depot.ajouter_livreur(l)
            self.livreurs_listbox.insert(tk.END, l.nom)
        else:
            messagebox.showerror("Erreur", "Nom invalide")

    def creer_commande(self):
        id = len(self.commandes) + 1
        destination = simpledialog.askstring("Destination", "Destination :")
        poids = float(simpledialog.askstring("Poids", "Poids de la commande :"))
        if Commande.valider_poids(poids):
            c = Commande(id, destination, poids)
            self.commandes.append(c)
            messagebox.showinfo("Commande", f"Commande {c.id} créée")
        else:
            messagebox.showerror("Erreur", "Poids invalide")

    def attribuer_vehicule(self):
        livreur_index = self.livreurs_listbox.curselection()
        vehicule_index = self.vehicules_listbox.curselection()
        if livreur_index and vehicule_index:
            livreur = self.depot.livreurs_disponibles[livreur_index[0]]
            vehicule = self.depot.vehicules_disponibles[vehicule_index[0]]
            self.depot.attribuer_vehicule(livreur, vehicule)
            messagebox.showinfo("Attribution", f"{vehicule} assigné à {livreur.nom}")
            self.vehicules_listbox.delete(vehicule_index[0])
        else:
            messagebox.showerror("Erreur", "Sélectionnez un livreur et un véhicule")

    def effectuer_livraison(self):
        index = self.livreurs_listbox.curselection()
        if index:
            livreur = self.depot.livreurs_disponibles[index[0]]
            if self.commandes:
                commande = self.commandes.pop(0)
                livreur.ajouter_commande(commande)
                resultats = livreur.effectuer_livraison()
                messagebox.showinfo("Livraison", "\n".join(resultats))
            else:
                messagebox.showwarning("Aucune commande", "Pas de commande à livrer")
        else:
            messagebox.showerror("Erreur", "Sélectionnez un livreur")

# ----- LANCEMENT -----

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLivraison(root)
    root.mainloop()
