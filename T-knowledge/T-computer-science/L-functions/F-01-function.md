---
title: Functions
description: One lens on functions as bounded executable nodes.
kind: F
edges:
  g: []
  l:
    prev: null
    next: F-02-execution.md
  r: []
---

# Functions

> This is only one way to see a function.
> Here we begin from the function as the local origin of structure, even if later we may say that everything is execution.

## 1. Function

A function is a bounded executable node.

$$
F : D_{in} \to D_{out}
$$

For now this is only a **structural hint**, not a full signature theory.
It simply says: something may enter, something may happen inside, and something may leave.

A compact shorthand is:

$$
I_F \to F \to O_F
$$

with local process $P_F$ inside the function scope.

---

## 2. Ports and Packets

A packet is denoted by:

$$
\rho
$$

and it remains a packet wherever it travels.
It does not become a different kind of thing by approaching an input port or leaving through an output port.

Here `packet` is intentionally abstract.
It may be a scalar, tuple, record, object, nested document, serialized blob, message, API response, or any other carried value.

When the packet is a data packet carrying structured data, its inner shape can be read through [data semantics](../semantics/01-data-semantics.md#data-packets-as-carriers).
The packet is the traveling carrier.
The semantic tree is the shape of the data being carried.

What changes is not the packet, but the orientation of the port relative to the node.

Each function owns two local ports:

- input port: $I_F$
- output port: $O_F$

These are not yet the full connections between functions.
They are the local surfaces through which the function may accept or expose packets.

So:

$$
\rho \in D(I_F)
\Rightarrow
\rho \text{ may validly enter } F
$$

and:

$$
\rho \in D(O_F)
\Rightarrow
\rho \text{ may validly leave } F
$$

At this level:

- packets are what travel
- ports are the local medium
- direction toward the node gives input / output meaning

Inter-function relation belongs to the network layer, not to the local ports themselves.

---

## 3. Function as Execution

Even though we begin from the function, a function is also an execution.

$$
F \in E
$$

and we may later think more broadly in terms of:

$$
E ::= F \mid M(c, E) \mid S(c, E_i) \mid \dots
$$

So this section is function-first, but not function-only.

The important idea is:

- a function is an executable
- an executable may also receive input and expose output
- some executables are direct
- some executables delegate to inner executables

This is why the interface idea matters:
the same executable concept can describe both leaf forms and composite forms.

Check [02-execution.md](02-execution.md) for more details.

Network structure is treated separately in [03-function-network.md](03-function-network.md).
Natural wrapper implementation is treated separately in [04-function-natural-wrappers.md](04-function-natural-wrappers.md).
Generic binder structure is treated separately in [05-carbon-binder.md](05-carbon-binder.md).
