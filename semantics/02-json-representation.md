# JSON Representation

The semantic tree can be represented in many languages.

For now, this topic uses JSON as a small practical carrier language.

JSON is not the semantics itself.
JSON is the syntax used to write one projected version of the semantics down.

The goal of this version is simplicity.

It should be easy for a human to read and easy for an LLM to digest, produce, and transform.

---

## 1. Projection Rule

The theoretical space uses three composite axes:

```text
cap
len
type
```

This JSON representation intentionally exposes a small subset:

```text
arrays  -> type + cap + sub_t
objects -> type + cap + optional len + sub_t
```

So arrays and objects are both uniform in this projection.

There are no custom child types yet.

This means the JSON carrier does not expose:

- custom array item types
- custom object value types
- ranged type assignment
- type exceptions over a default
- sparse array index sets
- key/property projection
- named type references
- `Any`

Those can be introduced later.

---

## 2. Node Form

Every semantic node has a `type`.

For leaves, `type` is one primitive symbol:

```json
{ "type": "s" }
```

For composites, `type` is the composite kind:

```json
{ "type": "array" }
```

```json
{ "type": "object" }
```

Composites also have:

```text
cap
sub_t
```

Objects may additionally have:

```text
len
```

In this first JSON projection, `cap` is a JSON number.

So the invariant is:

```text
array  -> type + cap + sub_t
object -> type + cap + sub_t
object with explicit keys -> type + cap + len + sub_t
```

---

## 3. Leaves

The primitive leaves are:

```json
{ "type": "s" }
```

```json
{ "type": "i" }
```

```json
{ "type": "f" }
```

```json
{ "type": "b" }
```

These are the JSON representations of:

$$
L = \{s,i,f,b\}
$$

Long-form metadata may be added later, but the semantic core is the `type`.

For example:

```json
{
  "type": "s",
  "description": "The display name of the entity."
}
```

---

## 4. Arrays

An array uses:

```json
{
  "type": "array",
  "cap": 3,
  "sub_t": {
    "type": "f"
  }
}
```

This means:

```text
three accessible numeric positions,
positions 0, 1, and 2,
every item is a float
```

Example value:

```json
[0.2, 0.4, 0.8]
```

Arrays do not expose `len` in this first projection.

Their accessible index domain is inferred from `cap`:

$$
I_A = \{0,1,\dots,cap-1\}
$$

So:

```json
{
  "type": "array",
  "cap": 4,
  "sub_t": {
    "type": "s"
  }
}
```

means:

```text
positions 0, 1, 2, and 3,
every item is a string
```

There is no custom per-index type in this projection.

So this is intentionally not allowed yet:

```text
0: s
1: i
2: b
```

---

## 5. Objects

An object uses:

```json
{
  "type": "object",
  "cap": 3,
  "sub_t": {
    "type": "f"
  }
}
```

This means:

```text
up to three unique string keys,
every value is a float
```

Example value:

```json
{
  "height": 1.82,
  "weight": 75.5,
  "score": 98.2
}
```

The key names are not constrained by this node.

The only object key constraint here is:

```text
keys are strings,
keys are unique
```

---

## 6. Object Len

An object may constrain the accessible key domain with `len`.

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

This means:

```text
only these three keys are accessible,
every value is a string
```

Example value:

```json
{
  "home": "111-111",
  "work": "222-222",
  "mobile": "333-333"
}
```

If `len` is present, then its size should match `cap`:

$$
|\operatorname{len}| = cap
$$

This is the only explicit index-domain subset exposed in the first JSON projection.

Arrays do not expose sparse allowed positions yet.

---

## 7. Nested Uniform Structures

The repeated child type can itself be composite.

For example, an array of uniform objects:

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

Example value:

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

The object values are all strings, so this still fits the uniform rule.

---

## 8. Consequence

This projection cannot yet express heterogeneous record-like objects such as:

```text
name: s
age: i
active: b
```

That would require custom object value types.

The theoretical file allows that maneuver, but this JSON projection does not expose it yet.

So this first JSON representation is best for:

- lists with one item type
- dictionaries with one value type
- objects with constrained key sets and one value type
- nested combinations of those forms

It is not yet a full schema language.

It is a small carrier language.

---

## 9. Compatibility Rules

The first JSON projection follows these rules:

| Form | Required JSON fields |
| --- | --- |
| array | `type`, `cap`, `sub_t` |
| object | `type`, `cap`, `sub_t` |
| object with explicit keys | `type`, `cap`, `len`, `sub_t`, with `len.length = cap` |

In short:

$$
\operatorname{array} \Rightarrow cap + sub\_t
$$

$$
\operatorname{object} \Rightarrow cap + sub\_t
$$

$$
\operatorname{object} + len \Rightarrow |\operatorname{len}| = cap
$$

The excluded maneuvers are intentional.
They are available in the theory, but not in this carrier yet.

---

## 10. Relation To Inference

The inference topic uses a semantic backbone and extraction fingerprints.

This topic defines one possible compact carrier for that semantic backbone.

Inference asks:

```text
Given examples, what semantic tree is present?
```

This JSON projection asks:

```text
How much of that tree do we expose in the first practical JSON language?
```

For now, the answer is:

```text
leaves,
uniform arrays,
uniform objects,
optional object len
```

