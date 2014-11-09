# Lightning - Simple and Fast backend for Mikotoboard imageboard script.

## Installation

* Check out source code to the folder of your desire
* Make sure that you have your RethinkDB instance running on the same machine.
* Create VirtualEnv (http://docs.python-guide.org/en/latest/dev/virtualenvs/) and source into it
* Run
```bash
$ pip install -r requirements.txt
```
* Run
```bash
$ python install.py
```
* Start app.py and daemonize it using screen or your favourite daemonizer.
* Proxy it using Nginx or your favourite Web server, or open your app port for connections from outside local net
* Proceed to install [Flash](http://github.com/Mikotoboard/Flash).