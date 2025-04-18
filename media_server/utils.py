"""
@title

@description

"""
import json
import math
import shutil
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import huggingface_hub
import numpy as np

def time_tag(tz_str='GMT'):
    time_zone = ZoneInfo(tz_str)
    curr_time = time.time()
    date_time = datetime.fromtimestamp(curr_time, tz=time_zone)
    time_str = date_time.strftime("%Y-%m-%d-%H-%M-%S")
    return time_str


def filter_dict(data, pass_keys):
    if isinstance(data, str):
        data = json.loads(data)

    filtered_data = {
        field_name: field_val
        for field_name, field_val in data.items()
        if field_name in pass_keys
    }
    return filtered_data


def check_disk_usage(base_path: Path, unit='gb'):
    unit_map = {
        'kb': 1e-3,
        'mb': 1e-6,
        'gb': 1e-9,
        'tb': 1e-12,
    }
    unit_mult = unit_map.get(unit, 1e-9)
    base_stat = shutil.disk_usage(base_path)
    base_stat = {
        'path': base_path,
        'total': base_stat.total * unit_mult,
        'free': base_stat.free * unit_mult,
        'used': base_stat.used * unit_mult,
        'unacc': (base_stat.total - (base_stat.used + base_stat.free)) * unit_mult,
    }
    return base_stat

def paragraphs(raw_text, max_len=180):
    raw_lines = raw_text.split('\n')
    paras = []
    for each_line in raw_lines:
        each_len = len(each_line)
        each_line = [each_line[i:i+max_len] for i in range(0, each_len, max_len)]
        each_line = '\n'.join(each_line)
        paras.append(each_line)
    full_text = '\n'.join(paras)
    return full_text
