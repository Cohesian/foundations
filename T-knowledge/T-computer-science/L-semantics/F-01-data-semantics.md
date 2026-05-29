---
title: Data Semantics
description: Composite tree shape of data before file format.
kind: F
edges:
  g: []
  l:
    prev: null
    next: F-02-json-representation.md
  r: []
---

# Data Semantics

Data has a natural shape before it has a file format.

That shape is a composite tree.

A value is either:

- a leaf
- a composite containing other values

The file representation may be JSON, YAML, TOML, XML, CSV, Markdown, HTML, or something else.
Those languages do not create the data semantics.
They only express it through a particular syntax.

This topic focuses on the semantic structure itself.
The representation layer comes later.

---

## 1. Natural Shape

The first idea is simple:

```text
data = tree(leaf | composite)
```

Equivalently:

$$
D ::= L \mid C
$$

Where $D$ is data, $L$ is a leaf, and $C$ is a composite.

A leaf is a terminal value.
It does not contain other semantic children.

A composite is a container.
It binds children into a larger structure.

So a nested document, object, table row, API response, config file, or profile record can all be read as a tree:

```text
root
  branch
    leaf
  branch
    composite
      leaf
      leaf
      composite
        leaf
```

The tree is the semantic object.
The concrete language is only one way to write it down.

### Data Packets As Carriers

In the [function graph lens](../L-functions/F-01-function.md#2-ports-and-packets), a packet is the value that travels through ports and between executable nodes.

Data semantics describes one important way to understand what such a packet may contain.
A packet may carry a leaf, tuple, record, array, object, table row, API response, document, or any nested composite tree.

So the packet belongs to the execution or network view.
The semantic tree belongs to the data-shape view.

This distinction matters because two functions may both exchange packets while expecting different semantic shapes.
In that case, validation, projection, serialization, deserialization, or adapter logic can be understood as changing the packet's representation or shape while preserving enough meaning for the next boundary.

---

## 2. Leaves

The first version of the leaf system has four primitive types:

| Symbol | Meaning |
| --- | --- |
| `s` | string |
| `i` | integer |
| `f` | float |
| `b` | boolean |

So a leaf is one of:

```text
s | i | f | b
```

Or:

$$
L = \{s,i,f,b\}
$$

This does not yet include unions such as:

```text
i | f
```

That may be useful later, but it adds another axis of complexity.
For now, each leaf has one primitive type.

---

## 3. Composites As Domain Maps

A composite is a container indexed by some domain.

In the most general shape:

$$
C : I \to D
$$

Where:

- $I$ is the index domain
- $D$ is the data domain

The composite maps index values to data values.

Arrays and objects are both composites in this sense.
They differ by the kind of index domain they use.

```text
array  -> numerical index domain
object -> key index domain
```

So both can be understood through the same three axes:

```text
cap
len
type
```

Where:

- `cap` says how many entries the composite can hold
- `len` says which index-domain values are accessible
- `type` says what values may live at those index-domain values

This is the most useful shared frame:

```text
composite<cap,len,type>
```

or:

$$
C\langle cap,len,type\rangle
$$

---

## 4. Capacity

Capacity answers:

```text
how many entries can this composite hold?
```

For arrays, those entries are items.

For objects, those entries are key-value entries.

Capacity can be finite:

```text
n
```

or unbounded:

```text
u
```

So:

$$
cap \in \mathbb{N} \cup \{u\}
$$

with:

$$
u \equiv 0..n
$$

Capacity is about the size of the accessible container.

It does not by itself say that every possible entry is required.
Requiredness is an orthogonal layer.

---

## 5. Len

`len` answers:

```text
which index-domain values are accessible?
```

This is different from capacity.

Capacity says:

```text
how many?
```

`len` says:

```text
which ones?
```

For arrays, `len` is about numeric positions:

```text
0, 1, 2, 3, ...
```

For objects, `len` is about keys:

```text
"name", "age", "active", ...
```

The ordinary array often has an implied `len`.

If:

```text
cap = 4
```

then the usual accessible positions are:

```text
0, 1, 2, 3
```

But the theory can also allow sparse or explicit position sets:

```text
len = {1, 3, 6}
```

For objects, explicit `len` is more natural:

```text
len = {"home", "work", "mobile"}
```

So `len` is the accessible slice of the index domain.

Symbolically:

$$
I_{len} \subseteq I
$$

and:

$$
|I_{len}| \leq cap
$$

---

## 6. Type

`type` answers:

```text
what values may live at the accessible indexes?
```

The simplest case is uniform:

```text
every index -> T
```

For example:

```text
every array position -> s
every object key -> f
```

A more expressive case is custom assignment:

```text
index 0 -> s
index 1 -> i
index 2 -> b
```

or:

```text
name -> s
age -> i
active -> b
```

A deeper language could also allow ranged assignment:

```text
0..3 -> s
4..7 -> i
```

or exceptions over a default:

```text
default -> T
except 3 -> T_3
except 6 -> T_6
except 7 -> T_7
```

So the type axis can be understood as a type assignment over `len`:

$$
\tau : I_{len} \to Type
$$

Uniform type is the constant case:

$$
\tau(i) = T
$$

for every accessible index $i$.

Custom type is the non-constant case.

---

## 7. Arrays

An array is a composite whose base index domain is numerical.

$$
A : I_A \to D
$$

where:

$$
I_A \subseteq \mathbb{N}_0
$$

The ordinary array uses sorted positions:

```text
0, 1, 2, 3, ...
```

So:

```text
array<cap,len,type>
```

means:

```text
cap  -> how many positions are accessible
len  -> which numeric positions are accessible
type -> what value type each position accepts
```

The common case is:

```text
cap = n
len = {0, 1, ..., n - 1}
type = uniform T
```

For example:

```text
array<4,{0,1,2,3},s>
```

means:

```text
four accessible positions,
positions 0 through 3,
each value is a string
```

The theory can also express sparse access:

```text
array<3,{1,3,6},s>
```

meaning:

```text
three accessible positions,
only positions 1, 3, and 6,
each value is a string
```

And it can express custom position typing:

```text
array<3,{0,1,2},{0:s,1:i,2:b}>
```

The JSON representation may choose not to expose those maneuvers yet.

---

## 8. Objects

An object is a composite whose base index domain is a key domain.

$$
O : I_O \to D
$$

where:

$$
I_O \subseteq K
$$

In the raw theory, keys could have many possible types.

For example:

```text
i:T
s:T
b:T
```

In this notation, the left side is the key type and the right side is the value type.

The common object projection constrains the key type to unique strings:

```text
s:T
```

So the practical object can be read as:

```text
unique string keys mapped to values
```

or:

$$
O : I_O \to D
$$

where:

$$
I_O \subseteq S
$$

and every key in $I_O$ is unique.

This uniqueness is natural for objects, but it is still a constraint.
In a very raw structure, one could imagine duplicate keys.
The first usable object theory chooses the ordinary constraint:

```text
string keys,
unique keys
```

With that constraint, an object key behaves like a hashed or named index position.
The array index is numerical.
The object index is key-based.

So:

```text
object<cap,len,type>
```

means:

```text
cap  -> how many key-value entries are accessible
len  -> which keys are accessible
type -> what value type each key accepts
```

For example:

```text
object<3,{"home","work","mobile"},s>
```

means:

```text
three accessible keys,
only home/work/mobile,
each value is a string
```

And:

```text
object<3,{"name","age","active"},{"name":s,"age":i,"active":b}>
```

means:

```text
three accessible keys,
custom type per key
```

Again, the JSON representation may choose not to expose that custom type assignment yet.

---

## 9. Domain Matching

The index domain can be matched to a property of the data domain.

For objects, this appears as:

```text
key -> <property>
```

For example:

```text
key -> <name>
```

Instead of:

```json
[
  {
    "name": "Ada",
    "score": 10
  },
  {
    "name": "Grace",
    "score": 12
  }
]
```

the object may use the `name` property as the key:

```json
{
  "Ada": {
    "score": 10
  },
  "Grace": {
    "score": 12
  }
}
```

Here the key is not just a label.
It is a projection of data into key position.

Symbolically:

$$
\operatorname{key}(x) = x.\operatorname{name}
$$

The same idea can theoretically exist for arrays if a data property maps cleanly into numeric positions.

For example:

```text
index -> <rank>
index -> <step>
index -> <position>
```

The general pattern is:

```text
index value = projected data property value
```

This is another maneuver over `len`.

---

## 10. Theory Versus Projection

The theoretical space is larger than any one representation language.

In theory, composites can vary across many degrees of freedom:

- capacity
- accessible index domain
- numeric positions
- key domains
- key uniqueness
- explicit key sets
- domain/property matching
- uniform type assignment
- custom type assignment
- ranged type assignment
- type exceptions over a default
- default or fallback child types

But a practical representation does not need to expose every degree of freedom at once.

It can project the theory into a smaller language.

For example, a JSON representation may choose:

```text
arrays use natural numeric positions
objects use unique string keys
objects may expose explicit key sets
all composites use one uniform sub type
no ranged type assignment yet
no custom type assignment yet
no union leaf types yet
```

That projected language is not the whole theory.
It is a usable collapse of the theory into common nested data structures.

This matters because the goal is not only to describe data.
The goal is to give agents and LLMs a compact language for understanding dynamic nested semi-structured input and producing structured output.

---

## 11. Composition

Every child type can itself be a composite.

Both arrays and objects are composites:

$$
A \in C
$$

$$
O \in C
$$

and:

$$
C ::= A \mid O
$$

This gives the recursive tree:

```text
Node ::= Leaf | Array | Object
Leaf ::= s | i | f | b
Array ::= array<cap,len,type>
Object ::= object<cap,len,type>
```

Equivalently:

$$
N ::= L \mid A \mid O
$$

or, grouping the composite forms:

$$
N ::= L \mid C
$$

$$
C ::= A \mid O
$$

For example, a profile can be read as:

```text
object<3,{"name","age","comments"},{"name":s,"age":i,"comments":array}>
```

or expanded:

```text
object
  cap: 3
  len: {"name", "age", "comments"}
  type:
    name -> s
    age -> i
    comments -> array
```

The source file may be JSON.
Or YAML.
Or TOML.
Or HTML.

But the semantic tree is the same kind of object.

For nested structured data, the root is usually a composite.
The whole value is then a composite tree whose branches eventually terminate in leaves.

---

## 12. Orthogonal Layers

The composite tree is the base structure.

Later layers can be stacked on top of it without changing the tree grammar.

Examples:

- required or optional fields
- defaults
- descriptions
- validation constraints
- extraction targets
- confidence scores

These are orthogonal layers.

They decorate or constrain a node, but they do not change whether the node is a leaf, an array, or an object.

---

## 13. Principle

The core principle is:

```text
semantics first,
representation second.
```

A representation language tells us how to write the structure.

The semantics tells us what structure is being written.

For now:

```text
natural data shape -> semantic tree -> representation projection
```

This gives a compact universal language for nested structured data.
