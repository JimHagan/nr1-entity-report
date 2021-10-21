# infra-host-report
Simple tool for extracting a report of all HOST applications avaiable to a user based on his user key.

## Getting started

1. Clone the repository
2. CD into the repository directory
3. Create a Python 3 virtual environment, install dependencies, and activate it.

```
virtualenv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```

4. Set the USER_API_KEY environment variable 

```
export USER_API_KEY=A_NEW_RELIC_USER_API_KEY
```

5. Run the program

```
python infra-host-report.py
```

You should see a nice summary of host counts broken down by account like so:

```
###### Report Summary ##########
Number of Accounts: 6
Total Number of Hosts: 200
###### Account Breakdown #######
Video Demo: 1
Demotron V2: 65
GCP DEMO: 34
Demotron Rotate: 60
Demotron Distributed Tracing: 11
Demotron_CAS: 29
```

6. Explore and analyze the output file `infra-host-report.csv`