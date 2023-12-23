# Icecast Scrobbler
![Icons](https://skillicons.dev/icons?i=py)

[![wakatime](https://wakatime.com/badge/github/burritosoftware/Icecast-Scrobbler.svg)](https://wakatime.com/badge/github/burritosoftware/Icecast-Scrobbler) [![Last updated](https://img.shields.io/github/last-commit/burritosoftware/Icecast-Scrobbler/pages?logo=github&label=last%20updated)](https://github.com/burritosoftware/Icecast-Scrobbler/commits/pages/)

An Icecast internet radio scrobbler for Last.fm, primarily designed for [Friday Night Tracks](https://fridaynighttracks.com).

## Disclaimer
This is not pretty and I would like to make it a bit more convenient than running a Python script. As a constant work-in-progress, expect bugs!

## Get It Running
1. Make sure you have Python installed.
2. Install/upgrade dependencies:
```
pip install -U -r requirements.txt
```
3. Duplicate `.env-example` to `.env`, and add a Last.fm API key and secret from https://www.last.fm/api/account/create.
```
cp .env-example .env
nano .env
```
4. Start the scrobbler. On first run, it'll ask you to authorize in a web browser. Then it'll start sending what's currently playing and scrobble songs once they end.
```
python3 scrobble.py
```