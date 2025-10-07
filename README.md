# Wireless Channel Modeling for Machine Learning - <br> A Critical View on Standardized Channel Models
Welcome to the repository for the paper "Wireless Channel Modeling for Machine Learning - A Critical View on Standardized Channel Models". 

## Overview

The provided code is split into different parts:
<ul>
  <li>Code for generating link-level (TDL and CDL) channel data (using the 5G Toolbox of Matlab)</li>
  <li>Code for generating scenario-level (QuaDRiGa) channel data (using the QuaDRiGa source code)</li>
  <li>Code for the Autoencoder applied to CSI compression.</li>
  <li>Code for the linear methods, i.e., the PCA, the LMMSE estimator, and the sample covariance Gaussian sampling.</li>
</ul>
The diffusion model estimator is not part of the code, but we used the implementation from <a href="https://github.com/benediktfesl/Diffusion_channel_est">this repository</a>. Moreover, we refer to the <a href="https://www.deepmimo.net/">DeepMIMO website </a> for the DeepMIMO data generation.

## Generating Link-Level Channel Data

<ul>
  <li>Run the scripts <code>link_level_data/TDLCDL/generate_cdl.m</code> or <code>link_level_data/TDLCDL/generate_tdl.m</code> to generate link-level channel data. 
  You can customize the type of model (<code>TDL-A</code>, <code>TDL-B</code>, ..) as well as configuration parameters such as the number of subcarriers within the scripts. 
  The datasets are stored in <code>link_level_data/TDLCDL</code>.
  The file names contain the type of model as well as the number of generated samples.</li>
  <li>To transform the <code>.mat</code> datasets to <code>.npy</code> run the <code>mat_to_py.py</code> file in <code>link_level_data</code>. 
  It takes as input the particular system (<code>ofdm</code> or <code>mimo</code>), as well as the number of samples in the dataset, and the particular dataset (<code>tdl_a</code> , <code>tdl_b</code>,...) as parser arguments. 
  <br> An example would be <code>python mat_to_py.py -system ofdm -n_samples 80000 -ds tdl_a</code> or <code>python mat_to_py.py -system mimo -n_samples 2000 -ds cdl_e</code>. Note that you must have generated a MATLAB dataset with the matching configuration beforehand.</li>
  <li>We included toy datasets with 2000 samples from the TDL-E and CDL-E link-level channel models as <code>.npy</code> files.</li>
</ul>
 
 <b> Requirements </b><br>

To be able to run these scripts you need the `5G Toolbox` of MATLAB. We used `MATLAB R2025b`. Next to standard python packages you also require the `h5py` package.

 <b> Comment </b><br>

 Note that the generation of 50000 or more samples can take quite some time. We have executed the code on a regular CPU and generated 80000 samples per channel model. It took about a day for each dataset to get generated.

## Generating Scenario-Level Channel Data

<ul>
  <li>Run the scripts <code>scenario_level_data/QuaDRiGa/generate_channels_with_structured_layout_rural.m</code> or <code>scenario_level_data/QuaDRiGa/generate_channels_with_structured_layout_urban.m</code> to generate OFDM scenario-level channel data. 
  You can customize configuration parameters such as the number of subcarriers within the scripts. 
  The datasets are stored in <code>scenario_level_data/QuaDRiGa</code>.
  The file names contain the type of model as well as the number of generated samples.</li>
  <li>To transform the <code>.mat</code> datasets to <code>.npy</code> run the <code>mat_to_py.py</code> file in <code>scenario_level_data</code>. 
  It takes as input the number of samples in the dataset, and the particular dataset (<code>rural</code> or <code>urban</code>) as parser arguments. 
  <br> An example would be <code>python mat_to_py.py -n_samples 80000 -ds rural</code>. Note that you must have generated a MATLAB dataset with the matching configuration beforehand.</li>
  <li>We included toy datasets with 2000 samples from the QuaDRiGa rural scenario-level channel models as <code>.npy</code> files.</li>
</ul>
 
 <b> Requirements </b><br>

To be able to run these scripts you need the quadriga_src code in `scenario_level_data/QuaDRiGa`. Note that we already uploaded the source code of QuaDRiGa with its license included (Version 2021.07.12_v2.6.1-0, only non-commercial use allowed!). You can download the source code also <a href="https://quadriga-channel-model.de/">here</a>. Next to standard python packages you also require the `h5py` package.

 <b> Comment </b><br>

 Note that the generation of 50000 or more samples can take quite some time. We have executed the code on a regular CPU and generated 80000 samples per channel model. It took about a day for each dataset to get generated.

## Applying Signal Processing and Machine Learning on the Datasets

To run the scripts covering the autoencoder, the PCA, the LMMSE estimator, and the Gaussian sampling, you need to execute the <code>main_compression_autoencoder.py</code>, <code>main_compression_pca.py</code>, <code>main_estimation_lmmse.py</code>, and <code>main_generation_sCov.py</code>, respectively. Each of these scripts take parser arguments as input.

<ul>
  <li> <code>main_compression_autoencoder.py</code> takes the dataset (e.g., <code>quadriga_rural</code>, <code>tdl_a</code>, ...), the latent dimension, the number of training samples, the number of test samples and the device (e.g., <code>cpu</code>, <code>cuda:0</code>, <code>cuda:1</code>, ...) as parser arguments (Example: <code>python main_compression_autoencoder.py -ds quadriga_rural -latent_dim 64 -ntrain 60000 -ntest 10000 -device cuda:0</code> </li>
  <li> <code>main_compression_pca.py</code> takes the dataset (e.g., <code>quadriga_rural</code>, <code>tdl_a</code>, ...), the latent dimension, the number of training samples and the number of test samples as parser arguments. Note that the latent dimension is meant complex valued, which is why it is twice the latent dimension (degree of freedom) in our work (Example: <code>python main_compression_pca.py -ds quadriga_rural -latent_dim 64 -ntrain 60000 -ntest 10000</code> </li>
  <li> <code>main_estimation_lmmse.py</code> takes the dataset (e.g., <code>cdl_a</code>, <code>cdl_b</code>, ...), the number of training samples, the number of test samples, and the snr in dB as parser arguments (Example: <code>python main_estimation_lmmse.py -ds cdl_a -ntrain 60000 -ntest 10000 -snr_db 10</code> </li>
  <li> <code>main_generation_sCov.py</code> takes the dataset (e.g., <code>cdl_a</code>, <code>cdl_b</code>, ...), the number of training samples, the number of samples to be generated, and the snr in dB (for the spectral efficiency evaluation) as parser arguments (Example: <code>python main_generation_sCov.py -ds cdl_a -ntrain 60000 -n_samples 10000 -snr_db 10</code> </li>
</ul>

Note that you need to have generated the matching dataset in `.npy` format beforehand. The `src` directory contains the dataset configuration file `configs/dataset.ini`. This file stores the path to the datasets. Note that if you adapt the number of generated samples, you also need to adapt the path names within this file (e.g., `data_path = link_level_data/ofdm_tdl_a_5000.npy` if you have generated 5000 samples with the TDL-A dataset). The corresponding section headers (e.g., `tdl_a` are used as the ds parser argument in the main files). The `src` directory also contains utility functions in `utils` that comprise the linear methods, evaluation methods and general organization methods such as the generation of directories for saving the results. It also contains the `modules` storing the autoencoder architecture.

All main-files store the results in newly generated directories in the `results` directory. The results contain the `experiment_config.json` file as well as an `.npz` file that stores important results.

<b> Requirements </b><br>

Next to standard python package, you also require `torch`. We used  `python 3.10`, `pytorch 2.5.1` and `pytorch-cuda 12.1`.

## Toy Examples

We have uploaded toy datasets. To test out whether the code works for you, you should immediately be able to run experiments with the following commands:

<ul>
  <li><code>python main_compression_pca.py -ds tdl_e -latent_dim 2 -ntrain 1500 -ntest 500</code></li>
  <li><code>python main_compression_pca.py -ds quadriga_rural -latent_dim 64 -ntrain 1500 -ntest 500</code></li>
  <li><code>python main_estimation_lmmse.py -ds cdl_e -ntrain 1500 -ntest 500 -snr_db 10</code></li>
</ul>

By doing so, there should be new directories in the `results` directory containing the results as `.npz` files. 


