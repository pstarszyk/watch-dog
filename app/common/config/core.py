import glob
import os

from ast import literal_eval
from pathlib import Path
from pydantic import BaseModel
from strictyaml import YAML, load
from typing import Dict, Tuple


class PreProcessorConfig(BaseModel):
    """
    PreProcessor config.
    """

    scale:                  float
    size:                   Tuple
    mean:                   Tuple
    swapRB:                 bool
    crop:                   bool


class ModelConfig(BaseModel):
    """
    Model config.
    """

    weights:                str
    config:                 str
    classes:                str


class DetectorPipelineConfig(BaseModel):
    """
    Pipeline orchestrator config.
    """

    components:             Dict[str, Dict]


class Config(BaseModel):
    """
    Master config object.
    """

    preprocessor_config:            PreProcessorConfig 
    mdl_config:                     ModelConfig
    detector_pipeline_config:       DetectorPipelineConfig


def fetch_config_from_yaml(path: Path) -> Dict[str, YAML]:
    """
    Parse YAMLs.
    """

    parsed_configs = {}
    for config_file_path in glob.glob(str(path / "*.yaml")):
        config_name = config_file_path.split('/')[-1:][0].split('.')[0]
        try:
            with open(config_file_path, "r") as config_file:
                parsed_config = load(config_file.read()).data
                if config_name == 'preprocessor_config':
                    parsed_config['scale'] = eval(parsed_config['scale'])
                    parsed_config['size'] = literal_eval(parsed_config['size'])
                    parsed_config['mean'] = literal_eval(parsed_config['mean'])
        except:
            raise OSError(f"Did not find config file at path: {config_file_path}")
        parsed_configs[config_name] = parsed_config
    return parsed_configs


def create_and_validate_config() -> Config:
    """
    Run validation on config values.
    """

    path = Path(__file__).resolve().parent
    parsed_configs = fetch_config_from_yaml(path)

    _config = Config(
        detector_pipeline_config=DetectorPipelineConfig(**parsed_configs["detector_pipeline_config"]),
        preprocessor_config=PreProcessorConfig(**parsed_configs["preprocessor_config"]),
        mdl_config=ModelConfig(**parsed_configs["mdl_config"])
    )
    return _config