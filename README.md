# Engineer Tree 🌳  

アプリ概要　[こちら](https://drive.google.com/file/d/15q8qybqer7ISOjVHXOt24rxkKpqLfF5h/view?usp=sharing)から

## back end

## 使用技術  
Python
Django , Django REST Framework , Pandas, matplotlib
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

## 本番環境  
```
heroku ps:scale web=1
heroku open

heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```



<!-- heroku config:set DISABLE_COLLECTSTATIC=1 -->


