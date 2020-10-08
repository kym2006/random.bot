import datetime

import config


async def log(bot, to_log, time=True, logfile=True, strip=True):
    if logfile:
        if strip:
            to_log = str(to_log).strip()
        else:
            to_log = str(to_log)
        if time:
            to_log = to_log.split("\n")
            to_log = [f"[{datetime.datetime.utcnow()}]: {line}" for line in to_log]
            log_string = "\n".join(to_log)
        else:
            log_string = to_log
            to_log = to_log.split("\n")
        print(log_string)
        with open(config.logfile, "a") as f:
            f.write(log_string + "\n")


def grab_logs():
    try:
        f = open(config.logfile, "rb")
        return f
    except IOError:
        f = open(config.logfile, "w")
        f.close()
        f = open(config.logfile, "rb")
        return f
