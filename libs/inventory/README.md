# `inventory`: the `term-world` item mini-game

The `inventory` library serves as the core to the ability of world residents to write, share, and use
items created within the world's inventory framework. Unlike many of the other libraries in the world,
`inventory` serves a user and developer purpose. 

## `inventory` assumptions

`inventory` requires each user to have a `~/.inv` directory featuring a `JSON`-compatible `.registry`
file. World configuration in the [`provisioner`](https://github.com/term-world/world-configure) script
creates these files, and the `Dockerfile` in the [`world-container`](https://github.com/term-world/world-container)
also attempts to guarantee them if they do not exist.

This folder also houses copies of the items acquired by users. This means that versions of items
collected in the world by a user may vary widely, though the latest version "picked up" will be the version
that users carry with them.

## Interacting with `inventory` as a user

To view basic inventory, users type:

```bash
dluman@term-world:~$ inventory
```

This lists the status of a user's world inventory and other facts about the items they carry:

```
                           dluman's inventory
                           dluman's inventory
┏━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Item name  ┃ Item count ┃ Item file  ┃ Consumable ┃ Volume ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Fertilizer │ 1          │ Fertilizer.py │ True       │ 1       │
└────────────┴────────────┴───────────────┴────────────┴─────────┘
Your current total volume limit is: 1/10Your current total volume limit is: 1/10
```

### Types of items in the world

At present, `3` types of items exist:

* `ItemSpec`
* `FixtureSpec`
* `BoxSpec`

|Type |Consumable |Capacity |Description |
|:----|:----------|:--------|:-----------|
|`ItemSpec` |Yes |`1` |Deplete/disappear when last instance is used |
|`FixtureSpec`|No |`3`|Disappears only when destroyed |
|`BoxSpec`|No |`0` |When executed, creates an item of any type in local folder

### `get`ting items

Imagine our user has a `LettuceSeed.py` in their local folder. Typing `get` followed by the file name
adds this file (if valid) to the user's inventory.

```bash
dluman@term-world:~$ get LettuceSeed.py
```

### `use`ing items

To use the `LettuceSeed.py` file, the user should:

```bash
dluman@term-world:~$ use LettuceSeed
You try the LettuceSeed, but it doesn't do anything.
```

If items have effects, these will happen when the item is used. The above does nothing -- which is the
inherited default for all items. Items can alter this behavior if containing an overriding `use` method.

### `drop`ping items

Users may drop items in their inventory by typing:

```bash
dluman@term-world:~$ drop LettuceSeed
```

This command will drop a copy of the item in the user's local directory. This command assumes users will
only want to drop `1`, though they are able to drop any number up to the amount held in inventory. To drop
multiples:

```bash
dluman@term-world:~$ drop LettuceSeed 5
```

The above will post-pend the file name of multiples with integers numbering up to the amount dropped. `get`ting
these items will add them back to the user's inventory without the numeric suffix.

### `remove`ing items

An accessory to `drop`, `remove` allows users to destroy any number of copies of a given item in their inventory.

```bash
dluman@term-world:~$ remove LettuceSeed
```

The above will delete `1` copy. To delete multiples:

```bash
dluman@term-world:~$ remove LettuceSeed 5
```

## Interacting with `inventory` as a developer


