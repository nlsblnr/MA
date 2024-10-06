import yfinance as yf
import numpy as np
from get_mu_sigma import yearly_mu_sigma
from math import comb

def euro_bin_price(ticker, time_to_maturity_days, exercise_price, step_amount):

    # Zinssatz einer U.S. Treasury Bill (3 Monate) am 5.4.24 =: risikofreier Zins
    r = 0.05351

    # Rechne Tage in Jahre um
    time_to_maturity_years = time_to_maturity_days/365

    # Hole aktuellen Preis S_0
    stock = yf.Ticker(ticker)
    S_0 = stock.info["currentPrice"]

    # Hole erwartete jährliche Rendite mu und Volatilität sigma
    (mu, sigma) = yearly_mu_sigma(ticker)

    # Berechne u und d
    u = np.exp(mu*(time_to_maturity_years/step_amount) + sigma*np.sqrt(time_to_maturity_years/step_amount))
    d = np.exp(mu*(time_to_maturity_years/step_amount) - sigma*np.sqrt(time_to_maturity_years/step_amount))

    # Berechne die Martingal-Up-Tick-Wahrscheinlichkeit
    pi = (np.exp(r*time_to_maturity_years/step_amount) - d)/(u - d)

    # Berechne Summe für die Berechnung des Call-Optionspreises
    sum1 = 0
    for k in range(0, step_amount+1):
        sum1 += comb(step_amount, k)*max((S_0*u**k*d**(step_amount - k) - exercise_price), 0)*pi**k*(1 - pi)**(step_amount - k)
    
    # Berechne Call-Optionspreis C_0
    C_0 = np.exp(-r*time_to_maturity_years)*sum1

    # Berechne Put-Optionspreis P_0 mithilfe Put-Call-Parität
    P_0 = C_0 + exercise_price*np.exp(-r*time_to_maturity_years) - S_0

    return (C_0, P_0)