function [a_streets, b_streets, dir_streets, indoor_centers] = generate_streets_and_indoor_centers(min_dist, max_dist, sector_anglespread, n_streets, n_indoor_centers)
    
    % This function generates the streets and indoor centers in the desired
    % scenario

    %Inputs:
    % min_dist:             -minimum distance to the BS
    % max_dist:             -maximum distance to the BS
    % sector_anglespread:   -the angular spread of the desired sector
    % n_streets:            -number of considered streets
    % n_indoor_centers:     -number of indoor user clusters

    %Outputs:
    % a_streets: the slope of the streets from a bird perspective (y = a*x + b)
    % b_streets: the offset of the streets from a bird perspective (y = a*x + b)
    % dir_streets: the directions of the street in rad
    % indoor_centers: x and y coordinates of the indoor user clusters
 
    dist_indoor_street = 20; % the minimum distance between the indoor centers and the streets
    
    % randomly sample 2 distances and angles of two anchor point of each street (the anchor points serve as reference points through which the street definitely has to go through)
    r_streets = (max_dist - min_dist) * rand(2,n_streets) + min_dist;
    angle_streets = sector_anglespread * (rand(2,n_streets) - 0.5);
    x_streets = r_streets .* cos(angle_streets);
    y_streets = r_streets .* sin(angle_streets);

    % compute the corresponding a and b for each street if the street is defined as y = a * x + b
    a_streets = (y_streets(1,:) - y_streets(2,:))./(x_streets(1,:) - x_streets(2,:));
    b_streets = y_streets(1,:) - a_streets .* x_streets(1,:);
    dir_streets = atan(a_streets);

    % compute centers of the indoor users (at least dist_indoor_street meters distance to any street)
    indoor_centers = zeros(n_indoor_centers,2);
    for n = [1:n_indoor_centers]
        distance_enough = false;
        while distance_enough == false
            % compute x and y of a potential indoor center
            r_center = (max_dist - min_dist) * rand(1) + min_dist;
            angle_center = sector_anglespread * (rand(1) - 0.5);
            x_center = r_center .* cos(angle_center);
            y_center = r_center .* sin(angle_center);
        
            % iterate through all streets and check if distance of 15 meters is fulfilled
            for j = [1:n_streets]
                dis = abs(y_center - a_streets(j) * x_center - b_streets(j))/sqrt(a_streets(j)^2 + 1);
                if dis < dist_indoor_street
                    distance_enough = false;
                    break
                else
                    distance_enough = true;
                end
            end
        end
        indoor_centers(n,:) = [x_center,y_center];
    end
end