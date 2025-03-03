import os
import sys
import pathlib

from lcb_runner.lm_styles import LanguageModel, LMStyle
from lcb_runner.utils.scenarios import Scenario

sys.path.append(os.path.abspath("/root/codefair"))
from utils import format_attribute, format_role


def ensure_dir(path: str, is_file=True):
    if is_file:
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    else:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return


def get_cache_path(model_repr: str, attribute: str, role: str, args) -> str:
    scenario: Scenario = args.scenario
    n = args.n
    temperature = args.temperature
    path = f"cache/{model_repr}/{format_attribute(attribute)}_{format_role(role)}_{scenario}_{n}_{temperature}.json"
    ensure_dir(path)
    return path


def get_output_path(model_repr: str, attribute: str, role: str, args) -> str:
    scenario: Scenario = args.scenario
    n = args.n
    temperature = args.temperature
    path = f"output/{model_repr}/{format_attribute(attribute)}_{format_role(role)}_{scenario}_{n}_{temperature}.json"
    ensure_dir(path)
    return path


def get_eval_all_output_path(model_repr: str, attribute: str, role: str, args) -> str:
    scenario: Scenario = args.scenario
    n = args.n
    temperature = args.temperature
    path = f"output/{model_repr}/{format_attribute(attribute)}_{format_role(role)}_{scenario}_{n}_{temperature}_eval_all.json"
    return path
