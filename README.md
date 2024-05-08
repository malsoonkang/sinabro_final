# 1학기 캡디 공모전 웹사이트

# Django-HTMX Chat Application

This is a simple backend focused chat application, created with django and htmx. There is 0% trace of javascript in the source code :) 
HTMX abstracts away the usage of Javascript for connecting and interacting with the websockets and other protocols.

Demo:

[chat-app-demo.webm](https://user-images.githubusercontent.com/40317114/217275886-4334ed5a-689d-4c48-8898-b9871398b7ce.webm)


## Features:

- Create Rooms
- Join Room with code
- Send and Recieve Message

## Requirements:

- python 3.10
- django 4.1
- channels
- htmx > 1.8.5

## Installation:

1. Clone the repository

```
git clone https://github.com/Mr-Destructive/django-htmx-chat
```

2. Create a python virtual environment

```
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Make Migrations:

```
python manage.py migrate
```

5. Run the Server:

```
python manage.py runserver
```

