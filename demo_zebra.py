from os import sep, system
from helpers import read_kaldi_folder_structure
from zebra import PriorLogOddsPlots, zebra_framework, export_zebra_framework_plots


__author__ = "Andreas Nautsch"
__email__ = "nautsch@eurecom.fr"
__coauthor__ = ["Jose Patino", "Natalia Tomashenko", "Junichi Yamagishi", "Paul-Gauthier Noé", "Jean-François Bonastre", "Massimiliano Todisco", "Nicholas Evans"]
__credits__ = ["Niko Brummer", "Daniel Ramos", "Edward de Villiers", "Anthony Larcher"]
__license__ = "LGPLv3"


# This is the object which handles the zero-evidence assessment
# It allows to assess one system at a time - when loading new scores, the old ones are forgotten
# Yet, it never forgets already plotted performance profiles :D
# Of course, we can re-initialize it, so we make it forget previously plotted profiles ;-)
zebra_plot = PriorLogOddsPlots()

# Folder structure of experiments
scr_files = read_kaldi_folder_structure(glob_cmd='exp' + sep + '*' + sep + '*' + sep + '*' + sep + '*test*' + sep + 'scores')

# To compare __multiple__ systems in __one__ condition (specific)
# 1. select scores and key
scr = 'exp/Baseline/primary/results-2020-05-10-14-29-38/ASV-libri_test_enrolls-libri_test_trials_f/scores'
key = 'keys-voiceprivacy-2020/libri_test_trials_f'

# 2. run the framework
zebra_framework(plo_plot=zebra_plot, scr_path=scr, key_path=key)

# 3. saving the plots
filename = 'ZEBRA-plots' + sep + 'example'
export_zebra_framework_plots(plo_plot=zebra_plot, filename=filename, save_plot_ext='png')
export_zebra_framework_plots(plo_plot=zebra_plot, filename=filename, save_plot_ext='pdf')
export_zebra_framework_plots(plo_plot=zebra_plot, filename=filename, save_plot_ext='tex')

system("cd ZEBRA-plots && pdflatex ZEBRA-example_standalone && rm ZEBRA-example_standalone.aux ZEBRA-example_standalone.log")
