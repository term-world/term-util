# `helper`: autonomous Python tutor

`helper` brings the power of GPT to `term-world` in the form of a helpful assistant providing
Python examples in the style of a system persona. This persona is currently writtent toward the
`civic` world.

## getting `help`er

Contrary to other `term-util` libraries, `helper` installs as a `CLI` interface. It can be
integrated into other files and/or assignments where necessary:

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
