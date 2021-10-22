import argparse
import csv
import os

from python_graphql_client import GraphqlClient

ENTITY_MAPPING = {
    'APM': {'DOMAIN': 'APM',
            'TYPE': 'APPLICATION',
            'MODEL': 'ApmApplicationEntityOutline'},
    'INFRA': {'DOMAIN': 'INFRA',
              'TYPE': 'HOST',
              'MODEL': 'InfrastructureHostEntityOutline'},
    'BROWSER': {'DOMAIN': 'BROWSER',
                'TYPE': 'APPLICATION',
                'MODEL': 'BrowserApplicationEntityOutline'},
    'MOBILE': {'DOMAIN': 'MOBILE',
                'TYPE': 'APPLICATION',
                'MODEL': 'MobileApplicationEntityOutline'},
    'SYNTH': {'DOMAIN': 'SYNTH',
                'TYPE': 'MONITOR',
                'MODEL': 'SyntheticMonitorEntityOutline'},
}

# Required to fetch paginated entities beyond the default limit of 20.
TEMPLATED_CURSOR_QUERY = """
{
  actor {
    entitySearch(queryBuilder: {domain: <ENTITIY_DOMAIN>, type: <ENTITY_TYPE>}) {
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
          ... on <ENTITY_MODEL> {
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

def get_entity_metadata(entity_domain):
    official_count = None
    account_entity_dict = {}
    headers = {}
    headers['Api-Key'] = os.getenv('USER_API_KEY')
    headers['Content-Type'] = 'application/json'
    client = GraphqlClient(endpoint="https://api.newrelic.com/graphql")
    client.headers=headers
    query = TEMPLATED_CURSOR_QUERY.replace("<CURSOR_STATEMENT>", '')
    query = query.replace("<ENTITIY_DOMAIN>", ENTITY_MAPPING[entity_domain]['DOMAIN'])
    query = query.replace("<ENTITY_TYPE>", ENTITY_MAPPING[entity_domain]['TYPE'])
    query = query.replace("<ENTITY_MODEL>", ENTITY_MAPPING[entity_domain]['MODEL'])
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
            cursor = cursor.replace("<ENTITIY_DOMAIN>", ENTITY_MAPPING[entity_domain]['DOMAIN'])
            cursor = cursor.replace("<ENTITY_TYPE>", ENTITY_MAPPING[entity_domain]['TYPE'])
            cursor = cursor.replace("<ENTITY_MODEL>", ENTITY_MAPPING[entity_domain]['MODEL'])
        if (len(results) == official_count):
            cursor = None

    key_set = set()
    entity_objects = []
    counter = 0
    for item in results:
        counter += 1
        scrubbed = {}
        for tag in item['tags']:
            scrubbed[tag['key']] = tag['values'][0]
        for k in scrubbed.keys():
            key_set.add(k)
        entity_objects.append(scrubbed)
        account = scrubbed['account']
        if account in account_entity_dict:
            account_entity_dict[account]+=1
        else:
            account_entity_dict[account] = 1
    
    return (account_entity_dict, entity_objects, key_set, official_count)




def write_csv(entity_objects, key_set):
    with open('nr1-entity-report.csv', 'w') as f:
        w = csv.DictWriter(f, key_set, extrasaction='ignore')
        w.writeheader()
        w.writerows(entity_objects)

def report_to_stdout(account_entity_dict, entity_objects, official_count, entity_domain):
    if (official_count > len(entity_objects)):
        print("Warning this report is based on a truncated graphql response! Only showing {} out of {} entities!".format(counter, official_count))
    print("###### Report Summary ##########")
    print("Entity Domain: {}".format(entity_domain))
    print("Number of Accounts: {}".format(len(account_entity_dict.keys())))
    print("Total Number of Entities: {}".format(len(entity_objects)))
    print("###### Account Breakdown #######")
    for account, entity_count in account_entity_dict.items():
        print("{}: {}".format(account, entity_count))



def main():
    parser = argparse.ArgumentParser(description='Extract NR1 entitity report from Nergraph.')
    parser.add_argument('entity_domain', choices=ENTITY_MAPPING.keys())
    args = parser.parse_args()
    entity_domain = args.entity_domain
    account_entity_dict, entity_objects, key_set, official_count = get_entity_metadata(entity_domain)
    write_csv(entity_objects, key_set)
    report_to_stdout(account_entity_dict, entity_objects, official_count, entity_domain)

if __name__ == '__main__':
    main()