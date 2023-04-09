# `helper`: autonomous Python tutor

`helper` brings the power of GPT to `term-world` in the form of a helpful assistant providing
Python examples in the style of a system persona. This persona is currently writtent toward the
`civic` world.

## getting `help`er

Contrary to other `term-util` libraries, `helper` installs as a `CLI` interface. It can be
integrated into other files and/or assignments where necessary:

```python
import helper

cliv3 = Helper()

# To implement chat:
cliv3.chat()

# To send a scripted question:
cliv3.query("What is the meaning of life?")
```

