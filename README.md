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
  <li>Run the scripts <code>link_level_data/TDLCDL/generate_cdl.m</code> or <code>link_level_data/TDLCDL/generate_tdl.m</code> to generate link-level channel data. 
  You can customize the type of model (<code>TDL-A</code>, <code>TDL-B</code>, ..) as well as configuration parameters such as the number of subcarriers within the scripts. 
  The datasets are stored in <code>link_level_data/TDLCDL.m</code>.
  The file names contain the type of model as well as the number of generated samples.</li>
  <li>To transform the <code>.mat</code> datasets to <code>.npy</code> run the <code>mat_to_py.py</code> file in <code>link_level_data/TDLCDL</code>. 
  It takes as input the particular system (<code>ofdm</code> or <code>mimo</code>), as well as the number of samples in the dataset, and the particular dataset (<code>tdl_a</code> , <code>tdl_b</code>,...). 
  <br> An example would be <code>python mat_to_py.py -system ofdm -n_samples 80000 -ds tdl_a</code></li>
  <li>We included toy datasets with 2000 samples from the TDL-E and CDL-E link-level channel models as <code>.npy</code> files.</li>
</ul>
 
## Requirements
The code is tested with `python 3.10`, `pytorch 2.5.1` and `pytorch-cuda 12.1`.

