import numpy as np
from scipy.linalg import dft

def compute_cdf(values, max_value, resolution):
    """
    calculate the cumulative density function of the given values untul max_value with a given resolution

    Parameters:
    ---------
    values: np.ndarray
        contains the samples from the distribution whose CDF we estimate
    max_value: float
        maximal value that is considered for the CDF
    resolution: int
        number of gridpoints for the cdf

    Returns:
    ----------
    max_value: float
        maximal value that is considered for the CDF
    cdf: np.ndarray
        values of the cdf
    """
    cdf = np.zeros(resolution)
    points = np.linspace(0, max_value, resolution)
    for i in range(resolution):
        cdf[i] = np.sum(values <= points[i])/len(values)

    return max_value, cdf

def dft_codebook_TVD(h_gen, h_gt):
    """
    compute the total variation between two normalized histograms interpreted as pmfs

    Paramaeters:
    ----------------
    h_gen: np.ndarray
        contains the samples from the generative model with shape [n_samples, dimension]
    h_gt: np.ndarray
        contains the samples from the channel model with shape [n_samples, dimension]

    Returns:
    -------------
    tv: float
        the total variation between the normalized histograms
    histo_gen:  np.ndarray
        normalized histogram of the samples from the generative model projected on the DFT codebook
    histo_gt: np.ndarray
        normalized histogram of the samples from the channel model projected on the DFT codebook
    """

    # compute normalized DFT
    n_ant = h_gen.shape[1]
    F = dft(n_ant)                 # default unnormalized DFT
    F /= np.linalg.norm(F, axis=0, keepdims=True)  # normalize columns

    # initialize histograms
    histo_gen = np.zeros(n_ant)
    histo_gt = np.zeros(n_ant)

    # compute the best-suited indices of the channels withe DFT codebook
    profile_gen = np.argmax(np.abs(np.einsum('ij,nj->ni',F.conj().T,h_gen)),axis=1)
    profile_gt = np.argmax(np.abs(np.einsum('ij,nj->ni', F.conj().T, h_gt)), axis=1)

    # compute the histograms
    for i in range(h_gen.shape[0]):
        histo_gen[profile_gen[i]] += 1
        histo_gt[profile_gt[i]] += 1

    # normalize the histograms
    histo_gen = histo_gen/np.sum(histo_gen)
    histo_gt = histo_gt / np.sum(histo_gt)

    # compute the total variation
    tv = 0.5 * np.sum(np.abs(histo_gen - histo_gt))

    return tv, histo_gen, histo_gt