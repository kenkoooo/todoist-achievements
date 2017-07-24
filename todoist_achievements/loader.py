import datetime
from typing import List

import todoist

TODOIST_START = "2017-07-18T00:33"
DATE_FORMAT = "%a %d %b %Y %H:%M:%S +0000"


class TodoistActivityLoader:
    @staticmethod
    def load(api_token: str) -> List[datetime.datetime]:
        api = todoist.TodoistAPI(api_token)
        activity_list = api.activity.get(event_type="completed", since=TODOIST_START, limit=100)
        dates = []
        for activity in activity_list:
            event_date = datetime.datetime.strptime(activity["event_date"], DATE_FORMAT)
            dates.append(event_date)

        return dates
