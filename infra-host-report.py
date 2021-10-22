import os
import csv
from python_graphql_client import GraphqlClient

# Required to fetch paginated entities beyond the default limit of 20.
TEMPLATED_CURSOR_QUERY = """
{
  actor {
    entitySearch(queryBuilder: {domain: INFRA, type: HOST}) {
      results<CURSOR_STATEMENT> {
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
        nextCursor
      }
      count
    }
  }
}
"""

account_host_dict = {}
official_count = None
def get_host_metadata():
    global official_count
    official_count = None
    headers = {}
    headers['Api-Key'] = os.getenv('USER_API_KEY')
    headers['Content-Type'] = 'application/json'
    client = GraphqlClient(endpoint="https://api.newrelic.com/graphql")
    client.headers=headers
    query = TEMPLATED_CURSOR_QUERY.replace("<CURSOR_STATEMENT>", '')
    results = []
    cursor = query
    while cursor:
        _result = client.execute(query=cursor)
        if not official_count:
            official_count = _result['data']['actor']['entitySearch']['count']
        results += [data for data in _result['data']['actor']['entitySearch']['results']['entities']]
        cursor_hash = _result['data']['actor']['entitySearch']['results']['nextCursor']
        if cursor_hash:
            cursor = TEMPLATED_CURSOR_QUERY.replace("<CURSOR_STATEMENT>", '(cursor: "{}")'.format(cursor_hash))
        if (len(results) == official_count):
            cursor = None

    key_set = set()
    host_objects = []
    counter = 0
    for item in results:
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
    
    return (account_host_dict, host_objects, key_set)




def write_csv(host_objects, key_set):
    with open('infra-host-report.csv', 'w') as f:
        w = csv.DictWriter(f, key_set, extrasaction='ignore')
        w.writeheader()
        w.writerows(host_objects)

def report_to_stdout(account_host_dict, host_objects, official_count):
    if (official_count > len(host_objects)):
        print("Warning this report is based on a truncated graphql response! Only showing {} out of {} entities!".format(counter, official_count))
    print("###### Report Summary ##########")
    print("Number of Accounts: {}".format(len(account_host_dict.keys())))
    print("Total Number of Hosts: {}".format(len(host_objects)))
    print("###### Account Breakdown #######")
    for account, host_count in account_host_dict.items():
        print("{}: {}".format(account, host_count))



def main():
    account_host_dict, host_objects, key_set = get_host_metadata()
    write_csv(host_objects, key_set)
    report_to_stdout(account_host_dict, host_objects, official_count)

if __name__ == '__main__':
    main()