#!/usr/bin/env bash


if [ -z "$@" ]; then
  echo "MUST SPECIFY A SCRIPT TO RUN!!!"
else
  SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
  $SCRIPT_DIR/../../venv_cfclient_py/bin/python $@
fi


