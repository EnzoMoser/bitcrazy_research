% 
%
% You can run this script to run all tests consecutively.
%
%

% Useful commands:
clear           % Clear all variables
clc             % Clear the command window
close all       % Close all figures

% Add all subfolders to path first:
add_all_files_to_path;

% Reset the RNG (Uncomment for variation):
rng(0,'twister');

TEST_1_create_lines; 
TEST_3_scan_area;
TEST_4_bfs_path;

TEST_2_cycle_lights;    % This script was made to loop.