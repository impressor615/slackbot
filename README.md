## Slack Bot (customized using this [tutorial](https://github.com/slackapi/Slack-Python-Onboarding-Tutorial))
----

## Requirements
----
- Python 2.7
- virtualenvwrapper
- [heroku](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

## install
----

1. clone git repository

```
git clone git@github.com:impressor615/slackbot.git

```

2. install requirements

```
mkvirtualenv -a `pwd` slackbot -p `which python`
pip install -r requirements.txt
```

3. set enviromental variables

- get the token below from [this website](https://api.slack.com/tutorials)
- you can get SK_PLANET_KEY from [this website](https://developers.skplanetx.com/apidoc/)

```
export CLIENT_ID = 'your client id'
export CLIENT_SECRET = 'your secret id'
export VERIFICATION_TOKEN = 'your verification token'
export BOT_TOKEN = 'your bot token'
export SK_PLANET_KEY = 'your sk planet key'
```

4. set webhook url in [slack page](https://api.slack.com/tutorials) with the endpoint of handlers 

## deploy (heroku)
----


```
heroku login
#put your heroku email and password

heroku create slackbot

git push heroku master
```
