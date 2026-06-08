import numpy as np
from scipy import stats

total_time = 1
steps = 365
delta_t = total_time/steps
sigma_brownian_motion = 1
mu = 0
S_0 = 100
r = 0.042
sigma_volatility = 0.20
K = 100

option_prices = []
averages = []

simulated_prices = []

for i in range(500):

    # Zeige alle 200 Durchgänge den Stand an
    if i%200==0:
        print(i)

    times = []
    stock_price = []
    W = []
    time_now = 0

    for x in range(steps + 1):
        times.append(time_now)
        
        if x == 0:
            stock_price.append(S_0)
            W.append(0)
        else:
            W_t = np.random.normal(loc=0, scale=sigma_brownian_motion*np.sqrt(delta_t))
            W.append(W[x-1] + W_t)
            stock_price.append(S_0*np.exp((r-sigma_volatility**2/2)*time_now + sigma_volatility*np.sqrt(time_now)*W[x]))

        time_now += delta_t
    
    final_price = stock_price[len(stock_price)-1]
    simulated_prices.append(final_price)
    option_prices.append(np.exp(-r*total_time)*max(final_price-K, 0))
    averages.append(np.average(option_prices))

print("Simulated stock prices:")
for i in simulated_prices:
    print(i)
print("\nOption prices:")
for i in option_prices:
    print(i)

print("\nAVERAGE:", np.average(option_prices))

'''
d_1 = 1/(sigma_volatility*np.sqrt(total_time))*(np.log(S_0/K) + total_time*(r + sigma_volatility**2/2))
d_2 = d_1 - sigma_volatility*np.sqrt(total_time)
black_scholes_price = S_0*stats.norm.cdf(d_1) - K*np.exp(-r*total_time)*stats.norm.cdf(d_2)
print("Black-Scholes:", black_scholes_price)

# Ausgeben der Daten
print("\n")
for ix, average in enumerate(averages):
    if ix%10==0:
        print(ix)
for ix, average in enumerate(averages):
    if ix%10==0:
        print(average)
'''