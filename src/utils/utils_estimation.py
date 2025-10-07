import numpy as np

def lmmse(X_train, Y_test, noise_var):
    """
    implements the linear minimum mean squared error estimator, where the sample covariance is build from X_train and
    the lmmse estimator is then applied to denoise Y_test with noise variance noise_var (in this script we assume the channels to have zero mean,
    but it can be easily extended to non zero means (see Eq. (19) in our work)

    Parameters:
    X_train: np.ndarray
        contains the complex valued channel realizations (in 2D) of shape [n_train_samples, dimension]
    Y_test: np.ndarray
        contains the complex valued channel observation to be denoised (in 2D) of shape [n_train_samples, dimension]
    noise_var: float
        the noise variance that is assumed to be known for the denoising

    Returns:
    X_est: np.ndarray
        contains the denoised complex valued channel estimations (in 2D) of shape [n_train_samples, dimension]
    """
    # compute the sample covariance
    sCov = (1 / X_train.shape[0]) * np.einsum('ni,nj->ij', X_train, X_train.conj(), optimize='optimal')

    # compute the lmmse matrix (cf. Eq. (19) with zero means)
    Eys = np.eye(sCov.shape[0])
    lmmse_filter = sCov @ np.linalg.inv(sCov + noise_var * Eys)

    # denoise
    X_est = np.einsum('ij,nj->ni', lmmse_filter, Y_test, optimize='optimal')
    return X_est