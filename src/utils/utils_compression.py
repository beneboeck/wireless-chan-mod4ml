import numpy as np

def complex_pca(data, num_components):
    """
    implements the cplx valued pca

    Parameters:
    ------------------
    data: np.ndarray
        The complex-valued data matrix of shape (n_samples, n_features).
    num_components: int
        The number of principal components to return.

    Returns:
    proj_data: np.ndarray
        The cplx-valued encoded compressed representation of the data of shape (n_samples, num_components)
    sorted_ev: np.ndarray
        All real valued sorted eigenvalues of the sample covariance
    p_components: np.ndarray
        The num_components eigenvectors (i.e., the principal components) of the sample covariance (sorted)
    mean: np.ndarray
        The dataset mean (actually not needed here since it is approximately zero, but included for generalization)
    """

    # Compute the mean (not needed)
    mean = np.mean(data, axis=0)
    centered_data = data - mean

    # Compute the covariance matrix.
    covariance_matrix = np.cov(centered_data, rowvar=False, bias=True)

    # Perform eigendecomposition on the covariance matrix.
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sort eigenvalues and eigenvectors in descending order.
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_ev = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Select the top num_components principal components (eigenvectors).
    p_components = sorted_eigenvectors[:, :num_components]

    # Project the centered data onto the principal components.
    proj_data = np.dot(centered_data, p_components.conj())

    return proj_data, sorted_ev, p_components, mean

def compress_and_reconstruct_data(data, p_components, mean):
    """
    use the principal components to compress and reconstruct given data in an autoencoder-fashion

    Parameters:
    ------------
    data: np.ndarray
        The new complex-valued data matrix to process.
    p_components: np.ndarray
        The principal components (eigenvectors) from the training data.
    mean: np.ndarray
        The mean of the training data. (again not needed, just included for generalization)

    Returns:
    -----------
    - reconstructed_data: np.ndarray
        The reconstructed data in the original domain.
    """
    # Center the new data using the mean from the training data.
    centered_data = data - mean

    # Project the centered new data onto the principal components to compress it.
    compressed_data = np.dot(centered_data, p_components.conj())

    # Reconstruct the centered data by multiplying with the original PC matrix.
    reconstructed_centered_data = np.dot(compressed_data, p_components.T)

    # Add the mean back to de-center the data and get the final reconstruction.
    reconstructed_data = reconstructed_centered_data + mean
    return reconstructed_data
