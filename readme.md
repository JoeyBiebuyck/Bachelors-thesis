# Website logic:
The website logic is in websites/websitename/homepage/views.py

# Bandit
The bandit is defined in bandits/XSS_bandit.py

# Website launching
The website launching is defined in start_server.py

# How to run:
python run_atlucb_xss.py -s 1 -t 100 -m 5

# How to export to .csv:
python run_atlucb_xss.py -s 1 -t 100 -m 5 | tr ' ' ',' > results/Firstoutput.csv

# How to postprocess .csv:
python postprocess.py -c atlucb_top5_1k.csv -s min -m 5

# How to do experiments with plots:
Run the script file of the bandit you want to experiment with, with the parameters specified inside of the file
