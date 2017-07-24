from typing import Dict

import io

import datetime
import yaml
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from slackclient import SlackClient
from todoist_achievements.converter import DateListConverter
from todoist_achievements.loader import TodoistActivityLoader


def run(config: Dict):
    time_difference = datetime.timedelta(hours=config["time-difference"])
    dates = TodoistActivityLoader.load(config["todoist-token"], time_difference)
    df = DateListConverter.convert(dates, time_difference)
    ax = df.plot(kind="bar", x=df.index)
    tick_labels = [item.strftime("%b %d") for item in df.index]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(tick_labels))
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    title = datetime.datetime.now() + time_difference
    title = title.strftime("Todoist %Y-%m-%d")
    client = SlackClient(config["slack-token"])
    client.api_call("files.upload", channels=config["slack-channel"], file=buf, title=title)
    buf.close()


if __name__ == '__main__':
    with open("config.yml") as f:
        run(yaml.load(f))
