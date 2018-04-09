# WhatStats
WhatStats is a program which allows you to generate various charts based on various statistics gathered from WhatApp chat logs. Charts are plotted with `matplotlib` and the GUI is built with `wxPython`. **Currently, only chat logs exported from WhatsApp on iOS are supported.**

## Getting Started

### Prerequisites
Python 3 is required to run WhatStats. To check which versioon yo have, type the following at the command line:
```
python --version
```
If you don't have Python, then you can download it from
[www.python.org/downloads/](https://www.python.org/downloads/).

### Installing

#### Windows
- [Download the prebuilt zip file and unzip](https://github.com/marcuscaisey/WhatStats/releases/latest)
- Run `WhatStats.exe`

#### From Source
- Install the required dependencies with
```
pip install -r requirements.txt
```
- Start the game with
```
python WhatStats.py
```

### Exporting chat log

#### iOS
|![](https://i.imgur.com/NqFh08B.png)|![](https://i.imgur.com/MuECKVM.png)|![](https://i.imgur.com/J9PDc2r.png)|
|---|---|---|

## To Do
- Add support for chat logs exported from android devices
- Add more statistics
- Add more charts?
- Fix some problems on mac OS (members list doesn't resize, progress dialog loading gauge doesn't move)
