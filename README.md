Initial Setup

```
brew install mongo
# follow caveats after brew install
mkvirtualenv nucraigslist
git submodule update --init
pip install -r requirements.txt
cp .secret.example .secret
# go edit .secret
```

Usage

```
workon nucraigslist
git pull
git submodule update --recursive
source .secret
python test.py
```

Export Database
```
mongoexport --db nucraigslist --collection posts --out posts.json
```