# WeChat Android APK Downloader

This tool helps you download WeChat Android APKs from WeChat official website.

> Only tested on python3.6.

## How to use

Download the newest version of WeChat APK:

```bash
python ./main.py
```

Download WeChat APK of specified version:

```bash
python ./main.py --target-version 6.6.6
```

List all available versions:

```bash
python ./main.py --list
```

Show helper messages:

```bash
python ./main.py -h
```

## How to test

Some test cases need custom environment variables, so you should set up them first.

For test get newest version:

```bash
# Replace the newest version according to
# `https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_faq_list`.
export WECHAT_NEWEST_VER=6.6.6
```

For test get url of nonexistent future version:

```bash
export WECHAT_FUTURE_VER=6.6.7
```

## Dependencies

[requests](http://docs.python-requests.org/en/master/)

[demjson](http://deron.meranda.us/python/demjson/)

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
