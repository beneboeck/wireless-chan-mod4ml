function layout = create_outdoor_trajectories(layout, no_of_UEs_outdoor, dir_streets, st_indices, v_max_outdoor, v_min_outdoor, duration_per_slot, n_slots, symbol_duration, i_process)

    % This function extends the corresponding tracks in the layout for all outdoor users with trajectories

    %Input:
    % layout: -the layout of interest with saved user positions
    % no_of_UEs_outdoor:    - number of users on the streets
    % dir_streets:          - the directions of the street in rad
    % st_indices:           - the street index assigned to each user
    % v_max_outdoor:        - maximal velocity of the outdoor users
    % v_min_outdoor:        - minimum velocity of the outdoor users
    % duration_per_slot:    - duration of one slot
    % n_slots:              - number of slots (typically simply 1)
    % symbol_duration:      - duration of one (OFDM) symbol
    % i_process:            - process index

    %Output:
    % layout: -the updated layout with the trajectories

    % create trajectories
    for i_track = 1:no_of_UEs_outdoor
        if mod(i_track,1000) == 0
            fprintf('outdoor, user index: %d\n', i_track);
        end
        % choice in which direction the users moves along the street
        dir_options = {dir_streets(st_indices(i_track)), dir_streets(st_indices(i_track)) + pi};
        phi_user = dir_options{randi(2)};
        veloc_rand = (v_max_outdoor - v_min_outdoor) / 3.6 * rand(1) + v_min_outdoor / 3.6;
        length_per_slot = duration_per_slot * veloc_rand;
        t = qd_track('linear',n_slots*length_per_slot,phi_user);
        t.name = sprintf('MS-%i-%i',i_process,i_track);
        t.initial_position = layout.rx_position(:,i_track);
        t.set_speed(veloc_rand) %terminal speed in m/s

        [~, layout.rx_track(:,i_track)] = interpolate(t.copy,'time',symbol_duration);
    end
end