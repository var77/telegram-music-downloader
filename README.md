# Telegram Music Downloader Bot

##### Working Demo
[@musdown_bot](http://telegram.me/musdown_bot)

### Installation and usage
Bot requires [Python](https://python.org/) v3+ to run.

Install the dependencies and start the server.
```sh
$ pip3 install -r requirements.txt
$ TELEGRAM_BOT_TOKEN=XXXX:XXXXXXXX python3 main.py
```
Then write ``/s search_text`` or ``/d youtube_video_link`` to your bot in telegram chat and enjoy!

>Use ```setup.sh``` to get the dependencies which should be installed: ```ffmpeg, youtube-dl, python3, pip3``` then it will install required python modules from ```requirements.txt```
>Don't forget to make ``dist`` directory if you haven't used ``setup.sh`` script.
>After this use [@botfather](http://telegram.me/botfather) to setup your bot and get the ``TOKEN``

>For music downloader is used [youtube-audio](https://github.com/var77/youtube-audio) module
