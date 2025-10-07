function layout = create_indoor_trajectories(layout, no_of_UEs_outdoor, no_of_UEs_perScenario, v_max_indoor, duration_per_slot, n_slots, symbol_duration, i_process)

    % This function extends the corresponding tracks in the layout for all outdoor users with trajectories

    %Input:
    % layout: -the layout of interest with saved user positions
    % no_of_UEs_outdoor:    - number of users on the streets
    % no_of_UEs_perScenario:- total amount of users
    % v_max_indoor:        - maximal velocity of the indoor users
    % duration_per_slot:    - duration of one slot
    % n_slots:              - number of slots (typically simply 1)
    % symbol_duration:      - duration of one (OFDM) symbol
    % i_process:            - process index

    %Output:
    % layout: -the updated layout with the trajectories

    % create trajectories
    for i_track = no_of_UEs_outdoor+1:no_of_UEs_perScenario
        if mod(i_track,1000) == 0
            fprintf('indoor, user index: %d\n', i_track);
        end
        random_angle = rand(1)*2*pi;
        veloc_rand = v_max_indoor / 3.6 * rand(1);
        length_per_slot = duration_per_slot * veloc_rand;
        t = qd_track('linear',n_slots*length_per_slot,random_angle);
        t.name = sprintf('MS-%i-%i',i_process,i_track);
        t.initial_position = layout.rx_position(:,i_track);
        t.set_speed(veloc_rand) %terminal speed in m/s
        [~, layout.rx_track(:,i_track)] = interpolate(t.copy,'time',symbol_duration);
    end
end