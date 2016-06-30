Hyper-Compose
=============

Command line utility which installs docker-compose application into the hyper.sh cloud


As Hyper is (loosly) based on the docker-api, we can re-use docker-compose and docker-py, but hack out the network part to use the authentication stuff from hyper


How to use
===========

Setup virtualenv in order to install all dependencies::

    virtualenv sandbox
    . ./sandbox/bin/activate
    pip install -U pip
    pip install -e .

Now you have ``hyper-compose`` in your path, and you can use it like docker compose::

    cd path/to/composeyml
    hyper-compose up
    hyper-compose stop
    hyper-compose rm

Note that you still need to use hyper command line in order to associate floating IP to your containers
