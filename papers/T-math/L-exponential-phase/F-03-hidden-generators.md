# Hidden Generators

> When the first exact phase step lands in the natural numbers, it is no longer only a value.
> It becomes a new local branching base.

This note continues [F-02-discrete-phase-rulers.md](F-02-discrete-phase-rulers.md).

The previous paper stabilized the phase language.
This one focuses on the object that appears when a ruler is exact:

$$
g = b^{1/a}
$$

We will call that object the hidden generator.

---

## 1. From Phase Step to Generator

Suppose a chosen ruler `a` is exact for a base `b`.

Then:

$$
b^{1/a}\in\mathbb{N}
$$

and we may define:

$$
g = b^{1/a}
$$

This gives:

$$
b^{n/a} = g^n
$$

So the first exact phase step does not only tell us a node count at depth `1/a`.
It gives a whole new local branching law.

This is why `g` is more than an intermediate number.
It generates the entire exact phase sequence.

---

## 2. Hidden Does Not Mean Secondary

The word "hidden" does not mean unimportant.

It only means that `g` is not visible in the coarse jump:

```text
1 -> b
```

At the coarse scale we only see the endpoint `b`.

But once the jump is unfolded by an exact ruler, we discover:

```text
1 -> g -> g^2 -> ... -> g^a = b
```

So the generator was structurally present all along.
The exact ruler simply made it visible.

---

## 3. A Generator Is Relative to a Ruler

For a fixed coarse endpoint, the hidden generator is always relative to a chosen exact ruler.

If:

$$
b^{1/a}=g
$$

then:

$$
b = g^a
$$

So a generator and a ruler always appear together:

- `a` tells us how many exact phase steps fit in the coarse jump
- `g` tells us what local base generates those steps

This is an important duality:

- choose a ruler `a`, and it determines a generator `g`
- choose a generator `g`, and it determines how many exact jumps reach `b`

That second direction only works when the resulting jump count is an integer.

---

## 4. Example: `9`

Take:

$$
9
$$

With the exact ruler:

$$
a=2
$$

the hidden generator is:

$$
g=9^{1/2}=3
$$

So:

$$
9 = 3^2
$$

and the exact unfolding is:

```text
1 -> 3 -> 9
```

Here the generator is unique among nontrivial integer generators.

---

## 5. Example: `27`

Now take:

$$
27
$$

With the exact ruler:

$$
a=3
$$

the hidden generator is:

$$
g=27^{1/3}=3
$$

So:

$$
27=3^3
$$

and the unfolding is:

```text
1 -> 3 -> 9 -> 27
```

Again, the generator is `3`, but the ruler is different.

This is why generator and ruler should not be confused.

The same generator may appear under different exact depths.

---

## 6. Example: `64`

This is the main example of the note.

Since:

$$
64 = 8^2 = 4^3 = 2^6
$$

the endpoint `64` admits several hidden generators:

- `8` under ruler `a=2`
- `4` under ruler `a=3`
- `2` under ruler `a=6`

So the generator is not always unique.

What changes is the depth of the exact unfolding:

```text
g=8  ->  1 -> 8 -> 64
g=4  ->  1 -> 4 -> 16 -> 64
g=2  ->  1 -> 2 -> 4 -> 8 -> 16 -> 32 -> 64
```

So the same endpoint may hide a family of generators, each one producing a different exact resolution.

---

## 7. Why Smaller Generators Give Deeper Phase Unfoldings

For a fixed endpoint `B`, suppose:

$$
B=g^a
$$

If `g` is larger, fewer jumps are needed.

If `g` is smaller, more jumps are needed.

So for the same endpoint:

- larger hidden generator -> coarser exact unfolding
- smaller hidden generator -> deeper exact unfolding

This is exactly what happens with `64`:

- `8` reaches it fast
- `4` reaches it in more steps
- `2` reaches it with the deepest exact unfolding

Later we will formalize this with the prime-factor criterion.
For now, the structural picture is already enough.

---

## 8. Symmetry Under a Fixed Endpoint

This is one of the most structural parts of the whole theory.

Fix a coarse endpoint:

$$
B
$$

and consider all exact nontrivial pairs:

$$
\Sigma(B)
=
\left\{
(g,a)\in\mathbb{N}_{\ge 2}^2
\;\middle|\;
B=g^a
\right\}
$$

For a fixed endpoint `B`, neither `g` nor `a` is free.
They must comply with the same boundary:

$$
B=g^a
$$

So each side determines the other:

$$
g = B^{1/a},
\qquad
a = \log_g(B)
$$

This creates a real symmetry of constraint:

- `a` measures how many exact jumps fit in the span
- `g` measures how strong each jump branches locally

If `a` increases, `g` must decrease.
If `g` increases, `a` must decrease.

So one and the same endpoint may be reached by:

- few large jumps
- or many small jumps

while still syncing at the same coarse boundary `B`.

This is not a symmetry by simple exchange of symbols.
It is a structural symmetry under a shared restriction.

You may think of `B` as the fixed outer boundary, and of `g` and `a` as two variables forced to adjust to each other inside that boundary.

For `64`, the exact nontrivial pair set is:

$$
\Sigma(64)=\{(8,2),\;(4,3),\;(2,6)\}
$$

which can be read as:

```text
g:  8   4   2
a:  2   3   6
```

So as the hidden generator shrinks, the admissible exact depth grows.
That is the symmetry.

There is also a natural finiteness bound.

Since:

$$
B=g^a
\qquad\text{and}\qquad
g\ge 2
$$

we must have:

$$
2^a \le B
$$

hence:

$$
a \le \log_2(B)
$$

So for a fixed endpoint, the exact pair family is always finite.

This matters conceptually:

- the endpoint fixes a finite structural field of admissible exact generators
- the deepest exact unfolding is not arbitrary
- the smallest exact generator and the largest exact ruler come together

---

## 9. Why Not `16` for `64`?

This is a useful boundary case.

`16` does lie on the same shared line:

```text
1, 2, 4, 8, 16, 32, 64
```

But it is not a hidden generator for endpoint `64`.

Why?

Because there is no integer `a \ge 2` such that:

$$
64 = 16^a
$$

In fact:

$$
\log_{16}(64)=\frac{3}{2}
$$

So `16` reaches `64` only at a fractional jump count.

That means `16` is visible on the shared line, but it does not generate `64` by an exact integer number of its own jumps.

However, `16` does become a hidden generator for a later endpoint:

$$
256 = 16^2
$$

So being on the line is not enough.
The endpoint must sync with the candidate generator at an integer jump count.

---

## 10. Generator Families

For an endpoint `B`, it is useful to name the full family of exact hidden generators:

$$
\Gamma(B)
=
\left\{
g \in \mathbb{N}_{\ge 2}
\;\middle|\;
\exists a \in \mathbb{N}_{\ge 2}
\text{ such that }
B=g^a
\right\}
$$

This set may be:

- empty, if `B` has no nontrivial exact generator
- a singleton, if `B` has exactly one nontrivial generator
- a family, if `B` admits several exact unfoldings

Examples:

$$
\Gamma(12)=\varnothing
$$

$$
\Gamma(9)=\{3\}
$$

$$
\Gamma(27)=\{3\}
$$

$$
\Gamma(64)=\{2,4,8\}
$$

So the generator family is the clean way to describe all exact coarse-to-fine views of one endpoint.

---

## 11. Nested Hidden Generators

A hidden generator may itself contain a deeper hidden generator.

Example:

$$
4096 = 64^2 = 8^4 = 4^6 = 2^{12}
$$

So `4096` can be unfolded in stages.

One possible nested zoom is:

```text
4096 -> 64 -> 8 -> 2
```

This should not be read as subtraction or division.
It is a chain of exact hidden generators under repeated zoom.

At each stage, the currently visible endpoint becomes the coarse jump for a finer local ruler.

This nested behavior is one reason the hidden-generator idea is so useful.

---

## 12. Hidden Generator vs Coarse Base

It is important not to confuse these two.

The coarse base is the object we start by looking at.

The hidden generator is the finer local base revealed by an exact ruler.

So if:

$$
64 = 2^6
$$

then:

- `64` is the coarse endpoint in one view
- `2` is the finest hidden generator in another view

Neither one is "the real one" in an absolute sense.
They belong to different resolutions of the same structure.

---

## 13. What This Note Has Added

We can now summarize the hidden-generator idea.

1. An exact ruler produces a first exact phase value:
   $$
   g=b^{1/a}
   $$
2. That value is not only a node count.
   It is also a new local branching base.
3. One endpoint may admit one, many, or no hidden generators.
4. Smaller hidden generators produce deeper exact unfoldings.
5. A candidate value is only a generator if it reaches the endpoint at an integer jump count.

So the hidden generator is the local base that was already structurally inside the coarse jump.

---

## 14. Next Note

Now that the generator object is clear, the next step is to formalize the exact relation:

$$
B = g^a
$$

as its own principle.

That will be the topic of the next paper on perfect-power unfolding.
