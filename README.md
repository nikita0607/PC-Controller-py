> Клиент для PC-Controller проекта

## Установка

Установить клиент можно командой:

```shell
pip install -U https://github.com/nikita0607/PC-Controller-py/archive/master.zip
```

## Пример использования

```python
from pcclient import API

api = API()
api.button.add("but", "Tap me!!!")
```
[Больше примеров]("https://github.com/nikita0607/PC-Controller-py/master/examples")


## Лицензия

Copyright © 2019-2021 [nikita0607](https://github.com/nikita0607).\
Этот проект имеет [MIT](https://github.com/nikita0607/LICENSE) лицензию.
