function [Mat_in, indoor_indices] = generate_indoor_user_positions(no_of_UEs_indoor, indoor_centers, min_dist, max_dist, sector_angularspread, n_indoor_centers)

    % This function generates random positions of all users on the streets

    %Input:
    % min_dist:              -minimum distance to the BS
    % max_dist:             -maximum distance to the BS
    % sector_anglespread:   -the angular spread of the desired sector
    % no_of_UEs_indoor:    -number of users indoor
    % indoor_centers: x and y coordinates of the indoor user clusters
    % n_indoor_centers:     - number of indoor clusters

    %Output:
    % Mat_in:              -matrix with the positions of the outdoor users
    % indoor_indices:          -list of indices which user belongs to which center

    indoor_variance = 20; % the variance of the indoor users around their center

    Mat_in = zeros(no_of_UEs_indoor,3);
    Mat_in(:,3) = 1.5;
    indoor_indices = zeros(no_of_UEs_indoor,1);

    for n_user = 1:no_of_UEs_indoor
        indoor_index = randi([1,n_indoor_centers]);
        indoor_indices(n_user) = indoor_index;
        within_the_sector = false;
        % create until the position is within the sector
        while within_the_sector == false
            % compute x and y
            x = indoor_centers(indoor_index,1) + sqrt(indoor_variance) * randn(1);
            y = indoor_centers(indoor_index,2) + sqrt(indoor_variance) * randn(1);
            % test if within the sector
            r = hypot(x, y);
            theta = abs(atan2(y, x));
            in_range = (r > min_dist) && (r < max_dist) && (theta < sector_angularspread/2);
            if in_range
                within_the_sector = true;
                Mat_in(n_user,1) = x;
                Mat_in(n_user,2) = y;
            end
        end
    end
end