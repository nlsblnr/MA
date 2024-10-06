import yfinance as yf
import numpy as np
from datetime import date, timedelta

def yearly_mu_sigma(ticker):
    # Zeitraum berechnet ist 1 Tag, ich will aber mu und sigma für 1 Jahr
    T_0 = 1
    T_1 = 365

    # Bestimmt heutiges Datum und Datum vor 365 Tagen für historischen Kursabruf
    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    # Abrufen der historischen Kursdaten von Yahoo Finance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Berechnung der täglichen Renditen
    stock_data['Returns'] = stock_data['Adj Close'].pct_change()
    
    # Entfernen von NaN-Werten
    pct_returns = stock_data['Returns'].dropna()
    
    # Konvertierung in logarithmische Rendite
    log_returns = []
    for pct_return in pct_returns:
        log_returns.append(np.log(pct_return+1))
    
    # Berechnung des Erwartungswerts und der Standardabweichung
    mean_return_day = np.mean(log_returns)
    std_dev_return_day = np.std(log_returns)

    # Erwartungswert und Standardabweichung auf die gegebene Zeitdauer (1 Jahr) hochrechnen
    mu = (T_1/T_0)*mean_return_day
    sigma = std_dev_return_day*np.sqrt(T_1/T_0)

    return(mu, sigma)