# YoruProxy
## 概要
@zorrilla\_氏作の[Twitpic API to twitter media upload gateway](http://lanieve.jp/picgw/)を見て作った，おそらく同じ動作をするプログラム

## 使い方
`config.ini.example`を`config.ini`という名前でコピーしてoauthと各ユーザの設定を書き換えて`yoru_proxy.py`を走らせる．

ただし，Python3じゃないと動かない．

夜フクロウの設定は`config.ini`のserverの項目いじってなければ`http://localhost:5000/`で良い．

### config.iniについて追記
`oauth`と`server`セクション以外のセクション名はアカウントの*screen\_name*に設定する．

各ユーザのaccess\_token, access\_token\_secretはexampleのように各ユーザのセクション内に配置する．

## 依存パッケージ
- [Flask](https://pypi.python.org/pypi/Flask/)
- [twitter](https://pypi.python.org/pypi/twitter/)
