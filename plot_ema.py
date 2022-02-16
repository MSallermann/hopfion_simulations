import numpy as np
import matplotlib.pyplot as plt


for i,K in enumerate([0, 0.01, 0.02, 0.03, 0.04, 0.05]):
    evals = np.loadtxt(f"eigenmodes_min_{K}.ovf", skiprows=40, max_rows = 20, comments = "#")
    print(evals)

    in_magnon_continuum = evals > 2*K

    idx = np.array(range(len(evals)))

    plt.plot(idx[in_magnon_continuum], evals[in_magnon_continuum], alpha=1, label=f"K = {K} meV", marker=".", color=f"C{i}")

    plt.plot( [idx[~in_magnon_continuum][-1] , idx[in_magnon_continuum][0]],  [evals[~in_magnon_continuum][-1] , evals[in_magnon_continuum][0]] )

    plt.plot(idx[~in_magnon_continuum], evals[~in_magnon_continuum], marker="o", color=f"C{i}")

    plt.axhline(2*K, color=f"C{i}", ls="--")

    K_list = 2*K*np.ones(len(evals))
    print(K_list)

    max_eval_list =  np.max(evals) * np.ones(len(evals))
    print(max_eval_list)

    # plt.fill_between( range(len(evals)), [min(e,2*K) for e in evals], evals , alpha=1)


import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

ax = plt.gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.ylabel("Eigenvalue [meV]")
plt.xlabel("Eigenvalue #")
plt.legend()
plt.savefig("evals.png", dpi=300)



plt.close()
K_list = []
eval_data = []

for i,K in enumerate([0, 0.01, 0.02, 0.03, 0.04, 0.05]):
    K_list.append(K)
    evals = np.loadtxt(f"eigenmodes_min_{K}.ovf", skiprows=40, max_rows = 20, comments = "#")
    eval_data.append(evals)

    # plt.plot(evals, label=f"K = {K} meV", marker=".", color=f"C{i}")
    # plt.axhline(2*K, color=f"C{i}")

K_list = np.array(K_list)

eval_data = np.transpose(eval_data)

for ev in eval_data:
    plt.plot(K_list, ev, marker=".")


plt.fill_between(K_list, 2*K_list, np.max(eval_data), alpha=0.2)

# plt.plot(K_list, 2*K_list, color="b", ls="--")
plt.ylabel("Eigenvalue [meV]")
plt.xlabel("K [meV]")
plt.legend()
plt.savefig("k_vs_evals.png", dpi=300)