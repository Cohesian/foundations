---
title: Function Orchestration
description: Internal process coordination behind a function boundary (draft).
kind: Fd
edges:
  g: []
  l:
    prev: F-04-function-natural-wrappers.md
    next: null
  r: []
---

# Function Orchestration

> A function may expose only a boundary from the outside, while internally coordinating a whole process.
> Orchestration is one possible process role, not the only one.

## 1. Outside / Inside

From the outside, a function appears only through its visible boundary:

$$
F : D_{in} \to D_{out}
$$

or, more explicitly:

$$
F \approx (\partial F, P_F)
$$

where:

$$
\partial F = (I_F, O_F, D_{in}, D_{out})
$$

and:

$$
P_F = \text{the internal process}
$$

So from outside we see only:

- what may enter
- what may leave
- what domains must fit

The **how** is hidden in $P_F$.

Here "functor" is used only informally as a mapping-like behavior, not yet in the strict category-theoretic sense.

---

## 2. Function Types by Process Role

These are better understood as **roles**, not rigid species.
One function may mix several of them.

We can write:

$$
T(F) \subseteq
\{
\text{alg},
\text{orch},
\text{proj},
\text{match},
\text{agg},
\text{io}
\}
$$

Useful roles include:

- **algorithmic** $F_{alg}$: computes mainly through local variables, local rules, and direct transformation
- **orchestrator** $F_{orch}$: calls other functions and coordinates packet exchange between them
- **projector / adapter** $F_{proj}$: strips, selects, reshapes, serializes, deserializes, or enriches packets between domains
- **matcher / router** $F_{match}$: chooses path according to a condition or predicate
- **aggregator / reducer** $F_{agg}$: joins many packets or outputs into one result
- **boundary / effectful** $F_{io}$: interacts with file systems, networks, clocks, databases, users, or other outer systems

This matters because "function" alone is too coarse.
Different process roles produce very different structural behavior.

---

## 3. Packet and Orchestration Notation

We keep one packet symbol throughout:

$$
\rho = \text{packet}
$$

A packet does not care whether it is near an input port or an output port.
It remains a packet.
Only the local orientation of the port relative to the function changes.

We reserve:

$$
\pi_{i \to i+1}
$$

for the projection, stripping, or adaptation step between neighboring stages.

A concrete orchestration chain can be written as:

$$
F_{orch}(\rho)
=
F_c\big(\pi_{b \to c}(F_b(\pi_{a \to b}(F_a(\rho))))\big)
$$

The recurring local motif is:

$$
\rho_i \xrightarrow{F_i} \rho_i' \xrightarrow{\pi_{i \to i+1}} \rho_{i+1}
$$

That is:

$$
\rho_i' = F_i(\rho_i),
\qquad
\rho_{i+1} = \pi_{i \to i+1}(\rho_i')
$$

So the generalized linear orchestration form is:

$$
F_{orch}
=
F_n \circ \pi_{n-1 \to n} \circ F_{n-1} \circ \dots \circ \pi_{1 \to 2} \circ F_1
$$

and therefore:

$$
F_{orch}(\rho_1)
=
\big(
F_n \circ \pi_{n-1 \to n} \circ F_{n-1} \circ \dots \circ \pi_{1 \to 2} \circ F_1
\big)(\rho_1)
$$

This section is intentionally restricted to the linear case:

- call a function
- receive a packet back
- strip or project that packet
- pass a packet to the next function

Later, one may insert routing or matching logic in between these stages, but not yet.

This is still process-internal notation.
The structural relation between functions as nodes belongs to the network layer.

---

## 4. Orchestration Span

When one function centrally coordinates many inner functions $F_i$, it becomes heavy.

A cleaner term than "degree" here is:

$$
\sigma_{orch}(F)
$$

the **orchestration span** of $F$.

Informally:

$$
\sigma_{orch}(F)
=
\left|
\left\{
F_i \;\middle|\; P_F \text{ directly coordinates } F_i
\right\}
\right|
$$

So $\sigma_{orch}(F)$ measures how many inner functions are centrally handled inside one function process.

If one orchestrator coordinates:

$$
F_1 \to F_2 \to \dots \to F_n
$$

inside one local scope, its orchestration span grows.
That is one common source of bloated orchestration functions.

If orchestration is decomposed into local pairs, span decreases:

$$
F_i \to F_{i+1}
$$

Pairwise coordination often keeps local span near $2$, which is usually easier to understand, test, and replace.

This is not graph degree in the strict graph-theoretic sense.
It is a local measure of coordination burden.

---

## 5. Example

Consider one function orchestrating four inner functions:

$$
F_{big}
=
F_4 \circ \pi_{3 \to 4} \circ F_3 \circ \pi_{2 \to 3} \circ F_2 \circ \pi_{1 \to 2} \circ F_1
$$

Equivalently:

$$
\rho_1 \xrightarrow{F_1} \rho_1' \xrightarrow{\pi_{1 \to 2}} \rho_2
\xrightarrow{F_2} \rho_2' \xrightarrow{\pi_{2 \to 3}} \rho_3
\xrightarrow{F_3} \rho_3' \xrightarrow{\pi_{3 \to 4}} \rho_4
\xrightarrow{F_4} \rho_4'
$$

Here:

$$
\sigma_{orch}(F_{big}) = 4
$$

because one scope centrally coordinates all four functions.

Now compare that with pairwise local coordinators:

$$
F_{12} = F_2 \circ \pi_{1 \to 2} \circ F_1
$$

$$
F_{23} = F_3 \circ \pi_{2 \to 3} \circ F_2
$$

$$
F_{34} = F_4 \circ \pi_{3 \to 4} \circ F_3
$$

and now:

$$
\sigma_{orch}(F_{12})
=
\sigma_{orch}(F_{23})
=
\sigma_{orch}(F_{34})
=
2
$$

The graph underneath may still describe the same path.
What changes is where the coordination burden is concentrated.

Pipelines, wrappers, and graph views of function composition are treated separately in [function-network.md](function-network.md).
