#! /bin/bash
# :Author:
#     Samuel Góngora García (s.gongoragarcia@gmail.com)

# __author__ = 's.gongoragarcia@gmail.com'

script_path="$( cd "$( dirname "$0" )" && pwd )"
project_path=$( readlink -e "$script_path/.." )

linux_packages="$script_path/debian.packages"
venv_dir="$project_path/.venv"

sudo apt install $(grep -vE "^\s*#" $linux_packages  | tr "\n" " ")

virtualenv --verbose -p /usr/bin/python2.7 $venv_dir
source "$venv_dir/bin/activate"

pip install -r "$project_path/requirements.txt"