# QuickMPC-libClient-py

[Japanese version](/README-ja.md)

## Install Package
### Develop
```console
$ git clone https://github.com/acompany-develop/QuickMPC-libClient-py.git
$ cd QuickMPC-libClient-py
$ pipenv sync --dev
```

## UnitTest

### Testing all cases
```console
$ pipenv run tox
```
Testing and syntax checking will be performed on Python 3.7, 3.8, and 3.9.

### Testing with Python 3.7
```console
$ pipenv run pytest tests
```

## Demo
This demonstration is performed by pip installing this repository under the assumption of actual use. The operating procedure is described in [demo/README.md](./demo/README.md).


## Python version
3.7.10

Tests have been done with 3.7, 3.8, and 3.9, so they all work.
