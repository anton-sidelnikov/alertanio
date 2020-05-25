"""Configurations fixed for library"""
from dataclasses import dataclass
from typing import Dict, List

import tyaml
from ocomone import Resources


@dataclass(frozen=True)
class BaseConfiguration:
    """Base configuration class"""
    name: str
    params: dict


@dataclass(frozen=True)
class AlertaConfiguration:
    """Alerta configuration class"""
    config_id: int
    config_name: str
    alerta_endpoint: str
    alerta_timeout: int
    alerta_debug: bool
    skip_environment: str


@dataclass(frozen=True)
class TopicMap:
    """Topic map class"""
    to: str
    subject: str


_CONFIGS = Resources(__file__)


def topic_map(topics: list):
    """Topic map"""
    map = {}
    topics = {item[0]: item[1:] for item in topics}
    for key, value in topics.items():
        map.update({key: TopicMap(*value)})
    return map


def _cfg_load(cfg_file: str, cfg_class):
    with open(cfg_file, 'r') as src_cfg:
        configs = tyaml.load(src_cfg, cfg_class)  # type: List[BaseConfiguration]
    result = {cfg.name: cfg for cfg in configs}
    return result


DATABASE: Dict[str, BaseConfiguration] = _cfg_load(_CONFIGS['db_init.yaml'], List[BaseConfiguration])
