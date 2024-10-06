import numpy as np
import get_mu_sigma
import yfinance as yf

# Konstante definieren
r = 0.053

# Payoff definieren (z.B. für Call oder Put)
def payoff(S, K):

    return max(K-S, 0)

# rekursives Berechnen der Snell-Umhüllenden
def snell(ups, downs, K, delta_t):
    
    # Aktienpreis für eine gegebene Anzahl ups und downs
    S = S_0*u**ups*d**downs

    # ist man in der letzten Schicht des Modells angekommen, ist snell = payoff
    if (ups + downs) == step_amount:
        return payoff(S, K)
    
    # ist man noch nicht bei der letzten Schicht angekommen, wird snell rekursiv berechnet
    elif (ups + downs) < step_amount:
        expected_snell = pi*snell(ups + 1, downs, K, delta_t) + (1 - pi)*snell(ups, downs + 1, K, delta_t)
        return max(payoff(S, K), np.exp(-r*delta_t)*expected_snell)

def american_option_price(ticker, t_days, K, T):

    # Variablen globalisieren
    global step_amount
    global pi, u, d
    global S_0

    step_amount = T 
    time_to_maturity = t_days/365

    # Aktuellen Preis der Aktie holen
    stock = yf.Ticker(ticker)
    S_0 = stock.info["currentPrice"]

    # mu und sigma holen
    (mu, sigma) = get_mu_sigma.yearly_mu_sigma(ticker)

    # u und d berechnen
    u = np.exp(mu*time_to_maturity/step_amount + sigma*np.sqrt(time_to_maturity/step_amount))
    d = np.exp(mu*time_to_maturity/step_amount - sigma*np.sqrt(time_to_maturity/step_amount))

    # pi berechnen
    pi = (np.exp(r*time_to_maturity/step_amount) - d)/(u - d)

    return snell(0, 0, K, time_to_maturity/step_amount)
