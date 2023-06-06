# `gitit`: leverage GitHub as a static CDN

The `gitit` module fetches "off-world" content from a GitHub content delivery network (CDN). This content
is largely used in assignment such as the `house` and others that rely on users being rewarded with objects
not hidden or otherwise stored on the platform server.

The library makes few methods available, though it is configurable as to which repositories it fetches from.

## `get`ting content

A standard `get` using the default configuration (i.e. `term-world`'s `world-objects` repository):

```python
import gitit

# Retrieves the Couch.py object
gitit.get(
    file_name = "Couch.py"
)
```

However, changing the endpoint and relevant repositories to pull from is possible via modifying `kwargs`:

```python
# Chooses new repository, folder, and object
gitit.get(
    raw_path = "BASE_REPOSITORY_TO_FETCH_FROM",
    file_type = "SUBDIRECTORY_TO_FETCH FROM"
    file_name = "FILE_TO_FETCH"
)
```

Successful execution of the `get` method results in download of requested object to the user's local
directory.
