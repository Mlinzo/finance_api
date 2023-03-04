from typing import Callable, Any
from numpy import genfromtxt, ndarray
import os

def load_data(filename: str, converters: tuple[Callable[[str], Any]]) -> ndarray:
    converters_dict = { ind: converter for ind, converter in enumerate(converters) }
    return genfromtxt(filename, delimiter='\t', skip_header=1, converters=converters_dict, missing_values=None, encoding='utf8')

def get_env(key: str) -> str | None:
    return os.getenv(key)