# Engineer Tree ð³  

ã¢ããªæ¦è¦ã[ãã¡ã](https://drive.google.com/file/d/15q8qybqer7ISOjVHXOt24rxkKpqLfF5h/view?usp=sharing)ãã

## back end

## ä½¿ç¨æè¡  
Python
Django , Django REST Framework , Pandas, matplotlib
twitterAPI


## ç°å¢æ§ç¯  

ä»®æ³ç°å¢æ§ç¯  
```
$ python -m venv myenv
```

ä»®æ³ç°å¢æå¹å  
```
$ myenv\scripts\activate
```

ã©ã¤ãã©ãªã¤ã³ã¹ãã¼ã«  
```
(myenv)  pip install -r requirements.txt
```


ãã®ä»ãããã
```
(myenv)  python manage.py makemigrations --settings api_et.settings_dev
(myenv)  python manage.py migrate --settings api_et.settings_dev
(myenv)  python manage.py createsuperuser --settings api_et.settings_dev
```


.envãã¡ã¤ã«ã®è¨­å®  
åå®¹ã¯mahiro72ã¾ã§

ãµã¼ãã¼èµ·å
```
(myenv)  python manage.py runserver --settings api_et.settings_dev

```

## æ¬çªç°å¢  
```
heroku ps:scale web=1
heroku open

heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```



<!-- heroku config:set DISABLE_COLLECTSTATIC=1 -->

<!-- mysql==0.0.2
mysql-connector-python==8.0.24
mysqlclient==2.0.3
pywin32==301 -->
<!-- # pywin32==302 -->

<!-- heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set  -->


