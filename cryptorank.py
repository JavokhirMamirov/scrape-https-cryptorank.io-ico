import requests
import xlsxwriter
from bs4 import BeautifulSoup
import concurrent.futures

url = "https://api.cryptorank.io/v0/coins?locale=en"
user_url = "https://api.cryptorank.io/v0/coins/{key}?locale=en"


def extract_data(dt):
    try:
        res1 = requests.get(user_url.format(key=dt['key']))
        if res1.ok:
            user_dt = res1.json()

            coin = user_dt['data']
            try:
                rise = coin['crowdsales'][0]['raise']['USD']
            except:
                rise = 0
            try:
                soup = BeautifulSoup(coin['description'], 'html.parser')
                desc = soup.text
            except:
                desc = ""

            data = {
                "name": coin['name'],
                "description": desc,
                "discord": coin['links'][2]['value'],
                "twitter": coin['links'][1]['value'],
                "website": coin['links'][0]['value'],
                "rise": rise
            }
            return data
        else:
            return None
    except:
        return None


def main():
    print("Data extracting ... ")
    res = requests.get(url)
    if res.ok:
        data = res.json()
        data = data['data']
        workbook = xlsxwriter.Workbook('report.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'name')
        worksheet.write(0, 1, 'description')
        worksheet.write(0, 2, 'discord')
        worksheet.write(0, 3, 'twitter')
        worksheet.write(0, 4, 'website')
        worksheet.write(0, 5, 'total rised')
        i = 1
        written_data = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(extract_data, dt): dt for dt in data}
            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    if data is not None and data not in written_data:
                        written_data.append(data)
                        worksheet.write(i, 0, data['name'])
                        worksheet.write(i, 1, data['description'])
                        worksheet.write(i, 2, data['discord'])
                        worksheet.write(i, 3, data['twitter'])
                        worksheet.write(i, 4, data['website'])
                        worksheet.write(i, 5, data['rise'])
                        i += 1
                except Exception as err:
                    pass


        workbook.close()


if __name__ == '__main__':
    main()
