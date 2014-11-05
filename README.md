## Setup python
```
brew install python
```
OR
```
brew install pyenv
echo "if which pyenv > /dev/null; then eval '\$(pyenv init -)'; fi" >> ~/.bash_profile
pyenv install 2.7.8
pyenv global 2.7.8
pyenv rehash # run this after you pip install anything
```

## Setup virtualenv/virtualenvwrapper
```
pip install virtualenv virtualenvwrapper
mkdir -p ~/.virtualenvs
echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bash_profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bash_profile
source ~/.bash_profile
```

## Setup NUCraigslist
```
mkvirtualenv nucraigslist
git submodule update --init
pip install -r requirements.txt
cp .secret.example .secret
```

## Usage
```
workon nucraigslist
source .secret
python manage.py runserver
```