from os import sep
from glob import glob
import matplotlib.pyplot as mpl
from pandas import Series, DataFrame
from numpy import argwhere


__author__ = "Andreas Nautsch"
__email__ = "nautsch@eurecom.fr"
__coauthor__ = ["Jose Patino", "Natalia Tomashenko", "Junichi Yamagishi", "Paul-Gauthier Noé", "Jean-François Bonastre", "Massimiliano Todisco", "Nicholas Evans"]
__credits__ = ["Niko Brummer", "Daniel Ramos", "Edward de Villiers", "Anthony Larcher"]
__license__ = "LGPLv3"


def read_kaldi_folder_structure(glob_cmd):
    """
    Gather score files of multiple experiments in easy tractable pandas database structure of score files

    :param glob_cmd: regular expression for searching files
    :return: scr_files: pandas.DataFrame object with meta-information: gender, dataset, task, label tailored to the 2020 VoicePrivacy challenge
    """
    score_glob = Series(glob(glob_cmd))
    score_files = score_glob.str.split(sep, expand=True)

    results_identifier = score_files[3].str.split('_', expand=True).iloc[:, 1:].apply(lambda x: '_'.join(filter(None, x)), axis=1)
    if not results_identifier.isna().all():
        for idx in argwhere(results_identifier.str.len().values > 0).squeeze():
            score_files.iloc[idx, 4] = score_files.iloc[idx, 4].replace(results_identifier[idx], 'anon')

    score_files_tmp = score_files[4].str.split('-', expand=True)
    score_files_tmp2 = score_files[5]
    score_files.drop(columns=[4, 5], inplace=True)
    for i in range(len(score_files_tmp.columns)):
        score_files.insert(loc=4+score_files_tmp.columns[i], column=4+score_files_tmp.columns[i], value=score_files_tmp[i].values)
    score_files.insert(loc=len(score_files.columns), column=len(score_files.columns), value=score_files_tmp2.values)

    # establish flags
    protected_enrol_test = Series(score_glob[score_files.loc[:, 5].str.contains('anon')])
    protected_test = Series(score_glob[score_files.loc[:, 6].str.contains('anon')]).drop(index=protected_enrol_test.index)
    # original = Series(score_glob).drop(index=protected_enrol_test.index).drop(index=protected_test.index)
    flag_gender = score_files.loc[:, 6].str.contains('_f')
    flag_libri = score_files.loc[:, 6].str.contains('libri')
    flag_vctk_common = score_files.loc[:, 6].str.contains('common')

    # extract score paths with boolean meta information
    scr_files_ds = DataFrame({'scr': score_glob})
    scr_files_ds['gender'] = 'm'
    scr_files_ds.loc[flag_gender, 'gender'] = 'f'
    scr_files_ds['dataset'] = 'vctk'
    scr_files_ds.loc[flag_libri, 'dataset'] = 'libri'
    scr_files_ds.loc[flag_vctk_common, 'dataset'] = 'vctk_common'
    scr_files_ds['task'] = 'o-o'
    scr_files_ds.loc[protected_test.index, 'task'] = 'o-a'
    scr_files_ds.loc[protected_enrol_test.index, 'task'] = 'a-a'
    team_sys = score_glob.str.split(sep, expand=True).iloc[:, 1:3]
    scr_files_ds['label'] = team_sys[1] + '-' + team_sys[2]

    return scr_files_ds


# Shrink current axis by 20%, see:
# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
def place_legend(figure, legend, shrink=0.2):
    ax = mpl.figure(figure).get_axes()[0]
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * shrink/2, box.width, box.height * (1 - shrink/2)])
    ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.1-shrink/4), fancybox=True, shadow=True, ncol=2)
