# `helper`: autonomous Python tutor

`helper` brings the power of GPT to `term-world` in the form of a helpful assistant providing
Python examples in the style of a system persona. This persona is currently writtent toward the
`civic` world.

## getting `help`er

Unlike other `term-world` utilities, `helper` installs as a `CLI` command. To use `helper` in 
an environment, type `helper` and follow the prompts.

### Development

To install a development version of `helper`, use `pip`:

```bash
python -m pip install -e .
```

#### `CLI`

The default install location for the development `CLI` is `~/.local/bin`. You may need to add
this location to your `.bashrc` file (for Unix):

```bash
export PATH="/PATH/TO/YOUR/HOME/.local/bin:$PATH"
```

#### Module

`helper` can be integrated into other files and/or assignments where necessary:

```python
from helper import Helper

cliv3 = Helper()

# To implement a chat loop:
cliv3.chat()

# To send a scripted question and avoid the chat loop:
cliv3.query("What is the meaning of life?")
```

To use the `helper` once installed, call it up using its name:

```bash
dluman@term-world:$ helper
```
