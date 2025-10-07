import sys
import os

import numpy as np
from src.utils import utils_general as ug
from src.modules import autoencoder as auto
import torch
import configparser
import argparse
from src.utils import dataset as ds

def main():

    # parse the dataset-name, the latent dimension, the number of training samples, number of test samples as well as the device
    parser = argparse.ArgumentParser()
    config_dataset = configparser.ConfigParser()
    parser.add_argument('-ds', '--dataset', type=str) # options: 'quadriga_rural', 'quadriga_urban', 'tdl_a', 'tdl_b', 'tdl_c', 'tdl_d', 'tdl_e' (see src/configs/dataset.ini)
    parser.add_argument('-latent_dim', '--latent_dim', type=int)
    parser.add_argument('-ntrain', '--n_training', type=int)
    parser.add_argument('-ntest', '--n_test', type=int)
    parser.add_argument('-device', '--device', type=str)

    # fixed variables for the autoencoder (the specific architecture and configuration is not crucial for our main outcomes of our work)
    lr = 1e-4
    ch_factor = 3
    n_conv = 3
    miter = 1000

    args = parser.parse_args()
    config_dataset.read('./src/configs/dataset.ini')

    # set up all configuration variables (fixed batchsize and validation samples)
    config_core = {
        'ds': args.dataset,
        'latent_dim': args.latent_dim,
        'n_training': args.n_training,
        'n_val': 10000,
        'bs': 256,
        'n_test': args.n_test,
        'lr': lr,
        'ch_factor': ch_factor,
        'n_conv': n_conv,
        'miter': miter,
    }
    config = {
        'data_path': config_dataset[args.dataset]['data_path'],
        'n_subc' : int(config_dataset[args.dataset]['n_subc']),
        'n_symbols': int(config_dataset[args.dataset]['n_symbols']),
        'device': args.device,
    }

    config.update(config_core)

    # create a directory to store the json as well as the results dictionaries
    config = ug.create_log(
        global_dic_path=config_core,
        global_dic=config,
        overall_path='./results/results_compression/' + args.dataset + '/ae',
        comment='')

    # prepare the dataset for the autoencoder
    _, _, _, loader_ae_train, loader_ae_val, loader_ae_test = ds.prepare_data_for_AE(
        path_taken=True,
        data_path=config['data_path'],
        nt=config['n_training'],
        nval=config['n_val'],
        ntest=config['n_test'],
        bs=config['bs'],
        h_sizes=[config['n_subc'], config['n_symbols']])

    # create the autoencoder
    ae = auto.autoencoder(
        device = config['device'],
        dim = [config['n_subc'], config['n_symbols']],
        ch_factor=config['ch_factor'],
        n_conv=config['n_conv'],
        ld=config['latent_dim'],
    ).to(config['device'])

    # train the autoencoder
    risk_val = ae.fit(config['lr'], config['miter'], loader_ae_train, loader_ae_val)

    # validate the autoencoder
    nmse = []
    ae.eval()
    with torch.no_grad():
        for ind, samples in enumerate(loader_ae_test):
            sample_in = samples.to(config['device'])
            sample_hat = ae.forward(sample_in)
            sample_in_cplx1d = (sample_in[:, 0, :, :] + 1j * sample_in[:, 1, :, :]).reshape(sample_in.shape[0], -1)
            sample_hat_cplx1d = (sample_hat[:, 0, :, :] + 1j * sample_hat[:, 1, :, :]).reshape(sample_hat.shape[0], -1)
            nmse_value = torch.mean( torch.sum(torch.abs(sample_hat_cplx1d - sample_in_cplx1d) ** 2, dim = 1)/ sample_hat_cplx1d.shape[1]).detach().to('cpu').numpy()
            nmse.append(nmse_value)

    # save the results in a npz dictionary
    nmse = np.mean(np.array(nmse))
    print(f'reconstruction nMSE: {nmse:.5f}')
    np.savez(config['dir_path'] + '/results.npz', **{'latent_dim': config['latent_dim'], 'nmse': nmse, 'risk_val': risk_val})

if __name__ == '__main__':
    main()