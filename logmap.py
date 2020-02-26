import numpy as np
import matplotlib.pyplot as plt

def solve(r, n_vals = 20, steps = 100):
	f = lambda x, r: r*x*(1-x)
	x0 = 0.001
	res = [x0]
	for i in range(steps):
		res.append(f(res[-1], r))

	uniques = list(set(res[-n_vals:]))
	x_list = [r for _ in range(len(uniques))]
	return(x_list, uniques)


r_range = np.linspace(2, 4, 100000)

x_plot=[]
y_plot=[]
for r in r_range:
	x_res, y_res = solve(r, n_vals=100, steps = 1000)
	x_plot+=x_res
	y_plot+=y_res

plt.scatter(x_plot, y_plot, s = 0.1)
plt.xlabel('r')
plt.ylabel('Response')
plt.show()