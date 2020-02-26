import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D





import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


def updateFig(data):
	newx, newy, newz = data



xi, yi , zi = 1, 1, 1

sigma = 10
beta = 8/3.
rho = 28
h = 0.001
maxiter = 50

dxdt = lambda x, y, z : sigma*(y-x)
dydt = lambda x, y, z : x*(rho-z)-y
dzdt = lambda x, y, z : x*y - beta*z

x_plot = [xi]
y_plot = [yi]
z_plot = [zi]

for _ in range(0, int(maxiter/h)):
	k1x = dxdt(xi, yi, zi)
	k1y = dydt(xi, yi, zi)
	k1z = dzdt(xi, yi, zi)

	k2x = dxdt(xi+k1x*h/2, yi+k1y*h/2, zi+k1z*h/2)
	k2y = dydt(xi+k1x*h/2, yi+k1y*h/2, zi+k1z*h/2)
	k2z = dzdt(xi+k1x*h/2, yi+k1y*h/2, zi+k1z*h/2)

	k3x = dxdt(xi+k2x*h/2, yi+k2y*h/2, zi+k2z*h/2)
	k3y = dydt(xi+k2x*h/2, yi+k2y*h/2, zi+k2z*h/2)
	k3z = dzdt(xi+k2x*h/2, yi+k2y*h/2, zi+k2z*h/2)

	k4x = dxdt(xi+k3x*h, yi+k3y*h, zi+k3z*h)
	k4y = dydt(xi+k3x*h, yi+k3y*h, zi+k3z*h)
	k4z = dzdt(xi+k3x*h, yi+k3y*h, zi+k3z*h)

	xi += h*(k1x+2*k2x+2*k3x+k4x)/6
	yi += h*(k1y+2*k2y+2*k3y+k4y)/6
	zi += h*(k1z+2*k2z+2*k3z+k4z)/6

	x_plot.append(xi)
	y_plot.append(yi)
	z_plot.append(zi)

fig = plt.figure(figsize = (5,5))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_plot, y_plot, z_plot)
plt.show()
