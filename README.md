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
piecemeal. To install all libraries at once, copy and paste the following command
from the list of choices:

### Unix

#### Install

`curl -fsSL https://raw.githubusercontent.com/term-world/term-util/main/install | bash`

#### Uninstall

`curl -fsSL https://raw.githubusercontent.com/term-world/term-util/main/install | bash - --uninstall`

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
