import numpy as np
import matplotlib.pyplot as plt

d = 1 #AA
l0 = 2 #AA

gamma_list = np.linspace(0,1)

def lhs(gamma):
    return np.array([ max(g, 6.0 * (1.0 - g)) for g in gamma])

def rhs(d, l0):
    return 6.5 * (d/l0)**2

plt.plot( gamma_list, lhs(gamma_list), color="r" )
plt.axhline( rhs(d, l0), color="b" )
plt.xlabel(r"$\gamma$")
plt.savefig("stability_criterion.png", dpi=300)


l0_list    = np.linspace(0,1)
plt.contourf( gamma_list, l0_list, lhs(gamma_list) - rhs(d,l0_list) )
plt.savefig("stability_criterion2.png", dpi=300)
