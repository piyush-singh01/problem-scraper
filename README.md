# Problem Scraper
A problem scraper to scrap problems from online judges in markdown(`.md`) format.

## Usage
```bash
# Clone the repo
$ git clone https://github.com/piyush-singh01/problem-scraper
$ cd problem-scraper

# Install requirements
$ pip install -r requirements.txt
```

### For CSES Problem set
Currently can fetch problems as well as entire task sections from CSES.

To fetch a single problem
```bash
$ python cses_scrap.py https://cses.fi/problemset/task/1068
```

To fetch entire task sections
```bash
$ python cses_scrap.py "Graph Algorithms"
```

### For Codeforces
Fetch the problem 
```bash
$ python cfscrap.py 
```

