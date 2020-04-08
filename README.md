# Part-II-Project

[![Build Status](https://travis-ci.org/codebyzeb/Part-II-Project.svg?branch=master)](https://travis-ci.org/ZGoriely/Part-II-Project)

This repository contains the code and the dissertation for my Part II Project at the University of Cambridge.

## Installation

This project is written entirely in Python, so simply download or clone the repository!

## Dissertation

The dissertation is located at `docs/Dissertation/diss.pdf`. This is the marked document that corresponded to 25% of my third-year grade and contains all the information about this project.

## Running a Simulation

The code for running a simulation can be found in the `simulating` module. While in the main repository, simply enter the following to bring up the help menu for the command line interface:

`python3 -m simulating.simulation -h`

This will print out all of the in-place and optional parameters used to run a simulation. A basic simulation in interactive mode can be run default parameters by just providing a language type and a folder name (where results are stored):

 `python3 -m simulating.simulation None testing -i`
 
 ## Plotting Results
 
 The `analysis` module contains code to plot various figures. To display fitness graphs, language frequency and QI correlation, use the `plotting` module:
 
 `python3 -m analysis.plotting -h`
 
 To display heatmaps for individual neural networks or populations of neural networks, use the `heatmap` module:
 
  `python3 -m analysis.heatmap -h`
