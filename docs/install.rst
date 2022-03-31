Instalation using ``pip``
-------------------------

The latest release is available on PyPI and can be installed using ``pip``:

::

    $ pip install ena-utils

Isolated environments using ``pipx``
------------------------------------

Install and execute ena-utils in an isolated environment using ``pipx``.

`Install pipx <https://github.com/pipxproject/pipx#install-pipx>`_
and make sure that the ``$PATH`` is correctly configured.

::

    $ python3 -m pip install --user pipx
    $ pipx ensurepath

Once ``pipx`` is installed use following command to install ``ena-utils``.

::

    $ pipx install ena-utils
    $ which ena-utils
    ~/.local/bin/ena-utils
