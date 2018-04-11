"""
plot 2d wham pmf and prob
"""

from _plots import plot_heatmap_imshow
from _wham import load_2d_pmf_prob

wham_pmf_file = "pmf.dat"
nxbins = 25
nybins = 40
x, y, pmf, prob = load_2d_pmf_prob(wham_pmf_file, nxbins, nybins)

left = x[0]
right = x[-1]
bottom = y[0]
top = y[-1]
print(left, right, bottom, top)

xlabel = "nmp core angle (deg)"
ylabel = "lid core angle (deg)"
zlabel = "PMF (kcal/mol)"
out = "pmf.pdf"

plot_heatmap_imshow(pmf[::-1,:], left, right, bottom, top,
                        xlabel, ylabel, zlabel, out,
                    nticks=8, 
                    figure_size=(6.4, 4.8) )

zlabel = "Probability"
out = "prob.pdf"
plot_heatmap_imshow(prob[::-1,:], left, right, bottom, top,
                        xlabel, ylabel, zlabel, out,
                    nticks=8,
                    figure_size=(6.4, 4.8))
