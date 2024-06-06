#!/bin/bash
###
### Setup script for Klingon Transcribe Jupyter Notebooks
###
apt install -y jupyter-core
pip install -q jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable collapsible_headings/main