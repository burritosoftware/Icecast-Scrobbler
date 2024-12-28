# Icecast Scrobbler
![Icons](https://skillicons.dev/icons?i=py)

[![wakatime](https://wakatime.com/badge/github/burritosoftware/Icecast-Scrobbler.svg)](https://wakatime.com/badge/github/burritosoftware/Icecast-Scrobbler) [![Last updated](https://img.shields.io/github/last-commit/burritosoftware/Icecast-Scrobbler/master?logo=github&label=last%20updated)](https://github.com/burritosoftware/Icecast-Scrobbler/commits/master)

An Icecast internet radio scrobbler for Last.fm, primarily designed around [Friday Night Tracks](https://fridaynighttracks.com), that includes many quality-of-life features for the monthly live radio show.

> [!WARNING]  
> This is not pretty and I would like to make it a bit more convenient than running a Python script. As a constant work-in-progress, expect bugs!

## Get It Running
1. Make sure you have Python installed.
2. Install/upgrade dependencies:
```
pip install -U -r requirements.txt
```
3. Duplicate `.env-example` to `.env`, and add a Last.fm API key and secret from https://www.last.fm/api/account/create.
> [!NOTE]  
> The configuration is, by default, set to work best with xbn.fm/Friday Night Tracks and requires no further configuration. However, if you are using an Icecast stream that only outputs one source, set `ICECAST_MULTI_SOURCE` to `False`. Additionally, if you don't want any tag removal, set the `TAG_REGEX` to `(?!x)x` to disable it.
```
cp .env-example .env
nano .env
```
4. Start the scrobbler. On first run, it'll ask you to authorize in a web browser. Then it'll start sending what's currently playing and scrobble songs once they end.
```
python3 scrobble.py
```

## Contributing
All contributions welcome! I am primarily using this for Friday Night Tracks, so while I can assist you with using this for other Icecast streams, I'm primarily making sure bugs are ironed out for FNT. However, if you're having issues either way, please open an issue and I'll try to do my best!