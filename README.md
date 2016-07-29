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
cp env.example env
$EDITOR env

PORT=127.0.0.1:52003 docker-compose build

PORT=127.0.0.1:52003 docker-compose up
```

Теперь можно просто твитить:
```bash
pip install "https://github.com/themylogin/twitter-overkill/zipball/master#egg=twitter-overkill[client]"
```

```python
import twitter
from twitter_overkill.client import TwitterOverkill
api = twitter.Api(...)
twitter_overkill = TwitterOverkill("http://127.0.0.1:52003")
twitter_overkill.tweet(api, "Всем привет! Меня зовут Вова.")
twitter_overkill.tweet(api, ["Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                             "God Is An Astronaut, Mogwai, Joy Wants Eternity и This Will Destroy You.",

                             "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                             "God Is An Astronaut, Mogwai и Joy Wants Eternity.",

                             "Всем привет! Меня зовут Вова. Я люблю слушать Godspeed You! Black Emperor, " +
                             "God Is An Astronaut и Mogwai.",])
```
