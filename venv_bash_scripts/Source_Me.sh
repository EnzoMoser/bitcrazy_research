#!/usr/bin/env bash

# Type "source Source_Me.sh" in order to access these aliases

SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR="$SOURCE_DIR"

alias run="bash $SCRIPT_DIR/run_script.sh"
alias install="bash $SCRIPT_DIR/install_module.sh"

