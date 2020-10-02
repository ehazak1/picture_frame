from flask import request
import json
from time import time
from pathlib import Path

def cookie_setup(display_session):
    display = request.cookies.get('display')
    if display:
        display = int(display)
        display += 1
        if display > len(display_session):
            display = 0
    else:
        display = 0
    
    return display


def make_display_decision(display, display_session, results):
    if display < len(display_session):
        res = results[display_session[display]]
        # Skip empty results 
        while len(res[0]['results']) == 0:
            display += 1
            if display >= len(display_session):
                display = 0
            res = results[display_session[display]]
        display_slideshow = False
    else:
        res = None
        display_slideshow = True

    return res, display_slideshow


def write_results(results):
    Path('results.json').touch(mode=0o666, exist_ok=True)
    with open('results.json') as f:
        f.write(json.dumps(results))


def check_stale_data(stats):
    last_updated_cookie = request.cookies.get('cfjc_res_updated')
    if last_updated_cookie:
        last_updated = int(last_updated_cookie)
        if int(time()) - last_updated < 3600:
            with open('results.json') as f:
                results = json.loads(f.read())
        else:
            results = stats.get_daily_results()
            write_results(results)
            last_updated = int(time())
    else:
        results = stats.get_daily_results()
        write_results(results)
        last_updated = int(time())
    return last_updated, results