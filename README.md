# TalemDB

[![Actions Status](https://github.com/maede97/TalemDB/workflows/TalemCI/badge.svg)](https://github.com/maede97/TalemDB/actions)

Datenbank-Tool für Talem

## Dependencies

Install dependencies by using `pip install -r requirements.txt`

## Run

Run the program by using `python main.py`

## Build on Windows

Simply run `pyinstaller mainWindows.spec`

## Auto Deploy with Actions
- Commit your changes
- Create Tag using `git tag -a v...` and add message "v..."
- Push your changes using `git push`
- Push tag using `git push origin v...`
- To delete a tag, use `git tag -d tagname` and `git push --delete origin tagname`
