clear; clc;

%% Carrier and OFDM info
carrier = nrCarrierConfig;        % default carrier
ofdmInfo = nrOFDMInfo(carrier);

num_samples = 2000; % define the number of samples

%% CDL channel (static, narrowband if DelaySpread=0 and Doppler=0)
cdl = nrCDLChannel;
cdl.DelayProfile = "CDL-E";      % choose profile
cdl.DelaySpread = 0;             % 0 -> flat (narrowband)
cdl.MaximumDopplerShift = 0;     % 0 -> static
cdl.CarrierFrequency = 3.5e9;    % define center frequency
cdl.SampleRate = ofdmInfo.SampleRate; 
cdl.ChannelResponseOutput = 'ofdm-response'
cdl.ChannelFiltering = false; 

% MIMO sizes
Nt = 16; 
Nr = 8;
cdl.TransmitAntennaArray.Size = [Nt 1 1 1 1];
cdl.ReceiveAntennaArray.Size  = [Nr 1 1 1 1];
cdl.TransmitAntennaArray.ElementSpacing = [0.5, 1, 1, 1];
cdl.ReceiveAntennaArray.ElementSpacing  = [0.5, 1, 1, 1];

%% Prepare variables

mimo_channels = zeros(num_samples, Nr, Nt);

for k = 1:num_samples
    if mod(k,100) == 0
        fprintf('\rProgress: %d %%', floor(100*k/num_samples));
    end
    release(cdl);
    % it is important to set a new seed for each sample as the same results
    % in the exact same channel realization
    cdl.Seed = k;
    [ofdmResponse,timingOffset] = cdl(carrier);
    
    mimo_channels(k,:,:) = squeeze(ofdmResponse(1,1,:,:));
end

mimo_channel_real = real(mimo_channels);
mimo_channel_imag = imag(mimo_channels);

% save data
cdl_type = char(cdl.DelayProfile);
channel_type = lower(cdl_type(1:3));
channel_number = lower(cdl_type(5));
num_samples_char = char(string(num_samples));

path = join(['../mimo_', channel_type, '_', channel_number, '_', num_samples_char]);
save(path, 'mimo_channel_real', 'mimo_channel_imag', '-v7.3');