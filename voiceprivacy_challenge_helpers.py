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
    score_glob = score_glob.drop(score_glob[score_glob.str.contains('dev_enrolls')].index)
    score_glob = score_glob.drop(score_glob[score_glob.str.contains('dev_trials')].index)
    score_glob = score_glob.reset_index(drop=True)
    score_files = score_glob.str.split(sep, expand=True)
    
    anon_identifier = Series(glob('exp/*/ASR-libri*test_asr_*')).str.split('test_asr_', expand=True)
    for i, anon in enumerate(anon_identifier[1]):
        score_files[2] = score_files[2].str.replace(anon, 'anon')

    score_files_tmp = score_files[2].str.split('-', expand=True)
    score_files_tmp2 = score_files[3]
    score_files.drop(columns=[2, 3], inplace=True)
    for i in range(len(score_files_tmp.columns)):
        score_files.insert(loc=2+score_files_tmp.columns[i], column=2+score_files_tmp.columns[i], value=score_files_tmp[i].values)
    score_files.insert(loc=len(score_files.columns), column=len(score_files.columns), value=score_files_tmp2.values)

    # establish flags
    protected_enrol_test = Series(score_glob[score_files.loc[:, 3].str.contains('anon')])
    protected_test = Series(score_glob[score_files.loc[:, 4].str.contains('anon')]).drop(index=protected_enrol_test.index)
    # original = Series(score_glob).drop(index=protected_enrol_test.index).drop(index=protected_test.index)
    flag_gender = score_files.loc[:, 4].str.contains('_f')
    flag_libri = score_files.loc[:, 4].str.contains('libri')
    flag_vctk_common = score_files.loc[:, 4].str.contains('common')

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
    scr_files_ds['label'] = score_glob.str.split(sep, expand=True).iloc[:, 1]
    scr_files_ds['key'] = 'data/vctk_test_trials_' + scr_files_ds['gender'] + '/trials'
    scr_files_ds.loc[flag_libri, 'key'] = 'data/libri_test_trials_' + scr_files_ds['gender'] + '/trials'
    scr_files_ds.loc[flag_vctk_common, 'key'] = 'data/vctk_test_trials_' + scr_files_ds['gender'] + '_common/trials'

    return scr_files_ds


# Shrink current axis by 20%, see:
# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
def place_legend(figure, legend, shrink=0.2):
    ax = mpl.figure(figure).get_axes()[0]
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * shrink/2, box.width, box.height * (1 - shrink/2)])
    ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.1-shrink/4), fancybox=True, shadow=True, ncol=2)
