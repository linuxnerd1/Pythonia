#Benötigte Module 

import tkinter as tk
import random


# Vokabelliste

Vokabeln = [
    ("Hello", "Hallo"),
    ("House", "Haus"),
    ("Cat", "Katze"),
]


# Mischen der Vokabeln

random.shuffle(Vokabeln)		


# Fenster

fenster = tk.Tk()
fenster.title("Vokabel-Quiz")
fenster.geometry("1000x1200")
fenster.config(bg="#00838F")

# Label für die Frage

lbl_frage = tk.Label(fenster, text="", bg="#E3F2FD", font=("Arial", 100))
lbl_frage.pack(pady=20)


# Label für die Lösung

lbl_loesung = tk.Label(fenster, text="",bg="#E3F2FD", font=("Arial", 100))
lbl_loesung.pack(pady=20)

aktuelle_karte = None


#Funktion die eine neue Vokabel ausgibt 

def neue_vokabel():
    global aktuelle_karte
    if not Vokabeln:
        aktuelle_karte = None
    else:
        aktuelle_karte = Vokabeln[0]


#Funktion der nächsten Karte (von karte_richtig aufgerufen)
        
def naechste_karte():
    neue_vokabel()

    if aktuelle_karte is None:
        lbl_frage.config(text="Fertig!")
        lbl_loesung.config(text="")
        return

    frage, _ = aktuelle_karte
    lbl_frage.config(text=frage)
    lbl_loesung.config(text="")


#Funktion der Ausgabe der Lösung
    
def loesung_zeigen():
    if aktuelle_karte is None:
        return
    _, antwort = aktuelle_karte
    lbl_loesung.config(text=antwort)


#Funktion (karte_falsch) falsche Karten werden wiederholt
    
def karte_falsch():
    if not Vokabeln:
        return
    Vokabeln.append(Vokabeln.pop(0))
    naechste_karte()


#Funktion karte_richtig (wird nicht mehr wiederholt)
    
def karte_richtig():
    if not Vokabeln:
        return
    Vokabeln.pop(0)
    naechste_karte()


#Funktion zum schließen
    
def fenster_schließen():
    fenster.destroy()
        
           
# Kontrollelemente definieren 

btn_loesung = tk.Button(fenster, text="Lösung", font=("Arial", 20), bg="#E3F2FD", command=loesung_zeigen)
btn_richtig = tk.Button(fenster, text="Richtig", font=("Arial",20), bg="#E3F2FD", command=karte_richtig)
btn_falsch = tk.Button(fenster, text="Falsch", font=("Arial", 20), bg="#E3F2FD", command=karte_falsch)
btn_fensterschließen = tk.Button(fenster, text="Beenden", font=("Arial", 20), bg="#E3F2FD", command =fenster_schließen)


#Kontrollelemente aufrufen

btn_loesung.pack()
btn_richtig.pack()
btn_falsch.pack()
btn_fensterschließen.pack()


# Start

naechste_karte()
fenster.mainloop()
