import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from european_BS_pricing import *
from binomial_pricing import *
import american_options_pricing as am

# Definiere Payoff-Funktionen für Call- und Put-Optionen
def payoff_call(S, K):
    return max(S - K, 0)
def payoff_put(S, K):
    return max(K - S, 0)

def submit_values():

    # Hole die Info, ob es sich um Call oder Put bzw. BS, euro (Bin) oder amerikanisch handelt
    # Zeige Fehler an, wenn eine nötige Angabe nicht gemacht wurde
    try:
        selected_option_method = option_method_var.get()
        selected_option_type = option_type_var.get()
    except:
        messagebox.showerror(title="Fehler", message="Es fehlen nötige Angaben.")

    # Daten aus Eingabefeldern entnehmen
    # Zeige Fehler an, wenn eine nötige Angabe fehlt oder wenn ein unbrauchbarer Wert eingegeben wurde
    try:
        ticker = str(ticker_entry.get())
        exercise_price = float(exercise_price_entry.get())
        time_to_maturity_days = float(time_to_maturity_entry.get())
        if selected_option_method in ("Binomial", "American"):
            steps = int(steps_entry.get())
    except:
        messagebox.showerror(title="Fehler", message="Überprüfe die Eingaben noch einmal!")

    # Berechne den gewünschten Preis
    if selected_option_method == "BS" and selected_option_type == "Call":
        show(european_BS_price(ticker, time_to_maturity_days, exercise_price)[0], "Europäisch (Black-Scholes)", "Call")
    elif selected_option_method == "Binomial" and selected_option_type == "Call":
        show(euro_bin_price(ticker, time_to_maturity_days, exercise_price, steps)[0], "Europäisch (Binomialmodell)", "Call")
    elif selected_option_method == "American" and selected_option_type == "Call":
        am.payoff = payoff_call
        show(am.american_option_price(ticker, time_to_maturity_days, exercise_price, steps), "Amerikanisch", "Call")
    elif selected_option_method == "BS" and selected_option_type == "Put":
        show(european_BS_price(ticker, time_to_maturity_days, exercise_price)[1], "Europäisch (Black-Scholes)", "Call")
    elif selected_option_method == "Binomial" and selected_option_type == "Put":
        show(euro_bin_price(ticker, time_to_maturity_days, exercise_price, steps)[1], "Europäisch (Binomialmodell)", "Put")
    elif selected_option_method == "American" and selected_option_type == "Put":
        am.payoff = payoff_put
        show(am.american_option_price(ticker, time_to_maturity_days, exercise_price, steps), "Amerikanisch", "Put")

# Generiere eine Infobox mit dem Resultat
def show(calculated_price, option_method, option_type):
    messagebox.showinfo(title="Resultat", message=(option_type + "-Optionspreis " + option_method + ": $" + str(round(calculated_price, 2))))

# Programmfenster erstellen
wn = Tk()
wn.title("Optionspreisrechner")
wn.geometry("300x450")

# Eingabeknopf für Berechnungsmethode
option_method_var = tk.StringVar(value="")
option_method_lbl = Label(wn, text="Berechnungsmethode:").pack()
ttk.Radiobutton(wn, text="Europäisch (Black-Scholes)", variable=option_method_var, value="BS").pack()
ttk.Radiobutton(wn, text="Europäisch (Binomialmodell)", variable=option_method_var, value="Binomial").pack()
ttk.Radiobutton(wn, text="Amerikanisch", variable=option_method_var, value="American").pack()

# vertikaler Abstand
br0 = Label(wn, text="\n").pack()

# Eingabeknopf für Optionstyp
option_type_var = tk.StringVar(value="")
option_type_lbl = Label(wn, text="Optionstyp:").pack()
ttk.Radiobutton(wn, text="Call", variable=option_type_var, value="Call").pack()
ttk.Radiobutton(wn, text="Put", variable=option_type_var, value="Put").pack()

# vertikaler Abstand
br1 = Label(wn, text="\n").pack()

#Eingabefelder und -beschriftungen generieren
ticker_entry_lbl = Label(wn, text="Aktiensymbol:").pack()
ticker_entry = Entry(wn)
ticker_entry.pack()

exercise_price_entry_lbl = Label(wn, text="Ausübungspreis:").pack()
exercise_price_entry = Entry(wn)
exercise_price_entry.pack()

time_to_maturity_entry_lbl = Label(wn, text="Laufzeit in Tagen:").pack()
time_to_maturity_entry = Entry(wn)
time_to_maturity_entry.pack()

steps_entry_lbl = Label(wn, text="Anzahl Schritte für Binomialmodell:").pack()
steps_entry = Entry(wn)
steps_entry.pack()

# vertikaler Abstand
br2 = Label(wn, text="\n").pack()

# Knopf für Einreichen der Daten
submit_data_btn = Button(wn, text="BERECHNEN", command=submit_values)
submit_data_btn.pack()

wn.mainloop()