from typing import Dict

import io
import yaml
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from slackclient import SlackClient
from todoist_achievements.converter import DateListConverter
from todoist_achievements.loader import TodoistActivityLoader


def run(config: Dict):
    dates = TodoistActivityLoader.load(config["todoist-token"])
    df = DateListConverter.convert(dates)
    ax = df.plot(kind="bar", x=df.index)
    tick_labels = [item.strftime("%b %d") for item in df.index]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(tick_labels))
    plt.gcf().autofmt_xdate()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    client = SlackClient(config["slack-token"])
    client.api_call("files.upload", channels=config["slack-channel"], file=buf)
    buf.close()


if __name__ == '__main__':
    with open("config.yml") as f:
        run(yaml.load(f))
