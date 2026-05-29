---
title: Function Natural Wrappers
description: Natural wrappers as reusable function boundaries.
kind: F
edges:
  g: []
  l:
    prev: F-03-function-network.md
    next: Fd-function-orchestration.md
  r: []
---

# Function Natural Wrappers

> A function is already a natural wrapper because it owns a hidden process inside a visible boundary.
> That is why pipelines are so often implemented through functions.

## 1. Function as Natural Wrapper

From [F-01-function.md](F-01-function.md), a function may be read as:

$$
F \approx (\partial F, P_F)
$$

where:

$$
\partial F = (I_F, O_F, D_{in}, D_{out})
$$

and:

$$
P_F = \text{the hidden internal process}
$$

So a function is already a wrapper in a structural sense:

- outside, it exposes only boundary
- inside, it contains process

If that process calls other functions, then the outer function wraps them naturally.

---

## 2. Pipeline Inside One Function

The most direct way to implement a pipeline with functions is to hide the whole path inside one larger function:

$$
F_{pipe}
=
F_n \circ \pi_{n-1,n} \circ F_{n-1} \circ \dots \circ \pi_{1,2} \circ F_1
$$

For example:

$$
\rho_1 \xrightarrow{F_1} \rho_1' \xrightarrow{\pi_{1,2}} \rho_2
\xrightarrow{F_2} \rho_2' \xrightarrow{\pi_{2,3}} \rho_3
\xrightarrow{F_3} \rho_3'
$$

This is simple and local, but the outer function becomes the central holder of the whole path.
That is exactly where a function can become bloated.

---

## 3. Wrapper Span

When one outer function centrally coordinates many inner functions, the wrapper starts carrying too much process burden.

A useful notation here is:

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

If one outer wrapper coordinates:

$$
F_1 \to F_2 \to \dots \to F_n
$$

inside one local scope, its span grows.
That is one common source of bloated wrapper-functions.

If the path is decomposed into smaller local wrappers, span decreases.

This is not graph degree in the strict graph-theoretic sense.
It is a local measure of coordination burden.

---

## 4. Span Example

Consider one outer function wrapping four inner functions:

$$
F_{big}
=
F_4 \circ \pi_{3,4} \circ F_3 \circ \pi_{2,3} \circ F_2 \circ \pi_{1,2} \circ F_1
$$

Equivalently:

$$
\rho_1 \xrightarrow{F_1} \rho_1' \xrightarrow{\pi_{1,2}} \rho_2
\xrightarrow{F_2} \rho_2' \xrightarrow{\pi_{2,3}} \rho_3
\xrightarrow{F_3} \rho_3' \xrightarrow{\pi_{3,4}} \rho_4
\xrightarrow{F_4} \rho_4'
$$

Here:

$$
\sigma_{orch}(F_{big}) = 4
$$

because one scope centrally coordinates all four inner functions.

Now compare that with pairwise local wrappers:

$$
F_{12} = F_2 \circ \pi_{1,2} \circ F_1
$$

$$
F_{23} = F_3 \circ \pi_{2,3} \circ F_2
$$

$$
F_{34} = F_4 \circ \pi_{3,4} \circ F_3
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

The underlying path may still describe the same graph.
What changes is where the coordination burden is concentrated.

---

## 5. Build-Up Through Interface Glue

Another implementation route is to build the path through a shared interface.

Abstractly:

```text
I
a
b
c
```

where `a`, `b`, `c` all satisfy the same interface `I`.

Then the chain is built by injection:

```text
I a   I b   I c
```

So each function-like stage depends on the same outer interface and receives its next neighbor through inversion of control.

This is close to a composite / decorator style build-up:

- each stage conforms to one interface
- each stage may hold the next stage
- the chain is glued at build-up time

The glue is the shared interface plus a packet shape broad enough to cross all stages.
For structured data packets, that shared shape can be described through a [semantic tree](../L-semantics/F-01-data-semantics.md#data-packets-as-carriers).

This often keeps local wrappers smaller, because the path is assembled in build-up time instead of being fully centralized in one large outer function.

---

## 6. Two Implementations

### 6.1 Single outer wrapper

```go
type Packet any

func Pipeline(rho Packet) Packet {
    rho = A(rho)
    rho = BindAB(rho)
    rho = B(rho)
    rho = BindBC(rho)
    rho = C(rho)
    return rho
}
```

This version is:

- easy to read locally
- easy to sketch as one visible path
- easy to bloat as the path grows

### 6.2 Interface glue

```go
type Packet any

type I interface {
    Do(Packet) Packet
}

type A struct {
    next I
}

func (a A) Do(rho Packet) Packet {
    rho = AFn(rho)
    rho = BindAB(rho)
    if a.next == nil {
        return rho
    }
    return a.next.Do(rho)
}
```

Then `B` and `C` follow the same shape, and the chain is assembled in build-up time.

This version is:

- more composable
- more decomposable
- more indirect
- more dependent on a shared packet boundary

So the choice is not simply "good" versus "bad."
It is a structural tradeoff.

---

## 7. Wrapper Shape

Once a function owns inner calls, the wrapper shape appears naturally.

Suppose a function process contains:

```text
call a
call b
call c
```

Those inner calls become children in the execution tree.
Their order matters.

If the walk is DFS-like, then sibling nodes can be read as the next local lines awaiting execution when control returns upward.

That is why wrappers naturally support before/after logic:

- start time
- call inner work
- end time

This is not the same as the pure path view of a pipeline.
It is the call/return geometry that appears when the path is implemented through nested function structure.

---

## 8. Connection

This note sits between the structural views:

- [F-01-function.md](F-01-function.md): a function already owns a hidden process
- [F-03-function-network.md](F-03-function-network.md): pipelines and wrappers as graph structures

So:

- `function-network` shows the graph
- `function-natural-wrappers` shows how ordinary functions tend to implement it
- `carbon-binder` will show how one shared binder can glue many concrete forms
