# Identifying the m-top best XSS payload transformations
This repository has the code used for my bachelors thesis.

## About
This repository contains a framework to identify the most effective XSS payload transformations. To be used in practice the code must be adapted for the specific use case, but this repository contains everything that was used to test the effectiveness of this approach. The bfts folder is a clone of the https://github.com/plibin/bfts repository.

There are two bandits, the Bernoulli bandit and the XSS bandit. The Bernoulli bandit is a bandit where each arm has a unique underlying Bernoulli reward distribution. The XSS bandit is used to test the effectiveness of a set of XSS payload transformations. To change the payload transformations used by the bandit, the XSS_bandit.py file in the bandits folder must be edited. Running an experiment can be done using the run_atlucb_*.py, run_bfts_*.py, or run_uniform_*.py files. To take into account randomness the generate_and_process.sh files can be used to run many experiments on the same parameters with different seeds. These script files also automatically combine each individual experiment's data and plot the graphs of the requested statistics.

Below is information about where changes need to be made to alter certain behaviour.

### Website logic:
The website logic is in websites/websitename/homepage/views.py

### Bandit
The bandits are defined in bandits/

### Website launching
Websites must be launched prior to starting an XSS bandit experiment. Any additional websites must be created manually.
The website launching is defined in start_server.py

### How to run:
python run_atlucb_xss.py -s 1 -t 100 -m 5

### How to export to .csv:
python run_atlucb_xss.py -s 1 -t 100 -m 5 | tr ' ' ',' > results/Firstoutput.csv

### How to postprocess .csv:
python postprocess.py -c atlucb_top5_1k.csv -s min -m 5

### How to do experiments with plots:
Run the script file of the bandit you want to experiment with, with the parameters specified inside of the file
