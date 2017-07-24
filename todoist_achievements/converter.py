from typing import List

import datetime
import pandas as pd


class DateListConverter:
    @staticmethod
    def convert(dates: List[datetime.datetime], time_difference: datetime.timedelta, days=10) -> pd.DataFrame:
        df = pd.DataFrame(columns=["solved"])
        for date in dates:
            x = pd.DataFrame({"solved": [1]}, index=[date])
            df = df.append(x)

        for i in range(days):
            date = datetime.datetime.now() - datetime.timedelta(days=i) + time_difference
            x = pd.DataFrame({"solved": [0]}, index=[date])
            df = df.append(x)

        df = df.groupby(pd.Grouper(level=0, freq="d")).sum()
        return df.sort_index(ascending=False)[:days].sort_index(ascending=True)
