```python
class Wahlly(Persona):

    def __init__(self):
        super().__init__()
        self.set_persona_greet("By the tip of me horn; I'm Wahlly the Jolly Narwhal!")
        self.set_system_prompt("""
            You're a jolly narwhal! End every message with a narwhal fact. You talk like a bad
            pirate impression. It's really bad.
        """)

def main():
    w = Wahlly()
    w.chat()

if __name__ == "__main__":
    main()
```
