import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np

class default_dataset(Dataset):
    def __init__(self,y, type='real'):
        """
        default standard dataset definition

        Parameters:
        -----------
        y: torch.tensor of shape [dataset_size, number_subcarriers, number_time_symbols] (cplx valued)
            or [dataset_size, 2, number_subcarriers, number_time_symbols] (real valued)
        type: either "real" or "cplx" and encodes whether we store complex valued or real valued datasets (see the two options for y, it has to match with the shape of y)
        """
        super().__init__()
        if type == 'real':
            self.y = y.float()
        else:
            self.y = y.cfloat()

    def __len__(self):
        return self.y.size(0)

    def __getitem__(self,idx):
        return self.y[idx,:]


def default_ds_dl_split(X_train,X_val,X_test,bs_train):
    """
    standard routine of splitting the dataset into training, validation and testing if the batchsize can be the same for all

    Parameters:
    ----------
    X_train: torch.tensor of shape [n_training_samples, number_subcarriers, number_time_symbols] (cplx valued)
            or [n_training_samples, 2, number_subcarriers, number_time_symbols] (real valued)
    X_val: torch.tensor of shape [n_val_samples, number_subcarriers, number_time_symbols] (cplx valued)
            or [n_val_samples, 2, number_subcarriers, number_time_symbols] (real valued)
    X_test: torch.tensor of shape [n_test_samples, number_subcarriers, number_time_symbols] (cplx valued)
            or [n_test_samples, 2, number_subcarriers, number_time_symbols] (real valued)

    Returns:
    -----------
    ds_train,ds_val,ds_test,dl_train,dl_val,dl_test: the corresponding datasets (starting with ds) and dataloaders (starting with dl)
    """
    ds_train = default_dataset(X_train)
    ds_val = default_dataset(X_val)
    ds_test = default_dataset(X_test)
    dl_train = DataLoader(ds_train, shuffle=True, batch_size=bs_train)
    dl_val = DataLoader(ds_val, shuffle=True, batch_size=bs_train)
    dl_test = DataLoader(ds_test, shuffle=True, batch_size=bs_train)
    return ds_train,ds_val,ds_test,dl_train,dl_val,dl_test

def prepare_data_for_AE(nt, nval, ntest, bs, h_sizes, data_path=None, X=None, path_taken=False):
    """
    prepares the dataset and outputs the datasets and dataloaders of training, validation and testset

    Parameters:
    ----------------
    X: cplx valued 2d nt x hdim channels (if not None)
    data_path: alternativ to X, we load an npy file stored at data_path
    path_taken: bool that controls whether data_path or X is taken
    nt: number of training samples
    nval: number of validation samples
    ntest: number of test samples
    bs: batchsize (if -1, then we take all, important for CSGMM)
    h_sizes: list storing the dimensions of the cplx valued channel realizations (e.g., n_subc x n_times for OFDM, or n_antennas for SIMO)
    """
    if path_taken == True:
        str_data = '../' + data_path
        X = np.load(str_data)
    # reshape X to the desired shape
    X = X.reshape(X.shape[0], *h_sizes)

    # stack real and imaginary part into the channel dimension (for the autoencoder we always want real valued datasets)
    X_stacked = np.empty((X.shape[0], 2, *h_sizes))
    X_stacked[:, 0, :] = np.real(X)
    X_stacked[:, 1, :] = np.imag(X)
    X_stacked = torch.from_numpy(X_stacked)

    # split into train, val and test data
    X_train = X_stacked[:nt, :]
    X_val = X_stacked[nt:nt + nval, :]
    X_test = X_stacked[nt + nval:nt + nval + ntest, :]

    ds_train, ds_val, ds_test, l_train, l_val, l_test = default_ds_dl_split(X_train, X_val, X_test, bs)
    return ds_train, ds_val, ds_test, l_train, l_val, l_test