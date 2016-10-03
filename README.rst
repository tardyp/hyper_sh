Hyper_sh
========

docker-py adapted to Hyper

It uses underscore '_' instead of '-' in its name like the original `Hyper_` service, but you can actually install either spelling.

This is a thin adaptation layer of docker-py for it to work with Hyper's credential scheme

Install from pip
================

::

    pip install hyper_py

How to use
==========

hyper_sh is used with the same API as docker-py

::

    from hyper_sh import client
    c = Client()  # without argument, config is guessed by reading ~/.hyper/config.json
    print c.images()

::

    from hyper_sh import client
    c = Client("path/to/config.json")  # you can pass a specific config.json
    print c.images()

::

    from hyper_sh import client
    c = Client({'clouds': {
        os.environ['hyper_endpoint']: {
            "accesskey": os.environ['hyper_accesskey'],
            "secretkey": os.environ['hyper_secretkey']
        }
    }})  # or you can give the content of a config.json directly
    print c.images()

API
===
At the moment, hyper_sh maps 1:1 to the api of docker-py, which means that some api will not work, as they are not supported by `Hyper_`.

https://docker-py.readthedocs.io/en/latest/api/

There are some other API supported by `Hyper_` that are not yet supported by this module (i.e. fip managment).
Patches are welcome.
