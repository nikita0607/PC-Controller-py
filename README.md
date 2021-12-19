# Асинхронный клиент для PC-Controller проекта

## Установка

Установить клиент можно командой:

```shell
pip install -U https://github.com/nikita0607/PC-Controller-py/archive/dev.zip
```

## Пример использования

```python
from pcclient import API

api = API("nikita0607", "RoBo")

@api.main
async def main():
    await api.method.computer.get_info()

api.run("http://0.0.0.0")
```
[Больше примеров]("https://github.com/nikita0607/PC-Controller-py/tree/master/examples")


## Лицензия

Copyright © 2019-2021 [nikita0607](https://github.com/nikita0607). \
Этот проект имеет [MIT](https://github.com/nikita0607/PC-Controller-py/tree/master/LICENSE) лицензию.
