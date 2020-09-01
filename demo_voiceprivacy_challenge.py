from zebra import PriorLogOddsPlots, zebra_framework, export_zebra_framework_plots, cmap_tab20, categorical_tags, cat_ranges, zebra_plots_sorted_legend
from helpers import read_kaldi_folder_structure, place_legend
from numpy import log, inf, hstack, argwhere
from pandas import DataFrame, read_csv
import matplotlib.pyplot as mpl
from performance import cllr
from functools import partial
from copy import deepcopy
from re import sub
from os import sep


__author__ = "Andreas Nautsch"
__email__ = "nautsch@eurecom.fr"
__coauthor__ = ["Jose Patino", "Natalia Tomashenko", "Junichi Yamagishi", "Paul-Gauthier Noé", "Jean-François Bonastre", "Massimiliano Todisco", "Nicholas Evans"]
__credits__ = ["Niko Brummer", "Daniel Ramos", "Edward de Villiers", "Anthony Larcher"]
__license__ = "LGPLv3"


# read score files
scr_files = read_kaldi_folder_structure(glob_cmd='exp' + sep + '*' + sep + '*' + sep + '*' + sep + '*test*' + sep + 'scores')

# compute metrics: ROCCH-EER, Cllr & min Cllr
challenge_results = DataFrame({
    'System': scr_files.label,
    'Gender': scr_files.gender,
    'Dataset': scr_files.dataset,
    'Task': scr_files.task})
challenge_results['ROCCH-EER [%]'] = 0.0
# challenge_results['Cllr'] = 0.0
# challenge_results['min Cllr'] = 0.0
challenge_results['ZEBRA Population [bit]'] = 1/log(4)
challenge_results['ZEBRA Individual'] = inf
challenge_results['ZEBRA Category'] = 'F'

zebra_plot = PriorLogOddsPlots()
for idx in range(len(scr_files)):
    # load scores
    scr = read_csv(scr_files.scr[idx], sep=' ', header=None).pivot_table(index=0, columns=1, values=2)
    key_path = 'keys-voiceprivacy-2020' + sep + '_'.join((scr_files.dataset[idx], 'test', 'trials', scr_files.gender[idx]))
    if 'a' in scr_files.task[idx]:
        key_path += '_anon'
    key = read_csv(key_path, sep=' ', header=None).replace('nontarget', False).replace('target', True).pivot_table(index=0, columns=1, values=2)
    classA_scores = scr.values[key.values == True]
    classB_scores = scr.values[key.values == False]

    # assessment
    zebra_plot.set_system(classA_scores, classB_scores)
    dece = zebra_plot.get_delta_ECE()
    max_abs_LLR = abs(hstack((zebra_plot.classA_llr_laplace, zebra_plot.classB_llr_laplace))).max() / log(10)
    cat_idx = argwhere((cat_ranges < max_abs_LLR).sum(1) == 1).squeeze()

    str_dece = ('%.3f' if dece >= 5e-4 else '%.e') % dece
    str_max_abs_llr = ('%.3f' if max_abs_LLR >= 5e-4 else '%.e') % max_abs_LLR

    if dece == 0:
        str_dece = '0'

    if max_abs_LLR == 0:
        str_max_abs_llr = '0'

    challenge_results.at[idx, 'ROCCH-EER [%]'] = '%.2f' % (zebra_plot.rocch_eer * 100)
    challenge_results.at[idx, 'Cllr'] = '%.2f' % cllr(classA_scores, classB_scores)
    challenge_results.at[idx, 'min Cllr'] = '%.2f' % cllr(zebra_plot.classA_llr, zebra_plot.classB_llr)
    challenge_results.at[idx, 'ZEBRA Population [bit]'] = '%s' % str_dece
    challenge_results.at[idx, 'ZEBRA Individual'] = '%s' % str_max_abs_llr
    challenge_results.at[idx, 'ZEBRA Category'] = list(categorical_tags.keys())[cat_idx]

for sys in challenge_results["System"].unique():
    # save single markdowns
    md_out = DataFrame(challenge_results.loc[challenge_results["System"] == sys]).sort_values(by=['System', 'Gender', 'Dataset', 'Task']).to_markdown()
    with open('voiceprivacy-challenge-2020' + sep + 'results-' + sys + '.md', "w") as text_file:
        text_file.write(sub('\n\|[\s\d:-]+', '\n', sub('^\|\s+','', md_out)))

with open('voiceprivacy-challenge-2020' + sep + 'results.csv', "w") as text_file:
    text_file.write(challenge_results.to_csv())

with open('voiceprivacy-challenge-2020' + sep + 'results.tex', "w") as text_file:
    text_file.write(challenge_results.to_latex(index=False))

md_out = challenge_results.sort_values(by=['System', 'Gender', 'Dataset', 'Task']).to_markdown()
with open('voiceprivacy-challenge-2020' + sep + 'results.md', "w") as text_file:
    text_file.write(sub('\n\|[\s\d:-]+', '\n', sub('^\|\s+','', md_out)))


# To compare __one__ system in __multiple__ conditions
team = 'Baseline'
systems = ['primary', 'contrastive']
dece_values = []
title_strings = []
zebra_objects = []
filename_strings = []
for system in systems:
    scr_files = read_kaldi_folder_structure(glob_cmd='exp' + sep + team + sep + system + sep + '*' + sep + '*test*' + sep + 'scores')
    zebra_plot = PriorLogOddsPlots()

    dece_values.append([])
    dece_handle = dece_values[-1]
    zebra_objects.append([])
    zebra_handle = zebra_objects[-1]

    color_idx = 0
    for gender in scr_files.gender.unique():
        for dataset in scr_files.dataset.unique():
            for task in scr_files.task.unique():
                key = 'keys-voiceprivacy-2020' + sep + '_'.join((dataset, 'test', 'trials', gender))
                if 'a' in task:
                    key += '_anon'

                condition_label = '-'.join((dataset, task, gender))
                scr_selection = scr_files[(scr_files.gender == gender) & (scr_files.dataset == dataset) & (scr_files.task == task)]
                for idx, scr in scr_selection.iterrows():
                    zebra_framework(plo_plot=zebra_plot, scr_path=scr.scr, key_path=key, label=condition_label, color_min=cmap_tab20[color_idx % len(cmap_tab20)])
                    color_idx += 1

                    # for sorting
                    dece_handle.append(zebra_plot.get_delta_ECE())
                    zebra_handle.append(deepcopy(zebra_plot))

    title = team + ': ' + system
    mpl.title(title)
    fname = 'voiceprivacy-challenge-2020' + sep + 'multiple_conditions' + '_' + system
    export_zebra_framework_plots(plo_plot=zebra_plot, filename=fname, save_plot_ext='png', legend_loc=partial(place_legend, shrink=1.3))
    mpl.close(zebra_plot.ece_fig)

    title_strings.append(title)
    filename_strings.append(fname)

# Plotting with sorted legend
zebra_plots_sorted_legend(dece_values, zebra_objects, title_strings, filename_strings, legend_loc=partial(place_legend, shrink=1.3))

# To compare __multiple__ systems in __one__ condition (automation for all)
scr_files = read_kaldi_folder_structure(glob_cmd='exp' + sep + '*' + sep + '*' + sep + '*' + sep + '*test*' + sep + 'scores')

dece_values = []
title_strings = []
zebra_objects = []
filename_strings = []

for dataset in scr_files.dataset.unique():
    for task in scr_files.task.unique():
        for gender in scr_files.gender.unique():
            zebra_plot = PriorLogOddsPlots()

            dece_values.append([])
            dece_handle = dece_values[-1]
            zebra_objects.append([])
            zebra_handle = zebra_objects[-1]

            key = 'keys-voiceprivacy-2020' + sep + '_'.join((dataset, 'test', 'trials', gender))
            if 'a' in task:
                key += '_anon'

            condition_label = '-'.join((dataset, task, gender))
            scr_selection = scr_files[(scr_files.gender == gender) & (scr_files.dataset == dataset) & (scr_files.task == task)]
            color_idx = 0

            for idx, scr in scr_selection.iterrows():
                zebra_framework(plo_plot=zebra_plot, scr_path=scr.scr, key_path=key, label=scr.label, color_min=cmap_tab20[color_idx % len(cmap_tab20)])
                color_idx += 1

                # for sorting
                dece_handle.append(zebra_plot.get_delta_ECE())
                zebra_handle.append(deepcopy(zebra_plot))

            mpl.title(condition_label)
            title_strings.append(condition_label)
            fname = 'voiceprivacy-challenge-2020' + sep + 'task_wise_' + condition_label
            export_zebra_framework_plots(plo_plot=zebra_plot, filename=fname, save_plot_ext='png')
            mpl.close(zebra_plot.ece_fig)

            # title_strings.append(condition_label)
            filename_strings.append(fname)

# Example for sorting legend
zebra_plots_sorted_legend(dece_values, zebra_objects, title_strings, filename_strings)

