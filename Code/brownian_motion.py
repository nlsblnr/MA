import numpy as np

total_time = 1
steps = 365
delta_t = total_time/steps
sigma = 1
mu = 0

times = []
brownian_motion = []
W = []

time_now = 0

for x in range(steps + 1):
    times.append(time_now)
    
    if x == 0:
        brownian_motion.append(0)
        W.append(0)
    else:
        W_t = np.random.normal(loc=0, scale=sigma*np.sqrt(delta_t))
        W.append(W[x-1] + W_t)
        brownian_motion.append(mu*time_now + W[x])

    time_now += delta_t

for a in times:
    print(a)
print("\n")
for b in brownian_motion:
    print(b)