#!/bin/env python
import pickle
import os
import pandas as pd


def load_dust_output(filepath):
    """
    Load dust output pickle file
    :param filepath: dust output file path
    :return: loaded dust output
    """

    with open(filepath, 'r') as f:
        dust_output = pickle.load(f)

    return dust_output


def load_all_dust(dust_out_dir):
    """
    Load all results from dust output directory and return all results as a list
    :param dust_out_dir: dust output directory
    :return: list of dust output
    """
    dust_file_names = os.listdir(dust_out_dir)

    dust_file_names = [f for f in dust_file_names if not f.startswith('.')]

    all_output = []

    for dust_file in dust_file_names:
        filepath = os.path.join(dust_out_dir, dust_file)
        all_output.append(load_dust_output(filepath))

    return all_output


def get_summary(all_output):
    """
    Generate summary from dust output
    :param all_output: all dust output dictionary
    :return:
    """

    summary_keys = ['status', 'obj_f', 'kkt_error', 'iter_num', 'constraint_violation', 'rhos', 'fn_eval_cnt',
                    'problem_name']

    summary_list = []
    rho_list = []
    for dust_output in all_output:
        tmp = {k: dust_output[k] for k in summary_keys if k in dust_output}
        tmp['rhos'] = tmp['rhos'][-1]
        summary_list.append(tmp)

        rho_list.append(pd.DataFrame({'problem_name': dust_output['problem_name'], 'rho': dust_output['rhos']}))

    summary_df = pd.DataFrame(summary_list)

    name_map = {'status': 'Status', 'obj_f': '$f(x)$', 'kkt_error': 'KKT Error', 'iter_num': 'Iter #',
                'constraint_violation': 'Violation', 'rhos': 'Rho', 'fn_eval_cnt': '$f(x)$ #',
                'problem_name': 'Problem'}

    cols = ['Problem', 'Iter #', '$f(x)$ #', '$f(x)$', 'Violation', 'KKT Error', 'Rho']
    summary_df.rename(columns=name_map, inplace=True)

    summary_df = summary_df[cols]

    summary_df['$f(x)$ #'] = summary_df['$f(x)$ #'].astype('int')
    summary_df['Iter #'] = summary_df['Iter #'] + 1
    summary_df['$f(x)$ #'] = summary_df['$f(x)$ #'] + 1

    with open('./summary/summary_table.tex', 'w') as f:
        summary_df.to_latex(f, index=False)

    rho_df = pd.concat(rho_list, ignore_index=True)

    return summary_df, rho_df
