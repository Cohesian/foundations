---
title: Semantic Data Packets
description: Agent prompts and semantic data packets.
kind: F
edges:
  g: []
  l:
    prev: F-02-json-representation.md
    next: null
  r: []
---

# Semantic Data Packets

This note is an agent-facing digest of the semantics topic.

Use it as a compact protocol for understanding and producing nested data packets.

The goal is to communicate data shape before caring about a source format.

---

## Core Model

Data is a tree.

Each node is either:

```text
leaf
composite
```

A leaf is a terminal value.

A composite contains other values.

The current leaf types are:

| Symbol | Meaning |
| --- | --- |
| `s` | string |
| `i` | integer |
| `f` | float |
| `b` | boolean |

So:

```text
Leaf = s | i | f | b
```

---

## Composite Model

A composite is a map from an index domain to data:

$$
C : I \to D
$$

Read this as:

```text
index value -> data value
```

Arrays and objects are both composites.

They differ by index domain:

```text
array  -> numeric positions
object -> unique string keys
```

Every composite can be understood through:

```text
cap
len
type
```

Where:

- `cap` means how many entries the composite can hold
- `len` means which index-domain values are accessible
- `type` means what values may live at those indexes

For arrays, `len` is positions:

```text
0, 1, 2, ...
```

For objects, `len` is keys:

```text
"name", "age", "active", ...
```

---

## Current JSON Carrier

The first JSON carrier is intentionally small.

It exposes only:

```text
type
cap
len
sub_t
```

Leaves use only `type`:

```json
{ "type": "s" }
```

Arrays use:

```json
{
  "type": "array",
  "cap": 3,
  "sub_t": {
    "type": "s"
  }
}
```

Objects use:

```json
{
  "type": "object",
  "cap": 3,
  "sub_t": {
    "type": "f"
  }
}
```

Objects may constrain their accessible keys with `len`:

```json
{
  "type": "object",
  "cap": 3,
  "len": ["home", "work", "mobile"],
  "sub_t": {
    "type": "s"
  }
}
```

---

## Reading Rules

For a leaf:

```json
{ "type": "s" }
```

Read:

```text
this node is a string
```

For an array:

```json
{
  "type": "array",
  "cap": 4,
  "sub_t": {
    "type": "i"
  }
}
```

Read:

```text
an array with positions 0, 1, 2, 3
each item is an integer
```

For an object without `len`:

```json
{
  "type": "object",
  "cap": 2,
  "sub_t": {
    "type": "s"
  }
}
```

Read:

```text
an object with up to two unique string keys
each value is a string
```

For an object with `len`:

```json
{
  "type": "object",
  "cap": 2,
  "len": ["first", "last"],
  "sub_t": {
    "type": "s"
  }
}
```

Read:

```text
an object whose accessible keys are first and last
each value is a string
```

---

## Nested Example

Semantic packet:

```json
{
  "type": "array",
  "cap": 2,
  "sub_t": {
    "type": "object",
    "cap": 2,
    "len": ["first", "last"],
    "sub_t": {
      "type": "s"
    }
  }
}
```

Valid data:

```json
[
  {
    "first": "Ada",
    "last": "Lovelace"
  },
  {
    "first": "Grace",
    "last": "Hopper"
  }
]
```

Why valid:

```text
outer node is an array with cap 2
each item is an object
each object has keys first and last
each value is a string
```

---

## Current Limits

This compact carrier does not yet express:

- custom array item types
- custom object value types
- sparse array indexes
- key/property projection
- ranged type assignment
- exceptions over a default type
- named type references
- `Any`
- union leaf types such as `i | f`

Those belong to the larger theory and can be added later.

For now, every composite has one uniform child type through `sub_t`.

---

## Agent Instructions

When reading a semantic data packet:

1. Inspect `type`.
2. If it is a leaf type, stop.
3. If it is `array`, read `cap` and recurse into `sub_t`.
4. If it is `object`, read `cap`, optionally read `len`, and recurse into `sub_t`.
5. Treat object keys as unique strings.
6. Treat arrays as numeric positions inferred from `cap`.
7. Do not invent custom per-key or per-index types unless the carrier is extended.

When producing data for a semantic data packet:

1. Produce values matching the leaf symbols.
2. For arrays, produce values whose items all match `sub_t`.
3. For objects with `len`, use exactly those keys.
4. For objects without `len`, use unique string keys up to `cap`.
5. Preserve the tree structure.

The guiding principle is:

```text
semantics first,
representation second.
```
