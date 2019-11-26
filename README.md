run with

```
gunicorn wsgi -b 0.0.0.0:5000

```
Set a route to trigger a token refresh
```
echo "REFRESH_URI=$(openssl rand -hex 16)" >> .env
```

needed environment variables to retrieve the token:
and access the API
```
LOGIN_USER_NAME=
LOGIN_SECRET=
```


