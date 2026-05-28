---
title: Execution
description: Execution as the interface admitting many executable forms.
kind: F
edges:
  g: []
  l:
    prev: F-01-function.md
    next: F-03-function-network.md
  r: []
---

# Execution

> If the function is one concrete executable form, execution is the wider interface that lets many forms belong to the same structural system.

## 1. Execution

Execution is the common interface of executable forms.

$$
F \in E
$$

and more generally:

$$
E ::= F \mid M(c, E) \mid S(c, \{E_i\}) \mid \dots
$$

So:

- `F` can be an execution
- `M` can be an execution
- `S` can be an execution
- each may contain, select, or delegate to other executions

This is why execution behaves like a **composite pattern**:

- some executions are leaves
- some executions are composites
- all belong to the same interface

Like functions, executions may receive and expose packets through local boundaries.
Input and output are therefore relative to the executable boundary, not intrinsic properties of the packet itself.

If a condition is involved, it is still part of execution:

$$
c : D \to \{0,1\}
$$

So even selection is not outside the system.
It receives something, evaluates something, and opens some inner path.

---

## 2. Execution System

We can think of an execution system as:

$$
\mathcal{E} = (E, R)
$$

where:

- `E` is the set of executable forms
- `R` is the set of structural relations between them

Those relations may later include:

- containment
- delegation
- selection
- sequencing
- composition

This is why execution can act like a kind of **glue**.

An analogy:
execution is to computational structure a bit like carbon is to chemistry.
Not because it explains everything, but because it is a highly reusable bonding concept.
From the same interface, many larger structures can be formed.

In that sense, execution is structurally cohesive.
It can connect simple forms into chains, branches, wrappers, trees, pipelines, and larger graphs.
Almost like polymers of computation.

And because each execution node may also carry meaning, condition, or transformation, the system starts to resemble a **graph of knowledge** as well as a graph of action.

---

## 3. Tree View

A simple execution tree may look like this:

```text
E
├── F
├── M(c, E)
│   └── F
└── S(c, {E_i})
    ├── F
    ├── F
    └── M(c, E)
        └── F
```

This is only one visible shape.
Later, the same system may be unfolded as:

- pipelines
- wrappers
- DAG-like applications
- richer execution graphs

The relation between DAG applications and neural-network-like structures is especially interesting, but it deserves its own paper.
