function plot_scenario_rural(Mat_out, B1, B2, B3, B4)

    fig = figure;
    set(fig, 'Units', 'inches', 'Position', [1 1 4.2 3]);
    set(groot, 'defaultTextInterpreter', 'latex');
    scatter(0, 0, 100, 'MarkerEdgeColor', 'r', 'Marker', 'x', 'LineWidth', 1.5);
    %scatter([0],[0],16,[0.6350 0.0780 0.1840],'filled')
    hold on;
    scatter(Mat_out(:,1), Mat_out(:,2), 20, 'c', '^', 'LineWidth', 1);
    hold on;
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
    yticks([-3000 -2000 -1000 0 1000 2000 3000]);
    lgd = legend('Access Point', 'LOS Users','Sector');
    set(lgd, 'Units', 'normalized');
    set(lgd, 'Position', [0.75, 0.8, 0.15, 0.1]);
    ax = gca;
    ax.FontSize = 10;
    grid on;
    exportgraphics(fig, '../../../data/QuaDRiGa/scenario_rural_60000.png', 'ContentType', 'image', 'Resolution', 300);
    %saveas(fig, '../../../data/QuaDRiGa/scenario_rural_60000.png');
end