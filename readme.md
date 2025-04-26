# website logic:
The website logic is in websitename/homepage/views.py

# bandit
The bandit is defined in XSS_bandit.py

# Website launching
The website launching is defined in start_server.py
z

# how to run:
python run_atlucb_xss.py -s 1 -t 100 -m 5

# how to export to .csv:
python run_atlucb_xss.py -s 1 -t 100 -m 5 | tr ' ' ',' > results/Firstoutput.csv