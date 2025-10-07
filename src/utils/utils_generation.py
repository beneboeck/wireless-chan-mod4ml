import numpy as np

def sCov_generation(X_train, n_samples):
    """
    simple Gaussian generator that samples n_samples times from a zero-mean Gaussian with sample covariance build from X_train

    Parameters:
    ------------
    X_train: np.ndarray
        contains the complex valued training channel realizations (in 2D) of shape [n_train_samples, dimension]
    n_samples: int
        number of samples to generate

    Returns:
    --------
    h_samples: np.ndarray
        contains the new complex valued channel realizations (in 2D) of shape [n_samples, dimension]
    """

    # compute the sample covariance
    sCov = (1 / X_train.shape[0]) * np.einsum('ni,nj->ij', X_train, X_train.conj(), optimize='optimal')

    # compute the eigenvalues and eigenvectors
    eigvals, eigvecs = np.linalg.eigh(sCov)

    # if the sCov is ill-conditioned, make sure that we have a proper covariance to sample from
    eigvals[eigvals < 0] = 0

    # compute the linear generator (optimal for Gaussian data) (cf. Eq. (20))
    generator = eigvecs @ np.diag(np.sqrt(eigvals)).astype(np.complex64)

    # sample
    e_samples = 1/np.sqrt(2) * (np.random.randn(n_samples, X_train.shape[1]) + 1j * np.random.randn(n_samples, X_train.shape[1]))
    h_samples = np.einsum('ij,nj->ni', generator, e_samples, optimize = 'optimal')

    return h_samples