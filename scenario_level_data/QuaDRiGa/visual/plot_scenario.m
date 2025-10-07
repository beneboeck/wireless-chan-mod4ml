function plot_scenario(Mat, Mat_in, B1, B2, B3, B4, l)

    fig = figure;
    set(fig, 'Units', 'inches', 'Position', [1 1 4.2 3]);
    MatLOS = [];
    MatNLOS = [];
    for ms = 1:min(300,length(Mat))
        % find MS scenario (LOS vs. NLOS)
        if strfind(l.rx_track(ms).scenario{1}, 'NLOS')
            MatNLOS = [MatNLOS;Mat(ms,1),Mat(ms,2)];
        else
            MatLOS = [MatLOS;Mat(ms,1),Mat(ms,2)];
        end
    end

    set(groot, 'defaultTextInterpreter', 'latex');
    scatter(0, 0, 100, 'MarkerEdgeColor', 'r', 'Marker', 'x', 'LineWidth', 1.5);
    %scatter([0],[0],16,[0.6350 0.0780 0.1840],'filled')
    hold on;
    if length(MatNLOS) > 0
        scatter(MatNLOS(:,1), MatNLOS(:,2), 20, 'b', 'LineWidth', 1);   % scatter plot for B
        hold on;
    end
    scatter(MatLOS(:,1), MatLOS(:,2), 20, 'c', '^', 'LineWidth', 1);
    hold on;
    if length(Mat_in) > 0
        scatter(Mat_in(:,1), Mat_in(:,2), 20, 'g', 'LineWidth', 1);   % scatter plot for B
        hold on;
    end
    plot(B1(:,1), B1(:,2), 'Color', 'k', 'LineStyle', '--', 'LineWidth', 1.5); % connect A with red lines
    hold on;
    plot(B2(:,1), B2(:,2), 'Color', 'k', 'LineStyle', '--', 'LineWidth', 1.5); % connect A with red lines
    hold on;
    plot(B3(:,1), B3(:,2), 'Color', 'k', 'LineStyle', '--', 'LineWidth', 1.5); % connect A with red lines
    hold on;
    plot(B4(:,1), B4(:,2), 'Color', 'k', 'LineStyle', '--', 'LineWidth', 1.5); % connect A with red lines
    hold on;
    xlabel('x-coord in [m]', 'Interpreter', 'latex', 'FontSize', 14);
    ylabel('y-coord in [m]', 'Interpreter', 'latex', 'FontSize', 14);
    yticks([-500 -250 0 250 500]);
    if (length(Mat_in)) > 0 & (length(MatNLOS) > 0) 
        lgd = legend('Access Point', 'NLOS Users', 'LOS Users', 'Indoor Users','Sector');
    elseif length(MatNLOS) > 0
        lgd = legend('Access Point', 'NLOS Users', 'LOS Users','Sector');
    else 
        lgd = legend('Access Point', 'LOS Users','Sector');
    end
    set(lgd, 'Units', 'normalized');
    set(lgd, 'Position', [0.75, 0.8, 0.15, 0.1]);
    ax = gca;
    ax.FontSize = 10;
    grid on;
    exportgraphics(fig, '../../../data/QuaDRiGa/scenario_urban_60000.png', 'ContentType', 'image', 'Resolution', 300);
    %saveas(fig, '../../../data/QuaDRiGa/scenario_urban_60000.png');
end