import requests
import json
import csv
import argparse
import colorama


def get_api(link):
    with requests.get(link) as response:
        source = json.loads(response.text)

    with open('public-api.json', 'w') as f_source:
        json.dump(source, f_source, indent=2)


def no_auth_apis():
    with open('public-api.json') as j_source:
        source = json.load(j_source)
    
    with open('no-auth.csv', 'w') as f:
        headers = ['Link', 'API', 'HTTPS', 'Cors', 'Category']
        write = csv.writer(f, dialect='excel')
        write.writerow(headers)

        for index, auths in enumerate(source['entries'], start=1):
            no_auth_data = []
            if auths['Auth'] == 'No' or auths['Auth'] == '':
                no_auth_data.extend((auths['Link'], auths['API'],
                        auths['HTTPS'], auths['Cors'], auths['Category']))
                print(f"No Authentication: {auths['API']}")
                write.writerows([no_auth_data])


def apis():
    with open('public-api.json') as j_source:
        source = json.load(j_source)

    print(f"Total APIs: {source['count']}")
    with open('All-APIs.csv', 'w') as f:
        headers = ['#', 'Link', 'API', 'Auth', 'HTTPS', 'Cors', 'Category']
        writer = csv.writer(f, dialect='excel')
        writer.writerow(headers)

        for index, apis in enumerate(source['entries'], start=1):
            data = [index, apis['Link'], apis['API'], apis['Auth'],
                    apis['HTTPS'], apis['Cors'], apis['Category']]
            writer.writerows([data])


if __name__ == '__main__':
    colorama.init()
    get_api('https://api.publicapis.org/entries')    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                    description="Lists APIs")

    parser.add_argument('-na', '--noauth',
                        metavar='NOAUTH',
                        help="Gets APIs that require no Authentication.")
    
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help="Lists down all APIs.")

    args = parser.parse_args()

    if args.noauth:
        no_auth_apis()

    if args.all:
        apis()