# `term-util`: monorepo of `term-world` services

This repository contains the source for the core libraries that provide services
to `term-world`. Each folder contains a separate `README` describing individual
libraries in more detail.

## Library list

|Library    |Purpose                                        |
|:----------|:----------------------------------------------|
|`couchsurf`|Interaction between `couchdb` and `term-world` |
|`gitit`    |Uses GitHub as static CDN for downloading off-world content |
|`helper`   |`GPT`-based chatbot used to offer civil-service Python examples |
|`inventory`|`term-world` inventory system |
|`marketplace`|Version of `pypi` for items made in `term-world` |
|`narrator` |Module that "plays" scripts and creates decision branches |
|`resources`|Raw resource system for implementation of `term-world` power grid |
|`worldlib` |Shortcut library for importing necessary assignment requirements |
|`notary`   |Provides cryptographic signatures based on `SSH` keys |

## Installing libraries

Each library contains an individual `setup.py` file for installing libraries
piecemeal. If intending to contribute to `term-util`, we recommend installing
libraries in this way using a virtual environment.

To do this:

1. create a virtual environment at a known location (such as `~/venv`)
2. activate that environment: `source ~/venv/bin/activate`
3. `cd` to the appropriate library folder in `libs/`
4. type `python -m pip install -e .` to install a development version of the library

You can then edit the source files for the library without having to reinstall
a version each time to test it.

## Contributing

To contribute to this library, [make a fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
of it and make improvements on that fork. Once ready to propose changes to `term-util`,
make a `Pull Request` to this repository. Owners will review the request and provide
any necessary feedback before merging the content.

While each library can work on its own, some libraries may be interdependent. Read through
each library's `requirements.txt` to see which libraries require each other. Most of these
co-requisites involve use of `inventory`.

For more on contribution style and process, see our [guidelines for contributing](CONTRIBUTING.md)
and [code of conduct](CODE_OF_CONDUCT.md).
