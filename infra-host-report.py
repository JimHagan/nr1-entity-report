import os
import csv
from python_graphql_client import GraphqlClient

account_host_dict = {}
official_count = 0
def get_host_metadata():
    global official_count
    headers = {}
    headers['Api-Key'] = os.getenv('USER_API_KEY')
    headers['Content-Type'] = 'application/json'
    client = GraphqlClient(endpoint="https://api.newrelic.com/graphql")
    client.headers=headers
    query = """
{
  actor {
    entitySearch(queryBuilder: {domain: INFRA, type: HOST}) {
      results {
        entities {
          tags {
            key
            values
          }
          guid
          name
          reporting
          permalink
          accountId
          account {
            id
            name
          }
          ... on InfrastructureHostEntityOutline {
            guid
            name
            domain
          }
        }
      }
      count
    }
  }
}





        """

    _result = client.execute(query=query)
    official_count = _result['data']['actor']['entitySearch']['count']
    return [data for data in _result['data']['actor']['entitySearch']['results']['entities']]


data = get_host_metadata()


key_set = set()
host_objects = []
counter = 0
for item in data:
    counter += 1
    scrubbed = {}
    for tag in item['tags']:
        scrubbed[tag['key']] = tag['values'][0]
    for k in scrubbed.keys():
        key_set.add(k)
    host_objects.append(scrubbed)
    account = scrubbed['account']
    if account in account_host_dict:
        account_host_dict[account]+=1
    else:
        account_host_dict[account] = 1



with open('infra-host-report.csv', 'w') as f:
    w = csv.DictWriter(f, key_set, extrasaction='ignore')
    w.writeheader()
    w.writerows(host_objects)


if (official_count > counter):
    print("Warning this report is based on a truncated graphql response! Only showing {} out of {} entities!".format(counter, official_count))
print("###### Report Summary ##########")
print("Number of Accounts: {}".format(len(account_host_dict.keys())))
print("Total Number of Hosts: {}".format(len(host_objects)))
print("###### Account Breakdown #######")
for account, host_count in account_host_dict.items():
    print("{}: {}".format(account, host_count))