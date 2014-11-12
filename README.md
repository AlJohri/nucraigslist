# NUCraigslist

## Setup node and bower
```
brew install npm
npm install -g bower
```

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
# download the .secret file
cp .secret.example .secret
# download nucraigslist.pem
sudo chmod nucraigslist.pem 400
cat ~/.ssh/id_rsa.pub | ssh -i nucraigslist.pem ubuntu@nucraigslist.com "sudo sshcommand acl-add dokku progrium"
git remote add production dokku@nucraigslist.com:www
```

## Usage
```
workon nucraigslist
source .secret
python manage.py migrate
python manage.py runserver
```

## Update Database
```
python manage.py download && python manage.py parse --dl
git commit -am "database update" # until we move to postgres
git push heroku master
```

## After Changing Models
```
python manage.py makemigrations
python manage.py migrate
```

## Word Bank
```
https://docs.google.com/spreadsheets/d/1vX1U4SjXDf4--P4iUg1e3apDMYhRh74xogAn6bIf5R4
```

## iPython
```
python manage.py shell_plus
python manage.py shell_plus --notebook
```

## Set up Dokku Redirect
```
dokku redirects:set www nucraigslist.com=www.nucraigslist.com
```

## Running Dokku Commands from Client
```
ssh -i nucraigslist.pem dokku@nucraigslist.com <command>
```