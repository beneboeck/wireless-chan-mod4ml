function [Mat_out, st_indices] = generate_outdoor_user_positions(no_of_UEs_outdoor, a_streets, b_streets, min_dist, max_dist, sector_angularspread, n_streets)

    % This function generates random positions of all users on the streets

    %Input:
    % min_dist:              -minimum distance to the BS
    % max_dist:             -maximum distance to the BS
    % sector_anglespread:   -the angular spread of the desired sector
    % no_of_UEs_outdoor:    -number of users on the streets
    % a_streets:            -the slope of the streets from a bird perspective (y = a*x + b)
    % b_streets:            -the offset of the streets from a bird perspective (y = a*x + b)
    % dir_streets:          -the directions of the street in rad
    % n_strets:             -number of streets

    %Output:
    % Mat_out:              -matrix with the positions of the outdoor users
    % st_indicies:          -list of indices which user belongs to which streets

    % compute the minimal and maximal existing x coordinate in the sector (is important for the sampling later on)
    x_min_uni = cos(sector_angularspread/2) * min_dist;
    x_max_uni = max_dist;

    Mat_out = zeros(no_of_UEs_outdoor,3);
    Mat_out(:,3) = 1.5;
    st_indices = zeros(no_of_UEs_outdoor,1);

    for n_user = 1:no_of_UEs_outdoor
        street_index = randi([1,n_streets]);
        st_indices(n_user) = street_index;
        within_the_sector = false;
        % create until the position is within the sector
        while within_the_sector == false
            % compute x and y
            x = (x_max_uni - x_min_uni) * rand(1) + x_min_uni;
            y = a_streets(street_index) * x + b_streets(street_index) + 3 * randn(1);
            % test if within the sector
            r = hypot(x, y);
            theta = abs(atan2(y, x));
            in_range = (r > min_dist) && (r < max_dist) && (theta < sector_angularspread/2);
            if in_range
                within_the_sector = true;
                Mat_out(n_user,1) = x;
                Mat_out(n_user,2) = y;
            end
        end
    end
end