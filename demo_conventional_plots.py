from matplotlib.pyplot import title, figure, legend, savefig, ylim, xlabel, ylabel
from zebra import PriorLogOddsPlots
from numpy.random import randn
from seaborn import distplot
from numpy import log
from os import sep


__author__ = "Andreas Nautsch"
__email__ = "nautsch@eurecom.fr"
__coauthor__ = ["Jose Patino", "Natalia Tomashenko", "Junichi Yamagishi", "Paul-Gauthier Noé", "Jean-François Bonastre", "Massimiliano Todisco", "Nicholas Evans"]
__credits__ = ["Niko Brummer", "Daniel Ramos", "Edward de Villiers", "Anthony Larcher"]
__license__ = "LGPLv3"


def plot_hist(scrA, scrB, label, fname):
    figure()
    distplot(scrA, color='g', label='class A')
    distplot(scrB, color='r', label='class B')
    legend()
    title(label)
    xlabel('Score value')
    ylim([0, 1])
    ylabel('Relative frequency')
    savefig(fname)


filename = 'prior-log-odds-plots' + sep + 'conventional-plot'

# see bosaris_toolkit/demo/demo_plot_nber.m
# random normal scores, raw scores
classA_scores = 3 + 2 * randn(10**5)
classB_scores = randn(10**5)
plot_hist(classA_scores, classB_scores, 'Histogram: raw scores', 'prior-log-odds-plots/histogram-raw-scores.png')

# LLR-ify
classA_llr = -0.5*(classA_scores-3)**2/(2**2) + 0.5*classA_scores**2 - 0.5*log(2)
classB_llr = -0.5*(classB_scores-3)**2/(2**2) + 0.5*classB_scores**2 - 0.5*log(2)
plot_hist(classA_llr, classB_llr, 'Histogram: LLR scores', 'prior-log-odds-plots/histogram-llr-scores.png')

# plotting
label = 'N(3, 2) vs N(0, 1)'
labels = ['raw scores', 'synthetic LLRs']
profile_styles = [':', '-']

for normalize in [True, False]:
    plo_plot = PriorLogOddsPlots(normalize=normalize)
    scr_idx = 0
    for a, b in [[classA_scores, classB_scores], [classA_llr, classB_llr]]:
        plo_plot.set_system(a, b)

        color_min = None
        if scr_idx == 0:
            color_min = 'k'

        plo_plot.plot_dcf(color_min=color_min, style_min='--', color_act='g', style_act=profile_styles[scr_idx])
        title(label)

        if scr_idx == 0:
            color_min = 'b'

        plo_plot.plot_ece(color_min=color_min, style_min='--', color_act='r', style_act=profile_styles[scr_idx])
        title(label)

        if scr_idx == 0:
            plo_plot.add_legend_entry('min profile')

        plo_plot.add_legend_entry('act profile: ' + labels[scr_idx])
        scr_idx += 1

    plo_plot.show_legend('DCF')
    plo_plot.save(filename, 'DCF')

    plo_plot.show_legend('ECE')
    plo_plot.save(filename, 'ECE')


plo_plot = PriorLogOddsPlots(classA_scores, classB_scores)
plo_plot.plot_dcf(color_min='k', style_min='--', color_act='g', style_act='-', plot_err=True)
plo_plot.add_legend_entry('min profile')
plo_plot.add_legend_entry('act profile')
plo_plot.add_legend_entry('EER (max min DCF): %.1f%%' % (100*plo_plot.eer))
plo_plot.show_legend('DCF')
plo_plot.save(filename + '_eer', 'DCF')
