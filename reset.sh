#!/bin/bash
###
### RESET CONDA ENVIRONMENT
###
# Get current conda environment name
CONDA_ENVIRONMENT=$CONDA_DEFAULT_ENV

conda deactivate
conda deactivate
conda remove --name $CONDA_ENVIRONMENT --all
conda create --name $CONDA_ENVIRONMENT python=3.11 pip -y
conda activate $CONDA_ENVIRONMENT
pip install pip-tools
pip-compile --output-file=requirements.txt requirements.in
pip install -r requirements.txt
jupyter contrib nbextension install --user
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable codefolding/main
jupyter nbextension enable execute_time/ExecuteTime
jupyter nbextension enable freeze/main
jupyter nbextension enable hide_input/main