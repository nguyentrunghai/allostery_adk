"""
plot wham 1d pmf and probability
"""

from _plots import plot_lines
from _wham import load_1d_pmf_prob


wham_pmf_file = "pmf.dat"
x, pmf, pmf_err, prob, prob_err = load_1d_pmf_prob(wham_pmf_file)

xlabel = "lid core angle (deg)"
ylabel = "PMF (kcal/mol)"
out = "pmf.pdf"
plot_lines([x], [pmf], yerrs=[pmf_err], xlabel=xlabel, ylabel=ylabel, out=out)


ylabel = "Probability"
out = "prob.pdf"
plot_lines([x], [prob], yerrs=[prob_err], xlabel=xlabel, ylabel=ylabel, out=out)