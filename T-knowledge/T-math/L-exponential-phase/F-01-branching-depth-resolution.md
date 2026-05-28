---
title: Branching Depth Resolution
description: Base as branching factor; exponent as depth coordinate.
kind: F
edges:
  g: []
  l:
    prev: null
    next: F-02-discrete-phase-rulers.md
  r: []
---

# Branching Depth Resolution

> `b` is the branching factor.
> We keep `b` fixed and change the exponent in order to inspect depth with different rulers.

The goal here is to go slowly.

We will not try to explain everything at once.
We will only build the first core idea:

- a base can be read as a branching factor
- an exponent can be read as a depth coordinate
- a rational exponent can act like a phase ruler over that depth

---

## 1. Two Anchor Properties

Everything begins with two simple facts:

$$
b^0 = 1
$$

and:

$$
b^1 = b
$$

These two identities are more important than they first appear.

They say:

- `1` is the universal origin
- `b` is the endpoint of the first full phase span

So every base already comes with a minimal frame:

```text
1 -> b
```

This is the coarse jump.

If later we refine that jump, we should still preserve these same anchor ideas:

- an origin at `1`
- a full jump at `b`

That is why these two formulas are the right place to begin.

---

## 2. The Global Depth Sequence of a Base

For a fixed branching factor `b`, define its global depth sequence:

$$
\mathcal{D}_b = \{b^k \mid k \in \mathbb{N}_0\}
$$

This only means:

- start at the origin `1`
- keep applying the same branching base `b`
- record the reachable layers

So if `b=3`, the depth sequence is:

```text
1, 3, 9, 27, 81, ...
```

because:

$$
3^0=1,\qquad
3^1=3,\qquad
3^2=9,\qquad
3^3=27
$$

and so on.

At this level the exponent is just telling us which depth layer we are on.

So:

- the base fixes the branching law
- the exponent fixes the depth position

That is the global view.

---

## 3. Why Rational Exponents Matter

Now we make the main move of the paper.

Instead of only looking at integer depths, we ask:

$$
b^{n/a}
$$

What is this doing structurally?

The key rewrite is:

$$
b^{n/a}
=
\left(b^{1/a}\right)^n
$$

This formula is the center of the note.

It says:

- first, cut the coarse jump into `a` equal phase slices
- then move `n` of those slices

So:

- `a` is the phase ruler
- `1/a` is one phase unit
- `n/a` is the depth reached after `n` phase units

This is why rational exponents are not just arithmetic ornaments here.
They let us inspect the inside of one coarse jump.

---

## 4. The Primitive Phase Step

The most important phase is always:

$$
b^{1/a}
$$

Why?

Because it is the first positive step on that chosen ruler.

Every other phase on the same ruler is built from it:

$$
b^{2/a},\qquad
b^{3/a},\qquad
\dots,\qquad
b^{a/a}=b
$$

So `1/a` is primitive on that ruler.

This is why we test the ruler at `1/a`, not first at `5/35` or `2/4`.

Those are already accumulated phases.
The real question is always:

$$
\text{does } b^{1/a} \text{ already give an exact discrete first step?}
$$

If the first phase is not exact, the whole ruler fails as an exact discrete ruler.

If the first phase is exact, the rest can be built by repeating it.

---

## 5. Hidden Generator Under Zoom

Suppose the first phase step is exact and lands in the natural numbers.
Call it:

$$
g = b^{1/a}
$$

Then:

$$
b^{n/a} = g^n
$$

This is the zoom principle.

The coarse base `b` has now been "squished" into a smaller hidden generator `g`.

From the coarse view, we only saw:

```text
1 -> b
```

But under zoom, we now see:

```text
1 -> g -> g^2 -> ... -> g^a = b
```

This works because the hidden generator also satisfies the same anchor pattern:

$$
g^0 = 1,
\qquad
g^1 = g
$$

This point is essential.

The reason `b^{1/a}` matters is not only that it is the first phase.
It matters because once it lands on an integer, the resulting value also satisfies the same base law:

$$
x^1 = x
$$

So the first exact micro-jump does two things at once:

- it gives the number of nodes at that first phase depth
- it also gives a legitimate new local base for that ruler

So `g` is not only an intermediate value.
It becomes a legitimate finer branching base.

---

## 6. Exact Discreteness

Not every chosen ruler is valid in a discrete setting.

The exact condition is:

$$
b^{1/a} \in \mathbb{N}
$$

If this happens, then the chosen ruler gives exact discrete phases.

If it does not happen, then the ruler still exists over the reals, but not as an exact node-by-node discrete phase sequence.

So the right question is not only:

$$
\text{can we cut the exponent into slices?}
$$

It is:

$$
\text{does that cut produce a discrete first jump?}
$$

That is the whole test.

---

## 7. Depth Windows

So far we have only looked at the first coarse interval:

$$
0 \le e \le 1
$$

But the same phase idea can be shifted to any unit depth window:

$$
m \le e \le m+1
$$

for some integer depth `m`.

In that case the phase points are:

$$
b^m,\quad
b^{m+1/a},\quad
b^{m+2/a},\quad
\dots,\quad
b^{m+a/a}=b^{m+1}
$$

So a phase ruler is not tied only to the first jump from the origin.
It can be used inside any later coarse jump of the same depth sequence.

---

## 8. First Worked Example: `9`

Take:

$$
b=9,\qquad a=2
$$

Then:

$$
9^{1/2}=3
$$

So the first phase step is exact.
This means the hidden generator is:

$$
g=3
$$

Now the whole coarse jump:

```text
1 -> 9
```

unfolds into:

```text
1 -> 3 -> 9
```

because:

$$
9^{0/2}=1,\qquad
9^{1/2}=3,\qquad
9^{2/2}=9
$$

The midpoint here is multiplicative, not arithmetic.

So the "middle" of `1` and `9` is not `5`.
It is:

$$
\sqrt{9}=3
$$

This is our first clean example of an exact discrete phase ruler.

---

## 9. Second Worked Example: `27`

Now take:

$$
b=27,\qquad a=3
$$

Then:

$$
27^{1/3}=3
$$

Again, the first phase is exact.
So the hidden generator is still:

$$
g=3
$$

But now the ruler is finer.

Instead of two layers:

```text
1 -> 3 -> 9
```

we get three phase steps before reaching the coarse endpoint:

```text
1 -> 3 -> 9 -> 27
```

because:

$$
27^{0/3}=1,\qquad
27^{1/3}=3,\qquad
27^{2/3}=9,\qquad
27^{3/3}=27
$$

This example is important because it shows that `sqrt` is not special.

`a=2` is only one possible phase ruler.
Here the exact ruler is cubic:

$$
a=3
$$

---

## 10. One Endpoint, Several Rulers

Some endpoints admit more than one exact ruler.

The clean example is:

$$
64
$$

because:

$$
64 = 8^2 = 4^3 = 2^6
$$

So `64` can be unfolded in several exact ways.

With `a=2`:

$$
64^{1/2}=8
$$

giving:

```text
1 -> 8 -> 64
```

With `a=3`:

$$
64^{1/3}=4
$$

giving:

```text
1 -> 4 -> 16 -> 64
```

With `a=6`:

$$
64^{1/6}=2
$$

giving:

```text
1 -> 2 -> 4 -> 8 -> 16 -> 32 -> 64
```

So one and the same endpoint may admit several exact phase rulers.

The finer the valid ruler, the deeper the exact layered tree.

It is also useful to compare these rulers on one common line:

```text
1, 2, 4, 8, 16, 32, 64
```

On that shared phase line:

- base `64` reaches the endpoint in one coarse jump
- base `8` reaches it in two coarse jumps
- base `4` reaches it in three coarse jumps
- base `2` reaches it in six coarse jumps

So different exact rulers may be compared almost linearly once they are projected onto the same endpoint.
This is one reason the `64` example is so rich.

---

## 11. When the Ruler Fails

Now take a counterexample:

$$
12
$$

At first it may look like `12` should fit somewhere between powers of `2`.
But exact discrete phase subdivision fails.

For example:

$$
12^{1/2} \notin \mathbb{N},
\qquad
12^{1/3} \notin \mathbb{N}
$$

So `12` does not admit a nontrivial exact discrete hidden generator.

This is important because it shows that size is not enough.

A number may be large and still fail.
A number may be smaller and still succeed.

What matters is not magnitude alone.
What matters is whether the endpoint can be exactly written as repeated powers of a smaller integer generator.

---

## 12. Head, Tail, and Unfolding

It is helpful to name the parts.

If:

$$
B = g^a
$$

then:

- `1` is the origin
- `g` is the hidden generator, or head
- `B` is the coarse endpoint, or tail

And the full unfolding is:

$$
\big(B^{0/a}, B^{1/a}, \dots, B^{a/a}\big)
=
\big(1, g, g^2, \dots, g^a\big)
$$

So the tail already contains the head implicitly.

The role of the rational exponent is to reveal the intermediate layers between them.

This is the cleanest structural reading of the note.

---

## 13. What This Paper Has Shown

We can now summarize the first result.

Given a base `b`:

1. `b^0=1` and `b^1=b` give the origin and the coarse jump.
2. `b^{n/a}` introduces a phase ruler over that jump.
3. `b^{1/a}` is the primitive first phase step on that ruler.
4. If `b^{1/a}` lands in `\mathbb{N}`, it becomes a hidden generator `g`.
5. Then:
   $$
   b^{n/a}=g^n
   $$
   and the coarse jump unfolds into an exact discrete phase sequence.

So a rational exponent may act as a depth-resolution operator over a branching structure.

---

## 14. What Comes Next

This first paper intentionally stops here.

We have not yet treated:

- the full prime-factor criterion
- local spans between internal levels
- logarithmic localization
- the later bridge toward continuity and Euler

Those belong to later notes in the track.

For now, the main insight is already enough:

> a coarse exponential jump may hide an exact finer unfolding, and the test begins at the first phase step `b^{1/a}`.
