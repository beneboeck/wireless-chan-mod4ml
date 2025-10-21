clear all %#ok<CLALL>
close all
addpath('./quadriga_src/')
addpath('./utils/')
addpath('./visual/')

% This file generates 4D channels in spatial, frequency and time domain.

%% System Parameters
rep_factor = 1;                                 %number of different scenarios with the same statistical characteristics (should kept to be 1 to have one specific scenario)

no_of_UEs_outdoor = 60;                        % number of channels per scenario
no_of_UEs_indoor = 20;     
no_of_UEs_perScenario = no_of_UEs_outdoor + no_of_UEs_indoor;

n_symbols = 14;                                 %number of times symbols per slot
duration_per_slot = 5e-3;                       %duration per slot
n_slots = 1;                                    %number slots
symbol_duration = duration_per_slot/n_symbols;
bandwidth = 48 * 60e3;                              % overall bandwidth
carriers = 48;                                  % number subcarriers
subcarrier_spacing = bandwidth / carriers;

bs_no_vertical_elements = 1;
bs_no_horizontal_elements = 1;
ms_no_vertical_elements = 1;
ms_no_horizontal_elements = 1;
bs_mult = bs_no_horizontal_elements * bs_no_vertical_elements;
ms_mult = ms_no_horizontal_elements * ms_no_vertical_elements;
n_mult = bs_mult * ms_mult;
K = 1;                                          % polarization indicator: K = 1 -> vertical polarization only (page 33)

%% User Parameters
v_min_outdoor = 10;                             %minimal outdoor velocity of users in km/h
v_max_outdoor = 50;                             %maximal outdoor velocity of users in km/h
v_max_indoor = 5;                               %maximal indoor velocity of users in km/h
n_streets = 3;
n_indoor_centers = 4;

%% Layout parameters
s = qd_simulation_parameters;
s.show_progress_bars = 0;
s.center_frequency = 6e9;
s.sample_density = 1.2;
s.use_absolute_delays = 1;  % include delay of the LOS path

min_dist_to_BS = 20;                    % minimal distance of the users to the BS
max_dist_to_BS = 500;                   % maximal distance of the users to the BS (multiple of 100)
sector_anglespread = 120 * pi/180;       % the angular range the considered sector covers

overall_norm2 = 0;


rng(123)
[a_streets, b_streets, dir_streets, indoor_centers] = generate_streets_and_indoor_centers(min_dist_to_BS, max_dist_to_BS, sector_anglespread, n_streets, n_indoor_centers);
%rng('shuffle')

H_4d = zeros(rep_factor,no_of_UEs_perScenario,bs_mult,ms_mult,carriers,n_slots*n_symbols);


for i_process = 1:rep_factor 
    if mod(i_process,10) == 0
        disp(['scenario iteration: ', num2str(i_process)])
    end

    l = qd_layout(s);

    % base station
    l.tx_position(3) = 25;  % 25m base station height
    l.tx_array = qd_arrayant('3gpp-3D', bs_no_vertical_elements, bs_no_horizontal_elements, s.center_frequency, K);

    % mobile terminals
    % create a uniform linear array with dipole antennas
    l.rx_array = qd_arrayant('omni');
    l.rx_array.no_elements = ms_no_horizontal_elements;
    for i = 1:l.rx_array.no_elements
        l.rx_array.element_position(:, i) = [(i-1)*s.wavelength/2; 0; 0];
    end
    l.no_rx = no_of_UEs_outdoor;

    % create initial user positions and track their street indices
    [Mat_out, st_indices] = generate_outdoor_user_positions(no_of_UEs_outdoor, a_streets, b_streets, min_dist_to_BS, max_dist_to_BS, sector_anglespread, n_streets);
    [Mat_in, indoor_indices] = generate_indoor_user_positions(no_of_UEs_indoor, indoor_centers, min_dist_to_BS, max_dist_to_BS, sector_anglespread, n_indoor_centers);
    Mat = [Mat_out;Mat_in];
    l.rx_position = Mat';

    % create trajectories
    l = create_outdoor_trajectories(l, no_of_UEs_outdoor, dir_streets, st_indices, v_max_outdoor, v_min_outdoor, duration_per_slot, n_slots, symbol_duration, i_process)
    l = create_indoor_trajectories(l, no_of_UEs_outdoor, no_of_UEs_perScenario, v_max_indoor, duration_per_slot, n_slots, symbol_duration, i_process)

    % set scenario
    indoor_rx = l.set_scenario('3GPP_38.901_UMa',1:no_of_UEs_outdoor,[],0.0);
    if no_of_UEs_indoor > 0
        indoor_rx = l.set_scenario('3GPP_38.901_UMa_NLOS_O2I',no_of_UEs_outdoor+1:no_of_UEs_perScenario,[],1.0);
    end

    % plot the scenario
    %if i_process == 1
    %    [B1, B2, B3, B4] = compute_sector_boundaries(min_dist_to_BS, max_dist_to_BS, sector_anglespread);
    %    plot_scenario(Mat_out(1:min(300,length(Mat_out)),:), Mat_in(1:min(100,length(Mat_in)),:), B1, B2, B3, B4, l);
    %end
    disp('generate channels')
    % generate channel coefficients
    [h_channel, h_builder] = l.get_channels();
    h_channel.swap_tx_rx();

    H = cell(l.no_rx, 1);
    no_los = 0;
    no_nlos = 0;
    powers_all = zeros(l.no_rx, 1);
    H_per = zeros(l.no_rx,bs_mult,ms_mult,carriers,n_slots*n_symbols);
    for ms = 1:l.no_rx

        % transform channel to frequency domain
        chan = h_channel(ms).fr(bandwidth, carriers,1:n_slots*n_symbols);
        H{ms}.channel = chan;
        
        % MS position
        H{ms}.pos = h_channel(ms).rx_position;
        % find MS scenario (LOS vs. NLOS)
        if strfind(l.rx_track(ms).scenario{1}, 'NLOS')
            H{ms}.los = 0;
            no_nlos = no_nlos + 1;
        else
            H{ms}.los = 1;
            no_los = no_los + 1;
        end
        H{ms}.pg = h_channel(ms).par.pg_parset;
        
        %Normalizing path loss (see docu p.204)
        norm_factor = sqrt(10^(0.1*H{ms}.pg));
        H{ms}.channel = H{ms}.channel ./ norm_factor;
        chan_vect = H{ms}.channel(:);
        overall_norm2 = overall_norm2 + norm(chan_vect)^2;
        
        H_per(ms,:,:,:,:) = H{ms}.channel;
    end

    H_4d(i_process,:,:,:,:,:) = H_per;
    
end

clear chan;

%Normalization factor for the whole dataset:
overall_norm2 = sqrt(overall_norm2 / (no_of_UEs_perScenario) / rep_factor);
H_all = zeros(rep_factor*no_of_UEs_perScenario,bs_mult,ms_mult,carriers,n_slots*n_symbols);
count = 1;
for iter=1:rep_factor
    for n_ue=1:no_of_UEs_perScenario
        H_all(count,:,:,:,:) = sqrt(bs_mult*ms_mult*carriers*n_slots*n_symbols)*H_4d(iter,n_ue,:,:,:,:) ./ overall_norm2;
        count = count + 1;
    end
end
clear H_4d; 

% permute randomly
idx = randperm(rep_factor * no_of_UEs_perScenario);
H_all = H_all(idx, :, :, :, :);

%pre-processing
H_all_urban = squeeze(H_all);
ofdm_channel_real = real(H_all_urban);
ofdm_channel_imag = imag(H_all_urban);

% save data
num_samples_char = char(string(no_of_UEs_perScenario));

path = join(['../ofdm_quadriga_urban_', num_samples_char]);
save(path, 'ofdm_channel_real', 'ofdm_channel_imag', '-v7.3');
