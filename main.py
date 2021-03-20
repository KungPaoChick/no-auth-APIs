import requests
import json
import csv


def get_api():
    with requests.get('https://api.publicapis.org/entries') as response:
        source = json.loads(response.text)

    with open('public-api.json', 'w') as f_source:
        json.dump(source, f_source, indent=2)


def no_auth_apis():
    with open('public-api.json') as j_source:
        source = json.load(j_source)

    print(f"Total API's: {source['count']}")
    
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


if __name__ == '__main__':
    get_api()
    no_auth_apis()
