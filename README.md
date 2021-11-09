# Engineer Tree 🌳  

バックエンド


## 使用技術  
Python
Django
Django REST Framework
Pandas,matplotlib
twitterAPI

## 環境構築  


仮想環境構築  
```
$ python -m venv myenv
```

仮想環境有効化  
```
$ myenv\scripts\activate
```

ライブラリインストール  
```
(myenv)  pip install -r requirements.txt
```


その他いろいろ
```
(myenv)  python manage.py makemigrations --settings api_et.settings_dev
(myenv)  python manage.py migrate --settings api_et.settings_dev
(myenv)  python manage.py createsuperuser --settings api_et.settings_dev
```


.envファイルの設定  
内容はmahiro72まで

サーバー起動
```
(myenv)  python manage.py runserver --settings api_et.settings_dev

```



heroku ps:scale web=1
heroku open

heroku run python manage.py migrate
heroku run python manage.py createsuperuser




<!-- heroku config:set DISABLE_COLLECTSTATIC=1 -->

<!-- mysql==0.0.2
mysql-connector-python==8.0.24
mysqlclient==2.0.3
pywin32==301 -->
<!-- # pywin32==302 -->

<!-- heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set  -->


