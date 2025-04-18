"""
@title

@description

"""
import json
import pickle
from pathlib import Path

import jsonlines
import pandas as pd
import yaml


def capture_log_message(message, destination=None):
    if destination is None:
        destination = print

    destination(message)
    return

def save_text(data, save_path):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'w') as data_file:
        data_file.writelines(data)
    return save_path

def load_text(save_path):
    if not save_path.exists():
        return

    with open(save_path, 'r') as data_file:
        data = [each_line.strip() for each_line in data_file]
    data = '\n'.join(data)
    return data

def save_json(data, save_path, human_readable=False):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'w') as data_file:
        # noinspection PyTypeChecker
        json.dump(data, data_file, indent=2 if human_readable else None)
    return save_path

def load_json(save_path):
    if not save_path.exists():
        return

    with open(save_path, 'r') as data_file:
        data = json.load(data_file)
    return data

def save_jsonl(data, save_path, append=False):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    if not isinstance(data, list):
        data = [data]

    open_flag = 'a' if append else 'w'
    with jsonlines.open(save_path, mode=open_flag) as jl_file:
        jl_file.write_all(data)
    return save_path

def load_jsonl(save_path):
    if not save_path.exists():
        return

    with jsonlines.open(save_path) as reader:
        data = [obj for obj in reader]
    return data

def save_pkl(data, save_path, **kwargs):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'wb') as data_file:
        # noinspection PyTypeChecker
        pickle.dump(data, data_file)
    return save_path

def load_pkl(save_path):
    if not save_path.exists():
        return

    with open(save_path, 'rb') as data_file:
        data = pickle.load(data_file)
    return data

def save_csv(data, save_path, **kwargs):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    data.to_csv(save_path, index=False)
    return save_path

def load_csv(save_path):
    return pd.read_csv(save_path)

def save_yaml(data, save_path):
    if not save_path.parent.exists():
        save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'w') as data_file:
        yaml.dump(data, data_file)
    return save_path

def load_yaml(save_path):
    if not save_path.exists():
        return

    with open(save_path, 'r') as data_file:
        data = yaml.safe_load(data_file)
    return data

def save_data(data, save_path: Path, **kwargs):
    func_map = {
        '.json': save_json,
        '.pkl': save_pkl,
        '.jsonl': save_jsonl,
        '.csv': save_csv,
        '.yml': save_yaml,
        '.yaml': save_yaml,
    }
    data_type = save_path.suffix
    save_func = func_map.get(data_type, save_text)
    result = save_func(data, save_path, **kwargs)
    return result

def load_data(save_path: Path, default_value=None):
    func_map = {
        '.json': load_json,
        '.pkl': load_pkl,
        '.jsonl': load_jsonl,
        '.csv': load_csv,
        '.yml': load_yaml,
        '.yaml': load_yaml,
    }
    data_type = save_path.suffix
    load_func = func_map.get(data_type, load_text)
    data = load_func(save_path)
    if data is None:
        data = default_value
    return data
