import sys
import os

import numpy as np
from src.utils import utils_generation as ugen
from src.utils import utils_metrics as met
from src.utils import utils_general as ug
import configparser
import argparse


def main():
    # parse the dataset-name, the number of training samples, number of test samples as well as SNR in db
    parser = argparse.ArgumentParser()
    config_dataset = configparser.ConfigParser()
    parser.add_argument('-ds', '--dataset', type=str) # options: 'cdl_a', 'cdl_b', 'cdl_c', 'cdl_d', 'cdl_e' (see src/configs/dataset.ini)
    parser.add_argument('-ntrain', '--n_training', type=int)
    parser.add_argument('-n_samples', '--n_samples', type=int)
    parser.add_argument('-snr_db', '--snr_db', type=float)

    args = parser.parse_args()
    config_dataset.read('./src/configs/dataset.ini')

    # set up all configuration variables
    config_core = {
        'ds': args.dataset,
        'n_training': args.n_training,
        'n_samples': args.n_samples,
        'snr_db': args.snr_db,
    }
    config = {
        'data_path': config_dataset[args.dataset]['data_path'],
    }
    config.update(config_core)

    # create a directory to store the json as well as the results dictionaries
    config = ug.create_log(
        global_dic_path = config_core,
        global_dic = config,
        overall_path = './results/results_generation/' + args.dataset + '/sCov',
        comment = '')

    # load dataset
    X = np.load('./' + config['data_path'])
    X = X[:config['n_training'] + config['n_samples'], 0, :].reshape(config['n_training'] + config['n_samples'], -1)

    # normalize the datasets to have a proper SNR definition
    shape_X = X.shape[1]
    X_energy = np.mean(np.sum(np.abs(X) ** 2, axis=1))
    X = X * np.sqrt(shape_X / X_energy)
    X_train = X[:config['n_training'], :].reshape(config['n_training'], -1)
    X_test = X[config['n_training']:, :].reshape(config['n_samples'], -1)

    h_samples = ugen.sCov_generation(X_train, config['n_samples'])

    # define the snr for the spectral efficiency
    snr_lin = 10**(0.1 * config['snr_db'])
    noise_var = np.array([1 / snr_lin])

    spectral_efficency_sCov = np.log2(1 + np.sum(np.abs(h_samples) ** 2, axis=1)/noise_var[None])
    spectral_efficency_gt = np.log2(1 + np.sum(np.abs(X_test) ** 2, axis=1) / noise_var[None])
    max_value = np.ceil(np.max(spectral_efficency_gt))

    _, cdf_sCov = met.compute_cdf(spectral_efficency_sCov, max_value, 100)
    _, cdf_gt = met.compute_cdf(spectral_efficency_gt, max_value, 100)

    tv, histo_gen, histo_gt = met.dft_codebook_TVD(h_samples, X_test)
    print(f'total variation: {tv:.5f}')
    np.savez(config['dir_path'] + '/results.npz',**{
        'snr_db': np.array(config['snr_db']),
        'n_samples': np.array(config['n_samples']),
        'max_value': np.array([max_value]),
        'cdf_sCov': cdf_sCov,
        'cdf_gt': cdf_gt,
        'tv': np.array([tv]),
        'histo_gen': histo_gen,
        'histo_gt': histo_gt,
        }
    )

if __name__ == '__main__':
    main()