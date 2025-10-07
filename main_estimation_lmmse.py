import sys
import os

import numpy as np
from src.utils import utils_estimation as uest
from src.utils import utils_general as ug
import configparser
import argparse

def main():

    # parse the dataset-name, the number of training samples, number of test samples as well as SNR in db
    parser = argparse.ArgumentParser()
    config_dataset = configparser.ConfigParser()
    parser.add_argument('-ds', '--dataset', type=str) # options: 'cdl_a', 'cdl_b', 'cdl_c', 'cdl_d', 'cdl_e' (see src/configs/dataset.ini)
    parser.add_argument('-ntrain', '--n_training', type=int)
    parser.add_argument('-ntest', '--n_test', type=int)
    parser.add_argument('-snr_db', '--snr_db', type=float)

    # set up all configuration variables (fixed batchsize and validation samples)
    args = parser.parse_args()
    config_dataset.read('./src/configs/dataset.ini')
    config_core = {
        'ds': args.dataset,
        'n_training': args.n_training,
        'n_test': args.n_test,
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
        overall_path = './results/results_estimation/' + args.dataset + '/lmmse',
        comment = '')

    # load dataset
    X = np.load('./' + config['data_path'])
    X = X[:config['n_training'] + config['n_test'], :, :].reshape(config['n_training'] + config['n_test'], -1)

    # normalize the datasets to have a proper SNR definition
    shape_X = X.shape[1]
    X_energy = np.mean(np.sum(np.abs(X) ** 2, axis=1))
    X = X * np.sqrt(shape_X / X_energy)

    X_train = X[:config['n_training'], :].reshape(config['n_training'], -1)
    X_test = X[config['n_training']:config['n_training'] + config['n_test'], :].reshape(config['n_test'], -1)

    snr_lin = 10**(0.1 * args.snr_db)
    noise_var = 1 / snr_lin

    Y_test = X_test + np.sqrt(noise_var / 2) * (np.random.randn(*X_test.shape) + 1j * np.random.randn(*X_test.shape))
    X_est = uest.lmmse(X_train, Y_test, noise_var)

    nmse = np.mean(np.sum(np.abs(X_est - X_test)**2,axis=1)/X_test.shape[1])

    print(f'estimation nMSE: {nmse:.5f}')
    np.savez(config['dir_path'] + '/results.npz', **{'snr_db': np.array(config['snr_db']), 'nmse': np.array(nmse)})

if __name__ == '__main__':
    main()