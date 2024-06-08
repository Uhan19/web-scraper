## Web scraper

The web scraper can be used to check if a product is in stock on a website.

## Initial setup

Install python if you do not have it on your machine. The following setup is focused on MacOS.
[source](https://medium.com/marvelous-mlops/the-rightway-to-install-python-on-a-mac-f3146d9d9a32)

### Install xcode-select

`xcode-select --install`

### Install HomeBrew

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

`brew update`
`brew upgrade`

### Install Pyenv and pyenv-virtualenv

Pyenv allows you to have multiple versions of python on one machine. pyenv-virtualenv allows to create virtual envs for specific python versions.

`brew install pyenv pyenv-virtualevn`

Add the following lines to your .zshrc

`eval "$(pyenv init -)"
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi`

### Install specific version of python

This project uses python v3.12.1

`pyenv install 3.12.0`

### Create a virtualenv

`pyenv virtualenv 3.12.1 web-scraper`

activate the virtual env

`pyenv local myproject`

### To run a script

example cmd: `poetry run python src/buying_group_new_deal_monitor.py`
