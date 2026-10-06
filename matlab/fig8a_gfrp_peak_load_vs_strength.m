%% fig8a_gfrp_peak_load_vs_strength.m
% Fig. 8a of Bond_RB_GFRP_manuscript_v8:
% peak pull-out load of cast-in GFRP bars against nominal concrete strength,
% one curve per bar diameter, with the pooled mean +/- 1 SD band at f'c >= 14.7 MPa.
%
% DATA SOURCE (nothing is simulated, fitted or smoothed):
%   - Table 10 of the manuscript: peak load P, mean (SD) in kN, n = 5 specimens per group.
%   - Section 3.6 of the manuscript: pooled peak load at 14.7 and 23.5 MPa = 20.8 +/- 2.7 kN (n = 30).
%
% Run in MATLAB R2020a or newer (needs exportgraphics; older releases fall back to print).
% After running, the figure is saved next to this script and the MATLAB version is printed;
% quote that version in the paper (see the suggested sentence at the end of this file).

clear; clc; close all;

%% 1. Data transcribed from Table 10 (rows: 6, 9, 12 mm; columns: 4.9, 14.7, 23.5 MPa)
fc = [4.9 14.7 23.5];            % nominal concrete strength, MPa
db = [6 9 12];                   % bar diameter, mm
Pm = [11.1 21.4 17.9;            % mean peak load, kN
      14.5 20.8 19.1;
      15.3 21.7 23.8];
Ps = [ 0.2  0.7  2.6;            % sample standard deviation, kN
       0.4  0.7  3.6;
       0.6  1.6  1.3];
n  = 5;                          % specimens per group

%% 2. Consistency checks against the numbers quoted in the text (stop if they disagree)
upper = Pm(:, 2:3);                                    % groups at 14.7 and 23.5 MPa
pooledMean = mean(upper(:));
M   = numel(upper);                                    % 6 groups -> 30 specimens
ssWithin  = sum((n - 1) * reshape(Ps(:, 2:3), [], 1).^2);
ssBetween = sum(n * (upper(:) - pooledMean).^2);
pooledSD  = sqrt((ssWithin + ssBetween) / (M * n - 1));
bandMean = 20.8;  bandSD = 2.7;                        % values reported in Section 3.6
assert(abs(pooledMean - bandMean) < 0.05, 'pooled mean differs from the reported 20.8 kN');
assert(abs(pooledSD   - bandSD)   < 0.10, 'pooled SD differs from the reported 2.7 kN');
fprintf('Pooled mean = %.2f kN (reported %.1f); pooled SD = %.2f kN (reported %.1f)\n', ...
        pooledMean, bandMean, pooledSD, bandSD);

%% 3. Style (muted, print-safe palette; thin lines; no top/right box)
col  = [0.290 0.314 0.345;       % 6 mm  - slate
        0.239 0.416 0.541;       % 9 mm  - steel blue
        0.612 0.478 0.322];      % 12 mm - warm brown
mark = {'o', 's', '^'};
dx   = [-0.35 0 0.35];           % small horizontal offsets for legibility only (MPa)
bandColor = [0.90 0.91 0.93];

fig = figure('Units', 'centimeters', 'Position', [2 2 9.0 7.0], 'Color', 'w');
ax  = axes(fig); hold(ax, 'on');
set(ax, 'FontName', 'Arial', 'FontSize', 9, 'LineWidth', 1.0, 'Box', 'off', ...
        'TickDir', 'out', 'XColor', [0.1 0.1 0.1], 'YColor', [0.1 0.1 0.1], ...
        'YGrid', 'on', 'GridColor', [0.85 0.85 0.83], 'GridAlpha', 1, 'Layer', 'bottom');

%% 4. Pooled mean +/- 1 SD band and mean line
xl = [11.6 26];
patch(ax, [xl(1) xl(2) xl(2) xl(1)], bandMean + bandSD * [-1 -1 1 1], bandColor, ...
      'EdgeColor', 'none', 'HandleVisibility', 'off');
plot(ax, [xl(1) xl(2)], [bandMean bandMean], ':', 'Color', [0.3 0.3 0.3], ...
     'LineWidth', 1.0, 'HandleVisibility', 'off');

%% 5. One curve per diameter: group mean +/- 1 SD
if exist('gobjects', 'file') ~= 0, h = gobjects(1, 3); else, h = zeros(1, 3); end   % MATLAB / Octave
for k = 1:3
    h(k) = errorbar(ax, fc + dx(k), Pm(k, :), Ps(k, :));
    set(h(k), 'LineStyle', '-', 'Marker', mark{k}, 'Color', col(k, :), 'MarkerFaceColor', col(k, :), ...
              'MarkerEdgeColor', col(k, :), 'MarkerSize', 5.5, 'LineWidth', 1.2);
    try, set(h(k), 'CapSize', 3); catch, end            % CapSize is not available in all releases
end

%% 6. Axes, labels, legend, annotation
set(ax, 'XLim', [2 26], 'YLim', [9 27.5], 'XTick', fc, 'YTick', 10:2.5:27.5);
xlabel(ax, 'Nominal concrete strength, f''_{c} (MPa)', 'FontName', 'Arial', 'FontSize', 9);
ylabel(ax, 'Peak pull-out load, P (kN)',            'FontName', 'Arial', 'FontSize', 9);
lg = legend(ax, h, {'6 mm', '9 mm', '12 mm'}, 'Location', 'southeast', 'Box', 'off', ...
            'FontName', 'Arial', 'FontSize', 8.5);
try, title(lg, 'Bar diameter'); catch, end
text(ax, 25.7, 27.0, {'Band: pooled mean \pm 1 SD at', 'f''_{c} \geq 14.7 MPa, 20.8 \pm 2.7 kN'}, ...
     'HorizontalAlignment', 'right', 'VerticalAlignment', 'top', ...
     'FontName', 'Arial', 'FontSize', 7.5, 'Color', [0.35 0.35 0.35]);

%% 7. Export (600 dpi raster + vector PDF) and record the MATLAB version used
isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;           % the file name must say which program drew the figure
if isOctave, suffix = '_OCTAVE_TEST_NOT_FOR_PUBLICATION'; else, suffix = '_MATLAB'; end
outfile = ['Fig8a_GFRP_peak_load_vs_strength' suffix];
if exist('exportgraphics', 'file') ~= 0
    exportgraphics(fig, [outfile '.png'], 'Resolution', 600);
    exportgraphics(fig, [outfile '.pdf'], 'ContentType', 'vector');
else
    print(fig, [outfile '.png'], '-dpng', '-r600');
end
v = ver('matlab');
if isempty(v), tool = 'GNU Octave (NOT MATLAB)'; else, tool = ['MATLAB ' v.Release ' (' v.Version ')']; end
fprintf('Figure written to %s.png using %s on %s\n', outfile, tool, datestr(now));

% Suggested wording for the manuscript (use it only after YOU have run this script in MATLAB):
%   "Figures were generated in MATLAB (R20xx, The MathWorks, Inc., Natick, MA, USA) from the
%    group means and standard deviations reported in Table 10."
