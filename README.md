# Wireless Channel Modeling for Machine Learning - A Critical View on Standardized Channel Models
Welcome to the repository for the paper "Wireless Channel Modeling for Machine Learning - A Critical View on Standardized Channel Models". 

## Overview

The provided code is split into different parts
<ul>
  <li>Code for generating link-level (TDL and CDL) channel data (using the 5G Toolbox of Matlab)</li>
  <li>Code for generating scenario-level (QuaDRiGa) channel data (using the QuaDRiGa source code)</li>
  <li>Code for the linear methods, i.e., the PCA, the LMMSE estimator, and the sample covariance Gaussian sampling, as well as code for the Autoencoder for CSI compression.</li>
</ul>
The diffusion model estimator is not part of the code, but we used the implementation from <a href="https://github.com/benediktfesl/Diffusion_channel_est">this repository</a>. Moreover, we refer to the <a href="https://www.deepmimo.net/">DeepMIMO website </a> for the DeepMIMO data generation.

## Generarting Link-Level Channel Data

<ul>
  <li>Run the scripts `link_level_data/TDLCDL/generate_cdl.m` or `link_level_data/TDLCDL/generate_tdl.m` to generate link-level channel data. You can customize the type of model (`TDL-A`, `TDL-B`, ..) as well as configuration parameters such as the number of subcarriers within the scripts. The datasets are stored in `link_level_data/TDLCDL.m`. The file names contain the type of model as well as the number of generated samples.</li>
  <li>To transform the `.mat` datasets to `.npy` run the `mat_to_py.py` file in `link_level_data/TDLCDL`. It takes as input the particular system (`ofdm` or `mimo`), as well as the number of samples in the dataset, and the particular dataset (`tdl_a , `tdl_b`,...). An example would be 
    `python mat_to_py.py -system ofdm -n_samples 80000 -ds tdl_a`
  </li>We included toy datasets with 2000 samples from the tdl-e and cdl-e link-level channel models as `.npy` files.
</ul>
 
## Requirements
The code is tested with `python 3.10`, `pytorch 2.5.1` and `pytorch-cuda 12.1`.

