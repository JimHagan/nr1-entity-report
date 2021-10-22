# nr1-entity-report
Simple tool for extracting a report of all New Relic monitored entities avaiable to a user based on his user key.  Currently supports INFRA HOST, APM APPLICTION, and  BROWSER APPLICATION

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

There are currently three entity domains supported

- INFRA
- APM
- BROWSER
- MOBILE
- SYNTH

Let's run it with the INFRA domain.

```
python nr1-entity-report.py INFRA
```

You should see a nice summary of host counts broken down by account like so:

```
###### Report Summary ##########
Number of Accounts: 6
Total Number of Entities: 260
###### Account Breakdown #######
Video Demo: 4
Demotron V2: 78
GCP DEMO: 21
Demotron Rotate: 73
Demotron Distributed Tracing: 17
Demotron_CAS: 67
```

6. Explore and analyze the output file `nr1-entity-report.csv`