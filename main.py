import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import xlsxwriter

URL1 = "https://cryptorank.io/ico"
URL2 = "https://cryptorank.io/active-ico"
URL3 = "https://cryptorank.io/upcoming-ico"


def main():
    browser = webdriver.Chrome()
    workbook = xlsxwriter.Workbook('report.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'name')
    worksheet.write(0, 1, 'description')
    worksheet.write(0, 2, 'discord')
    worksheet.write(0, 3, 'twitter')
    worksheet.write(0, 4, 'website')
    worksheet.write(0, 5, 'total rised')
    res = browser.get(URL1)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    games = soup.find_all('a', attrs={'class': 'table-coin-link__StyledLink-sc-pprt06-6 bLZygE'}, limit=10)
    i = 1
    for game in games:
        link = f"https://cryptorank.io{game['href']}"
        res = browser.get(link)
        html = browser.page_source
        soup1 = BeautifulSoup(html, 'lxml')
        name = soup1.find('h2', attrs={'class': 'coin-info__name'})
        if name is not None:
            name = name.text
        else:
            name = ""

        desc = soup1.find('div', attrs={'class': 'styled__CoinInfoDescription-sc-1iy13vh-2 dcSreG'})
        if desc is not None:
            desc = desc.text
        else:
            desc = ""

        total_rises_div = soup1.find_all('div', attrs={'class': 'styled__IcoColumn-sc-19xalay-4 kElqSx'})
        total_rised = ""
        for div in total_rises_div:
            if div.find('h4') is not None:
                if div.find('h4').text == "Raise":
                    if div.find('p') is not None:
                        total_rised = div.find('p').text


        web = soup1.find('a', attrs={'title': 'web'})
        if web is not None:
            web = web['href']
        else:
            web = ""

        twitter = soup1.find('a', attrs={'title': 'web'})
        if twitter is not None:
            twitter = twitter['href']
        else:
            twitter = ""

        discord = soup1.find('a', attrs={'title': 'web'})
        if discord is not None:
            discord = discord['href']
        else:
            discord = ""

        # whitepaper = soup1.find('a', attrs={'title': 'web'})
        # if whitepaper is not None:
        #     whitepaper = whitepaper['href']
        # else:
        #     whitepaper = ""

        worksheet.write(i, 0, name)
        worksheet.write(i, 1, desc)
        worksheet.write(i, 2, discord)
        worksheet.write(i, 3, twitter)
        worksheet.write(i, 4, web)
        worksheet.write(i, 5, total_rised)

        i += 1

    workbook.close()

if __name__ == '__main__':
    main()
