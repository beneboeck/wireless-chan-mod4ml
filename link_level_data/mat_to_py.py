import h5py
import numpy as np
import argparse

def main():

    parser = argparse.ArgumentParser()

    # Path to your .mat file
    parser.add_argument('-system', '--system', type=str) # 'ofdm' or 'mimo'
    parser.add_argument('-n_samples', '--n_samples', type=int)
    parser.add_argument('-ds', '--dataset', type=str) # 'tdl-a', 'tdl-b', 'tdl-c', 'tdl-d', 'tdl-e', 'cdl-a', 'cdl-b', 'cdl-c', 'cdl-d', 'cdl-e'
    args = parser.parse_args()

    path = './' + args.system + '_' + args.dataset + '_' + str(args.n_samples) + '.mat'

    # Open with h5py
    with h5py.File(path, "r") as f:
        # Check what keys are inside
        #print(list(f.keys()))
        # Load datasets (MATLAB stores them as HDF5 datasets)
        H_all_real = np.array(f[args.system + '_channel_real'])
        H_all_imag = np.array(f[args.system + '_channel_imag'])

    # save complex valued data + normalize (shuffling is not necessary for these link-level datasets)
    H_all = H_all_real + 1j * H_all_imag
    H_all = np.transpose(np.squeeze(np.array(H_all)),(2,1,0))
    shape_H = np.prod(H_all.shape[1:])
    H_energy = np.mean(np.sum(np.abs(H_all)**2,axis=(1,2)))
    H_all = H_all * np.sqrt(shape_H / H_energy)

    path_save = './' + args.system + '_' + args.dataset + '_' + str(args.n_samples) + '.npy'

    np.save(path_save, H_all)

if __name__ == '__main__':
    main()