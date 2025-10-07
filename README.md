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

 Note that the generation of 50000 or more samples can take quite some time. We have executed the code on a regular CPU and it took about a day for each dataset to get generated.

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

To be able to run these scripts you need the quadriga_src code in `scenario_level_data/QuaDRiGa`. Note that we already uploaded the source code of QuaDRiGa with its license included (Version 2021.07.12_v2.6.1-0). You can download the source code also <a href="https://quadriga-channel-model.de/">here</a>. Next to standard python packages you also require the `h5py` package.

 <b> Comment </b><br>

 Note that the generation of 50000 or more samples can take quite some time. We have executed the code on a regular CPU and it took about a day for each dataset to get generated.

## Applying Signal Processing to the Datasets



## Toy Examples



## Requirements
The code is tested with `python 3.10`, `pytorch 2.5.1` and `pytorch-cuda 12.1`.

