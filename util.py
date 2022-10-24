import math
import os


def get_field(o: dict, *fields):
    current = o
    for field in fields:
        current = current.get(field)
        if current is not None:
            continue
        else:
            return None
    return current


SEC_PER_MIN = 60
SEC_PER_HOUR = SEC_PER_MIN * 60
SEC_PER_DAY = SEC_PER_HOUR * 8
SEC_PER_WEEK = SEC_PER_DAY * 5


def format_time(t: int, useHours=False) -> str:
    s = ""
    rest = t
    if not useHours:
        weeks = math.floor(rest / SEC_PER_WEEK)
        rest -= weeks * SEC_PER_WEEK
        if weeks != 0:
            s += f" {weeks}w"
        days = math.floor(rest / SEC_PER_DAY)
        rest -= days * SEC_PER_DAY
        if days != 0:
            s += f" {days}d"
    hours = math.floor(rest / SEC_PER_HOUR)
    rest -= hours * SEC_PER_HOUR
    if hours != 0:
        s += f" {hours}h"
    minutes = math.floor(rest / SEC_PER_MIN)
    rest -= minutes * SEC_PER_MIN
    if minutes != 0:
        s += f" {minutes}m"
    if rest != 0:
        s += f" {rest}s"
    return s


def input_bool(__prompt) -> bool:
    return input(__prompt).lower() in ['1', 'y', 'yes', 'true']

debug_mode = os.environ.get("DEBUG_MODE") or ""
DEBUG: bool = True if debug_mode.lower() in [1, 'y', 'yes', 'true'] else False
def debug_print(*args):
    if DEBUG:
        print(args)