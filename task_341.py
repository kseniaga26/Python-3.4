import pandas as pd

class ProcessSalaries:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.currencies = pd.read_csv('dataframe.csv')
        self.available_currencies = list(self.currencies.keys()[2:])

    def get_nan_salary(self, row: pd.DataFrame) -> float or str:
        salary_from, salary_to, salary_currency, published_at = str(row[0]), str(row[1]), str(row[2]), str(row[3])
        if salary_currency == 'nan':
            return 'nan'
        if salary_from != 'nan' and salary_to != 'nan':
            salary = float(salary_from) + float(salary_to)
        elif salary_from != 'nan' and salary_to == 'nan':
            salary = float(salary_from)
        elif salary_from == 'nan' and salary_to != 'nan':
            salary = float(salary_to)
        else:
            return 'nan'
        if salary_currency != 'RUR' and salary_currency in self.available_currencies:
            date = published_at[:7]
            multiplier = self.currencies[self.currencies['date'] == date][salary_currency].iat[0]
            salary *= multiplier
        return salary

    def salaries_process(self) -> None:
        dataframe = pd.read_csv(self.file_name)
        dataframe['salary'] = dataframe[['salary_from', 'salary_to', 'salary_currency', 'published_at']].apply(self.get_nan_salary, axis=1)
        dataframe.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis = 1, inplace = True)
        dataframe = dataframe.loc[dataframe['salary'] != 'nan']
        dataframe.head(100).to_csv('conversion_pandas.csv', index = False)

ProcessSalaries('vacancies_dif_currencies.csv').salaries_process()