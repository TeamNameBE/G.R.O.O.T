# Groot (Website)
This folder contains all the logic and files behind the website https://groot.ninja

## Requirements installation
Simply run the following commands:
```
$ python3 -m venv ve
$ source ve/bin/activate
$ pip install -r requirements.txt
```

## Running a test server
First, you may need to update the `settings.py` file. Then you'll simply have to start the server by running
```
$ python3 main.py
```

In order to make the website work properly, you'll need to run a redis database, and set the correct address and port in the `settings.py` file.