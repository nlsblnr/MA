import yfinance as yf
import numpy as np
from get_mu_sigma import yearly_mu_sigma
from scipy import stats

# Zinssatz einer U.S. Treasury Bill (3 Monate) am 5.4.24 =: risikofreier Zins
r = 0.05351

def european_BS_price(ticker, time_to_maturity_days, exercise_price):

    # Rechne Tage in Jahre um
    time_to_maturity_years = time_to_maturity_days/365

    # Hole aktuellen Preis S_0
    stock = yf.Ticker(ticker)
    S_0 = stock.info["currentPrice"]

    # Hole erwartete jährliche Rendite mu und Volatilität sigma
    (mu, sigma) = yearly_mu_sigma(ticker)

    # d_1 und d_2 berechnen
    d_1 = 1/(sigma*np.sqrt(time_to_maturity_years))*(np.log(S_0/exercise_price) + time_to_maturity_years*(r + sigma**2/2))
    d_2 = d_1 - sigma*np.sqrt(time_to_maturity_years)

    # Call-Optionspreis C_0 berechnen
    C_0 = float(S_0*stats.norm.cdf(d_1) - np.exp(-r*time_to_maturity_years)*exercise_price*stats.norm.cdf(d_2))

    # Put-Optionspreis P_0 berechnen
    P_0 = float(-S_0*stats.norm.cdf(-d_1) + np.exp(-r*time_to_maturity_years)*exercise_price*stats.norm.cdf(-d_2))

    return (C_0, P_0)