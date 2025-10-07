import sys
import os

import numpy as np
from src.utils import utils_general as ug
from src.utils import utils_compression as ucom
import configparser
import argparse

def main():

    # parse the dataset-name, the latent dimension, the number of training samples, number of test samples as well as the device
    parser = argparse.ArgumentParser()
    config_dataset = configparser.ConfigParser()
    parser.add_argument('-ds', '--dataset', type=str) # options: 'quadriga_rural', 'quadriga_urban', 'tdl_a', 'tdl_b', 'tdl_c', 'tdl_d', 'tdl_e' (see src/configs/dataset.ini)
    parser.add_argument('-latent_dim', '--latent_dim', type=int) # note that this is the cplx valued latent dimension, i.e., 2 * N_L in the paper!
    parser.add_argument('-ntrain', '--n_training', type=int)
    parser.add_argument('-ntest', '--n_test', type=int)

    args = parser.parse_args()
    config_dataset.read('./src/configs/dataset.ini')

    # set up all configuration variables (fixed batchsize and validation samples)
    config_core = {
        'ds': args.dataset,
        'latent_dim': args.latent_dim,
        'n_training': args.n_training,
        'n_test': args.n_test,
    }
    config = {
        'data_path': config_dataset[args.dataset]['data_path'],
    }
    config.update(config_core)

    # create a directory to store the json as well as the results dictionaries
    config = ug.create_log(
        global_dic_path = config_core,
        global_dic = config,
        overall_path = './results/results_compression/' + args.dataset + '/pca',
        comment = '')

    # load dataset
    X = np.load('./' + config['data_path'])
    X_train = X[:config['n_training'], :, :].reshape(config['n_training'], -1)
    X_test = X[config['n_training']:config['n_training'] + config['n_test'], :, :].reshape(config['n_test'], -1)

    # apply pca
    _, _, principal_components, mean = ucom.complex_pca(X_train, config['latent_dim'])
    X_test_pca = ucom.compress_and_reconstruct_data(X_test, principal_components, mean)

    # validate pca
    nmse = np.mean(np.sum(np.abs(X_test_pca - X_test)**2,axis=1)/X_test.shape[1])
    print(f'reconstruction nMSE: {nmse:.5f}')

    # save the results in a npz dictionary
    np.savez(config['dir_path'] + '/results.npz', **{'latent_dim': np.array(config['latent_dim']), 'nmse': np.array(nmse)})

if __name__ == '__main__':
    main()