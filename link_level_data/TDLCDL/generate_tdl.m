% Basic setup
clear;
clc;
carrier = nrCarrierConfig;
carrier.NSizeGrid = 4;
carrier.SubcarrierSpacing = 60;
channel = nrTDLChannel;

channel.DelayProfile = "TDL-E";
channel.MaximumDopplerShift = 800;
ofdmInfo = nrOFDMInfo(carrier);
channel.SampleRate = ofdmInfo.SampleRate;
channel.ChannelResponseOutput = "ofdm-response";
channel.ChannelFiltering = false;
channel.NumTimeSamples = sum(ofdmInfo.SymbolLengths(1:carrier.SymbolsPerSlot));

num_samples = 2000;


ofdm_channels = zeros(num_samples, carrier.NSizeGrid * 12, 14);

for k = 1:num_samples
    if mod(k,100) == 0
        fprintf('\rProgress: %d %%', floor(100*k/num_samples));
    end
    release(channel);
    channel.Seed = k;
    [ofdmResponse,timingOffset] = channel(carrier);
    ofdm_channels(k, :, :) = squeeze(ofdmResponse(:, :, 1, 1));
end

ofdm_channel_real = real(ofdm_channels);
ofdm_channel_imag = imag(ofdm_channels);

% save data
tdl_type = char(channel.DelayProfile);
channel_type = lower(tdl_type(1:3));
channel_number = lower(tdl_type(5));
num_samples_char = char(string(num_samples));

path = join(['../ofdm_', channel_type, '_', channel_number, '_', num_samples_char]);
save(path, 'ofdm_channel_real', 'ofdm_channel_imag', '-v7.3');