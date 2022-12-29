import pandas as pd
import requests
import xml.etree.ElementTree as ET

class ProcessCurrencies:
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.df = pd.read_csv(file_name)
        self.min_date = self.df['published_at'].min()
        self.max_date = self.df['published_at'].max()
        self.currencies_to_convert = None
        self.__currencies_data = None

    def generate_currency(self, start_date: str, finish_date: str) -> None:
        first_year = int(start_date[:4])
        first_month = int(start_date[5:7])
        last_year = int(finish_date[:4])
        last_month = int(finish_date[5:7])
        dataf = pd.DataFrame(columns=['date'] + self.currencies_to_convert)
        for year in range(first_year, last_year + 1):
            for month in range(1, 13):
                if (year == first_year and month < first_month) or (year == last_year and month > last_month):
                    continue
                row = self.create_row(month, year)
                if row is None:
                    continue
                dataf.loc[len(dataf.index)] = row
        self.__currencies_data = dataf
        dataf.to_csv('dataframe331.csv')

    def create_currencies_to_convert(self, n = 5000) -> list:
        curr_convert = []
        currency_counts = self.df['salary_currency'].value_counts()
        for currency, count in currency_counts.items():
            print(currency, count)
            if count > n:
                curr_convert.append(currency)
        self.currencies_to_convert = curr_convert
        return curr_convert

    def create_row(self, month: str, year: str) -> list or None:
        try:
            format_month = ('0' + str(month))[-2:]
            url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/{format_month}/{year}'
            res = requests.get(url)
            tree = ET.fromstring(res.content)
            row = [f'{year}-{format_month}']
            for value in self.currencies_to_convert:
                if value == 'RUR':
                    row.append(1)
                    continue
                value_found = False
                for valute in tree:
                    if valute[1].text == value:
                        row.append(round(float(valute[4].text.replace(',', '.'))
                                         / float(valute[2].text.replace(',', '.')), 6))
                        value_found = True
                        break
                if not value_found:
                    row.append(None)
            return row
        except Exception:
            return None

result = ProcessCurrencies('vacancies_dif_currencies.csv')
result.create_currencies_to_convert()
result.generate_currency(result.min_date, result.max_date)
