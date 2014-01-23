# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import itertools
import numpy
import operator


def join_list(l, separator=", ", last_separator=" и "):
    if len(l) == 0:
        return ""

    if len(l) == 1:
        return l[0]

    return separator.join(l[:-1]) + last_separator + l[-1]


def tweet_with_list(tweet_variant_wo_list, tweet_variant_w_list, list_, *args, **kwargs):
    return tweet_with_lists({(False,): tweet_variant_wo_list, (True,): tweet_variant_w_list}, [list_], *args, **kwargs)


def tweet_with_lists(tweet_variants, lists, *args, **kwargs):
    tweets = []
    """
    Например, lists = [[1, 2, 3], [1, 2]]
    Мы можем взять 3 элемента из первого списка и 2 из второго,
        или 3 элемента из первого списка и 1 из второго,
        или 3 элемента из первого списка и 0 из второго,
        или 2 элемента из первого списка и 2 из второго,
        или 2 элемента из первого списка и 1 из второго и т.п.
    Это цикл по кортежам из количеств элементов, которые мы будем брать из списков.
    Для вышеописанного примера lists_counts будет перебирать значения (3, 2), (3, 1), (3, 0), (2, 2), (2, 1), ...
    """
    for lists_counts in itertools.product(*[range(len(list_), -1, -1) for list_ in lists]):
        """
        Ключи словаря tweet_variants — кортежи булевых значений длиной, равной размеру lists.
        i'ый элемент кортежа равен True, если текст твита предполагает, что i'ый список будет непустой.
        Пример: {
            (False, False): "Голодный день :(",
            (False, True):  "Пью %s",
            (True, False):  "Ем %s",
            (True, True):   "Ем %s и пью %s"
        }
        """
        tweet_variant = tweet_variants.get(tuple(map(lambda count: count > 0, lists_counts)))
        if tweet_variant is None:
            continue

        lists_slices = map(lambda list_, count: list_[:count], lists, lists_counts)

        tweet = tweet_variant % tuple(map(lambda list_: join_list(list_, *args, **kwargs), filter(None, lists_slices)))

        tweets.append((tweet, lists_counts))

    """
    Всё хорошо, но твиты должны быть отсортированы по приоритету (максимально информативные — впереди), а у нас
    получается так, что сначала мы урезаем первый список до нуля и наверняка получаем твит меньше 140 символов;
    отправляем его без единого элемента первого списка, зато с двумя элементами второго. Поэтому отсортируем твиты,
    сравнивая их следующим образом:
    """
    def cmp((tweet1, counts1), (tweet2, counts2)):
        "1. Из твитов с разным количеством элементов списков более информативен тот, в котором элементов больше"
        if sum(counts1) > sum(counts2):
            return -1
        elif sum(counts2) > sum(counts1):
            return 1

        """
        2. Из твитов с одинаковой суммой количеств элементов список выбираем тот, где количества элементов более
        сбалансированы (например, [1, 1] лучше, чем [2, 0])
        """
        std1 = numpy.std(counts1)
        std2 = numpy.std(counts2)
        if std1 < std2:
            return -1
        elif std2 < std1:
            return 1

        "И, наконец, наиболее информативен твит большей длины"
        if len(tweet1) > len(tweet2):
            return -1
        elif len(tweet2) > len(tweet1):
            return 1

        return 0

    return map(operator.itemgetter(0), sorted(tweets, cmp))
