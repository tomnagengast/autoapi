# AutoAPI

## Usage

I'm using [httpie](https://httpie.io/docs/cli/introduction) here.

Set the dev url
```sh
echo "URL=https://$REPLIT_DEV_DOMAIN"
```

```sh
http GET $URL/api/recipes
```

```sh
http GET $URL/api/meals
```

```sh
http GET $URL/api/meals/85dfc531-7e01-4755-9d64-de5c6c9cc978
```

```sh
http POST $URL/api/meals \
    name="Cookies" \
    description="The classic tollhouse cookie recipe\!"
```

```sh
http PATCH $URL/api/meals/85dfc531-7e01-4755-9d64-de5c6c9cc978 \
    name="Cookies" \
    description="The classic tollhouse cookie recipe\!"
```

```sh
http DELETE $URL/api/meals/85dfc531-7e01-4755-9d64-de5c6c9cc978
```


```sh
http GET $URL/api/recipes
```