% Determine where this file's folder is.
folder = fileparts(which(matlab.desktop.editor.getActiveFilename));
% Add that folder plus all subfolders to the path.
addpath(genpath(folder));