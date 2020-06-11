import argparse
from matplotlib.pyplot import show, legend
from zebra import PriorLogOddsPlots, zebra_framework, export_zebra_framework_plots


__author__ = "Andreas Nautsch"
__email__ = "nautsch@eurecom.fr"
__coauthor__ = ["Jose Patino", "Natalia Tomashenko", "Junichi Yamagishi", "Paul-Gauthier Noé", "Jean-François Bonastre", "Massimiliano Todisco", "Nicholas Evans"]
__credits__ = ["Niko Brummer", "Daniel Ramos", "Edward de Villiers", "Anthony Larcher"]
__license__ = "LGPLv3"


parser = argparse.ArgumentParser(description='ZEBRA: Zero Evidence - an assessment framework to privacy for natural signals.')
parser.add_argument('-s', dest='score_file', type=str, nargs=1, required=True, help='path to score file')
parser.add_argument('-k', dest='key_file', type=str, nargs=1, required=True,   help='path to key file')
parser.add_argument('-l', dest='label', type=str, nargs=1, default='ZEBRA profile', help='label of experiment (and export filename); default: "profile"')
parser.add_argument('-p', dest='plots', action='store_true', help='flag: create plots; default: False')
parser.add_argument('-e', dest='ext', type=str, nargs=1, default=None, help='file type (exporting plots; implies [-e]), supported file types: tex, pdf, png; default: None')

args = parser.parse_args()
score_file = args.score_file[0]
key_file = args.key_file[0]
label = args.label
if type(label) is not str:
    label = label[0]

plots = args.plots
if type(plots) is not bool:
    plots = plots[0]

ext = args.ext
if (type(ext) is not str) and (ext is not None):
    ext = ext[0]

flag_ext = ext is not None

zebra_obj = PriorLogOddsPlots()
line_style_min = None
if plots or ext:
    line_style_min = 'b'

zebra_framework(plo_plot=zebra_obj, scr_path=score_file, key_path=key_file, label=label, color_min=line_style_min)

if plots or flag_ext:
    legend(zebra_obj.legend_ECE)

    if flag_ext:
        show(block=False)
        export_zebra_framework_plots(plo_plot=zebra_obj, filename=label, save_plot_ext=ext)

    if plots:
        show()

print('')
