# NUCraigslist

## Setup node and bower
```
brew install npm
npm install -g bower
```

## Setup ruby
```
brew install rbenv
# follow caveats (similar to pyenv)
gem install foreman
rbenv rehash
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

## Setup Postgres
```
brew install postgresql
# follow the caveats
```

## Setup NUCraigslist
```
mkvirtualenv nucraigslist
git submodule update --init
pip install -r requirements.txt
# download the .secret file
cp .secret.example .secret
# download nucraigslist.pem and symlink to repo
# ln -s /path/to/nucraigslist.pem nucraigslist.pem
sudo chmod nucraigslist.pem 400
cat ~/.ssh/id_rsa.pub | ssh -i nucraigslist.pem ubuntu@nucraigslist.com "sudo sshcommand acl-add dokku progrium"
git remote add production dokku@nucraigslist.com:www
git remote add staging dokku@nucraigslist.com:staging
```

## Usage
```
workon nucraigslist
source .secret
python manage.py migrate
# python manage.py runserver
foreman start
```

## Update Database
```
# staging
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku run staging python manage.py download
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku run staging python manage.py parse

# production
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku run www python manage.py download
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku run www python manage.py parse
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

## Pushing a Branch to Dokku
```
git push staging branch:master
```

## Running Dokku Commands from Client
```
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku config:set staging KEY=VALUE
ssh -i nucraigslist.pem ubuntu@nucraigslist.com dokku logs www
```

## Flush Database
```
python manage.py flush
python manage.py flush --database=staging
python manage.py flush --database=production
```

## Backup Database
```
# data only
pg_dump --no-owner --data-only --schema=public nucraigslist > latest.dump.txt

# with create statements
pg_dump --no-owner --schema=public nucraigslist > latest.dump.txt
```

## Seed Database
```
cat latest.dump.txt | python manage.py dbshell
cat latest.dump.txt | python manage.py dbshell --database=staging
cat latest.dump.txt | python manage.py dbshell --database=production
```

## Reset Database
```
# backup must be data only
python manage.py flush && cat latest.dump.txt | python manage.py dbshell

# YOU MUST STOP THE APP BEFORE RUNNING THESE COMMANDS AS OF NOW. THE AUTO-DOWNLOADER WILL DOWNLOAD POSTS WHILE THE RESTORE OCCURS CAUSING THE RESTORE TO ERROR OUT. WE CANNOT PAUSE THE DOWNLOADER REMOTELY DUE TO THIS: http://celery.readthedocs.org/en/latest/getting-started/brokers/django.html.
python manage.py flush --database=staging && cat latest.dump.txt | PGPASSWORD='' python manage.py dbshell --database=staging
python manage.py flush --database=production && cat latest.dump.txt | PGPASSWORD='' python manage.py dbshell --database=production
```
