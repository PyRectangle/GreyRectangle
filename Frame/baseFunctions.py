import time
import os


def output(text, level="info"):
    try:
        completeDebug = os.environ["LOG_LEVEL"] == "complete"
        debug = os.environ["LOG_LEVEL"] == "debug"
        info = os.environ["LOG_LEVEL"] == "info"
    except KeyError:
        completeDebug = False
        debug = False
        info = False
    underCompleteLevel = level == "info" or level == "debug"
    if level == "info" and info or debug and underCompleteLevel or completeDebug:
        currentTime = time.localtime()
        print("[" + str(currentTime.tm_hour) + ":" + str(currentTime.tm_min) + ":" + str(currentTime.tm_sec) + "] " +
              text)
