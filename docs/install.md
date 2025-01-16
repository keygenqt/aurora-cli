Приложение доступно на [PyPi](https://pypi.org/project/aurora-cli/).
Менеджер пакетов `pip` доступен на большинстве дистрибутивов Linux.

Установка приложения доступна на дистрибутивах с наличием Python `3.8.10+` версии.
Была проверена на Ubuntu `20.04` & ALT Linux `10`, разработка ведется на `24.04`.

#### Ubuntu 24.04

```shell
sudo apt update
sudo apt install python3-pip

python3 -m pip install --upgrade setuptools --break-system-packages
python3 -m pip install aurora-cli --break-system-packages
```


#### Ubuntu 22.04

```shell
sudo apt update
sudo apt install python3-pip

python3 -m pip install aurora-cli
```

#### Ubuntu 20.04

```shell
sudo apt update
sudo apt install python3-pip
sudo apt install libpangocairo-1.0-0

python3 -m pip install aurora-cli
```

#### ALT Linux 10

```shell
su -
apt-get update
apt-get install sudo
control sudowheel enabled
exit
```

```shell
sudo apt-get install pip
sudo apt-get install python3-modules-sqlite3

python3 -m pip install aurora-cli
```

#### Update

```shell
python3 -m pip install aurora-cli --upgrade
```

!!! info
    Ubuntu 24+ нужно добавить флаг `--break-system-packages`.

#### Dependencies

Для работы всех компонентов приложения требуются следующие зависимости:

- `sudo` - Platform SDK требует наличе `sudo`.
- `git` - Flutter SDK клонируется из репозитория.
- `git-lfs` - Подтянет большие файлы, если такие будут.
- `ssh` - Подключение к устройствам и эмулятору происходит по SSH.
- `curl` - Требуется для работы Flutter SDK.
- `tar` - Установка Platform SDK происходит из архива.
- `unzip` - Нужна для распаковки архивов.
- `bzip2` - Нужна для распаковки архивов.
- `ffmpeg` - Конвертация формата `webm` в человеческий `mp4`.
- `vscode` - Есть методы, помогающие работе с VS Code.
- `clang-format` - Форматирование С++ кода.
- `gdb-multiarch` - Позволяет запускать отладку С++ для приложений Flutter.
- `virtualbox` - Эмулятор работает через него, необходим для установки эмулятора.

Install (Ubuntu):

```shell
sudo apt update

sudo apt-get install \
  git \
  git-lfs \
  ssh \
  curl \
  tar \
  unzip \
  bzip2 \
  ffmpeg \
  clang-format \
  gdb-multiarch \
  virtualbox
```

#### Standalone zip application

Помимо установки pip в вашей среде, aurora-cli доступно как отдельное zip-приложение.
Приложение в `pyz` доступно на странице [релизов](https://github.com/keygenqt/aurora-cli/releases) GitHub.

!!! info
    В зависимости от дистрибутивов, возможно, необходимо будет установить некоторые зависимости для использования pyz.
    Например, пакет shiv требуется в docker на Ubuntu.

Для запуска такого приложения достаточно выполнить:

```shell
python3 ~/Downloads/aurora-cli-3.2.11.pyz
```