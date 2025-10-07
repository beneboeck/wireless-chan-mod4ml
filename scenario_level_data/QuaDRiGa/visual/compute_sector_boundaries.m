function [B1, B2, B3, B4] = compute_sector_boundaries(min_dist, max_dist, sector_anglespread)
    
    % This function computes samples along the sector boundaries and
    % divides them in four arrays for each section each

    % Inputs:
    % min_dist:             -minimum distance to the BS
    % max_dist:             -maximum distance to the BS
    % sector_anglespread:   -the angular spread of the desired sector

    % Outputs:
    % B1, B2, B3, B4:       -four arrays with samples along the sections of the sector boundaries

    % create samples along the scenario boundaries
    theta = sector_anglespread * linspace(-0.5, 0.5, 101);  % 0.01 steps
    r_edge = linspace(min_dist, max_dist, 11);  % 0.1 steps
    r_inner = linspace(min_dist, max_dist, 101); % 0.01 steps
    angle_half = sector_anglespread / 2;

    % Arcs
    B1 = [min_dist * cos(theta)', min_dist * sin(theta)'];
    B3 = [max_dist * cos(theta)', max_dist * sin(theta)'];

    % Radial edges
    B2 = [r_edge' * cos(angle_half), r_edge' * sin(angle_half)];
    B4 = [r_inner' * cos(-angle_half), r_inner' * sin(-angle_half)];
end