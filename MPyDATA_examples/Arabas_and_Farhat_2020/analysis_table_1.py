from MPyDATA_examples.Arabas_and_Farhat_2020.simulation import Simulation
from MPyDATA_examples.Arabas_and_Farhat_2020.setup2_american_put import Setup
from MPyDATA_examples.Arabas_and_Farhat_2020.analysis_figures_2_and_3 import error_L2_norm
import numpy as np
from joblib import Parallel, delayed, parallel_backend


def compute_row(simulations):
    S0 = simulations[0].setup.S0
    T = simulations[0].setup.T
    for i in range(1, len(simulations)):
        assert simulations[i].setup.T == T
        assert simulations[i].setup.S0 == S0
    row = [simulations[0].setup.T, simulations[0].setup.S0]
    for simulation in simulations:
        f = simulation.run(n_iters=2)
        row.append(
            error_L2_norm(simulation.solvers, simulation.setup, simulation.S, simulation.nt, n_iters=2))
        np.testing.assert_almost_equal(simulation.S[simulation.ix_match], S0)
    row.append(f[simulations[0].ix_match])
    row.append(simulations[0].setup.analytical_solution(S0))
    row.append(simulations[0].setup.analytical_solution(S0, amer=False))
    return row


def table_1_data():
    with parallel_backend('threading', n_jobs=1):
        result = Parallel(verbose=10)(
            delayed(compute_row)(tuple(
                Simulation(Setup(T=T, C_opt=C_opt, S0=S0))
                for C_opt in (.02, .01, .005)
            ))
            for T in (.25, .5, 3)
            for S0 in (80, 90, 100, 110, 120)
        )
        return result

