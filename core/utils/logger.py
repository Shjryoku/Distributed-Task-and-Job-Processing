import datetime
import os

LOG_PATH = "logs/server.log"

def info(msg: str): return _logger("INFO", msg)
def warn(msg: str): return _logger("WARN", msg)
def error(msg: str): return _logger("ERROR", msg)
def debug(msg: str): return _logger("DEBUG", msg)

def _logger(level: str, msg: str):
    entry = {
        "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "level": level,
        "msg": msg
    }

    log = _formatter(entry)

    to_file(log)

def _formatter(entry):
    return f"[{entry['time']}] [{entry['level']}] [{entry['msg']}]"

def to_file(log):
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log + "\n")
    except Exception as e:
        print(f"Logger error: {e}")

