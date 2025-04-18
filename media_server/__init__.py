"""
@title

project_properties.py

@description

Common paths and attributes used by and for this project.

"""
import os
import shutil
import logging
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------
# Project versioning and attributes
# --------------------------------------------
project_name = 'media_server'
project_version = '0.1'
TIMEZONE = 'EST'

# --------------------------------------------
# Base paths for relative pathing to the project base
# --------------------------------------------
source_package = Path(__file__).parent
project_path = source_package.parent

# --------------------------------------------
# Development and source directories
# --------------------------------------------
script_dir = Path(os.environ.get('SCRIPT_DIR', project_path / 'scripts'))
notebook_dir = Path(os.environ.get('NOTEBOOK_DIR', project_path / 'nb'))
execs_dir = Path(os.environ.get('EXECS_DIR', project_path / 'execs'))

# --------------------------------------------
# Paths to store assets and related resources
# --------------------------------------------
resources_dir = Path(os.environ.get('RESOURCES_DIR', project_path / 'resources'))
data_dir = Path(os.environ.get('DATA_DIR', project_path / 'data'))
docs_dir = Path(os.environ.get('DOCS_DIR', project_path / 'docs'))
model_dir = Path(os.environ.get('MODEL_DIR', project_path / 'models'))

# --------------------------------------------
# Output directories
# Directories to programs outputs and generated artefacts
# --------------------------------------------
output_dir = Path(os.environ.get('OUTPUT_DIR', project_path / 'output'))
exps_dir = Path(os.environ.get('EXPS_DIR', output_dir / 'exps'))
log_dir = Path(os.environ.get('LOG_DIR', output_dir / 'logs'))
profile_dir = Path(os.environ.get('PROFILE_DIR', output_dir / 'profile'))

# --------------------------------------------
# Cached directories
# Used for caching intermittent and temporary states or information
# to aid in computational efficiency
# no guarantee that a cached dir will exist between runs
# --------------------------------------------
cached_dir = Path(os.environ.get('CACHED_DIR', project_path / 'cached'))

# --------------------------------------------
# Test directories
# Directories to store test code and resources
# --------------------------------------------
test_dir = Path(os.environ.get('TEST_DIR', project_path / 'test'))
test_config_dir = Path(os.environ.get('TEST_CONFIG_DIR', test_dir / 'configs'))

# --------------------------------------------
# Resource files
# paths to specific resource and configuration files
# --------------------------------------------
config_dir = Path(os.environ.get('CONFIG_DIR', project_path / 'configs'))
env_dir = Path(os.environ.get('ENV_DIR', config_dir / 'envs'))
secrets_dir = Path(os.environ.get('SECRETS_DIR', config_dir / 'secrets'))

# --------------------------------------------
# Useful properties and values about the runtime environment
# --------------------------------------------
TERMINAL_COLUMNS, TERMINAL_ROWS = shutil.get_terminal_size()

# --------------------------------------------
# Default project environment configuration
# --------------------------------------------
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
load_dotenv(env_dir / '.envs')
os.environ['HF_HOME'] = str(model_dir)