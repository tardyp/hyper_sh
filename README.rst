Hyper-Compose
=============

Command line utility which installs docker-compose application into the hyper.sh cloud


As Hyper is (loosly) based on the docker-api, we can re-use docker-compose and docker-py, but hack out the network part to use the authentication stuff from hyper


POC
===

This project is more a PoC. Some features of docker-compose are not working

- Networking configuration
- container re-creation (they need to be removed, and the created again)
- IP affectation (you will need to use original hyper command line in order to affect public IP addresses to your containers)

Future plans
============

The official hyper-compose functionality from hyper crew will come later with better integration to the hyper system.
It will be directly integrated into the "hyper" command line utility, and will be implemented mostly server side, to provide better coordination, and status monitoring.

Install from pip
================

::

    pip install hyper-compose

How to develop
==============

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
