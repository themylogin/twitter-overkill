twitter-overkill
================

Зачем это нужно?
----------------

Постинг в [twitter](https://twitter.com). Казалось бы, что может быть проще?
```python
import twitter
api = twitter.Api(...)
api.PostUpdate("Всем привет! Меня зовут Вова.")
```
Вот задачка посложнее:
```python
api.PostUpdate("Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
               "God Is An Astronaut, Mogwai, Joy Wants Eternity и This Will Destroy You.")
```
Конечно же, результатом будет
```python
twitter.TwitterError: [{u'message': u'Status is over 140 characters.', u'code': 186}]
```
Решение очевидно — формировать несколько твитов и выбирать самый приоритетный из подходящих (а если никакой не подходит, так уж и быть, обрезать с многоточием самый короткий):
```python
api_wrapper.tweet(["Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                   "God Is An Astronaut, Mogwai, Joy Wants Eternity и This Will Destroy You.",
                   
                   "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                   "God Is An Astronaut, Mogwai и Joy Wants Eternity.",
                   
                   "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                   "God Is An Astronaut и Mogwai.",])
```
Снова всё просто? А как быть в такой ситуации?
```python
"Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
"God Is An Astronaut и Mogwai. Зацените: http://last.fm/user/themylogin"
```
Несмотря на то, что длина твита — 146 символов, URL будет автоматически сокращён до `t.co`, и в итоге твит займёт 137 символов и сможет быть успешно отправлен. Получается, при вычислении длины твита необходимо найти в нём все ссылки [тем же способом, что это делает сам Twitter](https://github.com/twitter/twitter-text-js) и заменить их на «болванки» коротких ссылок, длину которых нужно ежедневно обновлять при помощи [GET help/configuration](https://dev.twitter.com/docs/api/1/get/help/configuration).

При этом очевидно, что постинг в twitter должен происходить асинхронно — дали задание и забыли: пусть сетевые задержки, повторные попытки и прочие неприятности происходят где-нибудь в отдельном потоке. А ещё хорошо бы видеть состояние отправки твитов и хранить их историю... Вот так простейшая задача, решаемая, казалось бы, одной строчкой кода, превращается в **twitter-overkill**!

Установка
---------

```bash
python setup.py develop
```

[twitter-text-python](https://github.com/ianozsvald/twitter-text-python) — отстой: его авторы не знают про [twitter-text-conformance](https://github.com/twitter/twitter-text-conformance) и потому он работает некорректно, так что придётся воспользоваться библиотекой на другом языке, например, javascript, для чего установим [node.js](http://nodejs.org) и [twitter-text-js](https://github.com/twitter/twitter-text-js):
```bash
sudo aptitude install nodejs
cd ~ && npm install twitter-text
```

Для работы вам потребуется какой-нибудь брокер сообщений, совместимый с [Celery](http://www.celeryproject.org/), например, [RabbitMQ](http://www.rabbitmq.com/) или [Redis](http://redis.io/). Его достаточно просто установить, конфигурация по-умолчанию уже работает. Так же вы, возможно, захотите хранить твиты в какой-нибудь приличной СУБД (а не SQLite).

Теперь просто создаём файл конфигурации (в `~/.config/twitter-overkill.yaml` или `/etc/twitter-overkill.yaml`):
```yaml
celery:
    BROKER_URL: amqp://

db: mysql://root@localhost/twitter_overkill?charset=utf8

consumer_key:
consumer_secret:
access_token_key:
access_token_secret:
```
Это конфигурация для RabbitMQ, таблицы в БД будут автоматически созданы при запуске.

Для запуска демона-воркера, осуществляющего, непосредственно, отправку твитов, напишем задачу для [upstart](http://upstart.ubuntu.com/):
```text
########################################
##### install in /etc/init         #####
########################################

description "twitter-overkill"

env PYTHON_HOME=/home/themylogin/www/apps/virtualenv

start on runlevel [2345]
stop on runlevel [!2345]

setuid themylogin
setgid themylogin

exec $PYTHON_HOME/bin/celery -A twitter_overkill worker

respawn
respawn limit 10 5
```

Теперь можно просто твитить:
```python
import twitter
from twitter_overkill import tweet
api = twitter.Api(...)
tweet(api, "Всем привет! Меня зовут Вова.")
tweet(api, ["Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
            "God Is An Astronaut, Mogwai, Joy Wants Eternity и This Will Destroy You.",
             
            "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
            "God Is An Astronaut, Mogwai и Joy Wants Eternity.",
             
            "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
            "God Is An Astronaut и Mogwai.",])
```
