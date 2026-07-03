# Discrete Phase Rulers

> A phase ruler does not change the base.
> It changes how finely one coarse exponential jump is inspected.

This note continues [F-01-branching-depth-resolution.md](F-01-branching-depth-resolution.md).

The previous paper introduced the main idea:

$$
b^{n/a}
=
\left(b^{1/a}\right)^n
$$

This second note slows down around one specific question:

> what exactly is a phase ruler, and why does everything begin at `1/a`?

---

## 1. One Coarse Jump

Every base begins with the same coarse frame:

$$
b^0 = 1,
\qquad
b^1 = b
$$

So the first full jump is:

```text
1 -> b
```

A phase ruler does not replace this jump.
It only cuts it into equal exponent slices.

If the chosen ruler is `a`, then the coarse exponent interval `[0,1]` is cut into:

$$
0,\quad \frac{1}{a},\quad \frac{2}{a},\quad \dots,\quad \frac{a}{a}
$$

This is the whole idea of the ruler.

---

## 2. Phase Coordinates

For a chosen ruler `a`, define its phase coordinates:

$$
\Phi_a
=
\left\{
\frac{k}{a}
\;\middle|\;
k=0,1,\dots,a
\right\}
$$

These are not yet node counts.
They are only positions inside one coarse exponential jump.

The corresponding phase-value sequence for base `b` is:

$$
\mathcal{P}_b^{(a)}
=
\left\{
b^{k/a}
\;\middle|\;
k=0,1,\dots,a
\right\}
$$

So the ruler lives in exponent space, and the phase-value sequence lives in value space.

That distinction matters.

---

## 3. Why `1/a` Is Primitive

The most important coordinate is:

$$
\frac{1}{a}
$$

because it is the first positive phase on that ruler.

Every other phase is only repeated accumulation of that same unit:

$$
\frac{2}{a}=2\cdot\frac{1}{a},
\qquad
\frac{3}{a}=3\cdot\frac{1}{a},
\qquad
\dots,
\qquad
\frac{a}{a}=1
$$

So:

- `1/a` is primitive
- `2/a` is already two primitive phase steps
- `5/35` is not fundamental; it is the fifth phase on a `35`-slice ruler

This is why we test the phase sequence at:

$$
b^{1/a}
$$

before testing any later phase.

---

## 4. The First Phase Step

Once the ruler `a` has been chosen, the first phase value is:

$$
b^{1/a}
$$

This is the first micro-jump inside the coarse jump `1 -> b`.

It is the decisive value.

If it is exact and lands in the natural numbers, then it becomes a valid hidden generator:

$$
g = b^{1/a}
$$

and then:

$$
b^{k/a}=g^k
$$

So one first exact micro-jump is enough to organize the entire phase sequence.

This is where the anchor law matters again.

Because:

$$
g^1 = g
$$

the first exact phase value is not only a node count at depth `1/a`.
It can also be treated as the new local branching base for that ruler.

So the first phase reveals both:

- the size of the first exact micro-layer
- the finer base that generates the rest of the exact phase sequence

If the first phase step fails, the whole ruler fails as an exact discrete ruler.

---

## 5. Exact and Nonexact Rulers

This gives the central dichotomy of the note.

### 5.1 Exact ruler

A ruler `a` is exact for base `b` when:

$$
b^{1/a}\in\mathbb{N}
$$

Then every phase is exact:

$$
b^{0/a},\;
b^{1/a},\;
b^{2/a},\;
\dots,\;
b^{a/a}
$$

and the whole phase sequence can be rewritten with the hidden generator `g`.

### 5.2 Nonexact ruler

A ruler `a` is nonexact when:

$$
b^{1/a}\notin\mathbb{N}
$$

Then the phases still exist over the reals, but they do not define an exact discrete node-by-node phase sequence.

So the entire question collapses to a first-step test.

---

## 6. Example: Base `9`

Take:

$$
b=9,\qquad a=2
$$

Then the phase coordinates are:

$$
0,\quad \frac{1}{2},\quad \frac{2}{2}
$$

and the phase-value sequence is:

$$
9^0,\quad 9^{1/2},\quad 9^{2/2}
$$

which gives:

```text
1 -> 3 -> 9
```

because:

$$
9^{1/2}=3
$$

So the ruler `a=2` is exact.

And the hidden generator is:

$$
g=3
$$

This is the clearest case of a two-phase ruler.

---

## 7. Example: Base `27`

Now take:

$$
b=27,\qquad a=3
$$

Then the phase coordinates are:

$$
0,\quad \frac{1}{3},\quad \frac{2}{3},\quad \frac{3}{3}
$$

and the phase sequence becomes:

```text
1 -> 3 -> 9 -> 27
```

because:

$$
27^{1/3}=3,\qquad
27^{2/3}=9,\qquad
27^{3/3}=27
$$

So the cubic ruler is exact.

This matters because it shows that the phase idea is not tied to halves.

---

## 8. Example: Base `64`

This is where the note becomes richer.

Since:

$$
64 = 8^2 = 4^3 = 2^6
$$

the same endpoint admits several exact rulers.

With `a=2`:

```text
1 -> 8 -> 64
```

With `a=3`:

```text
1 -> 4 -> 16 -> 64
```

With `a=6`:

```text
1 -> 2 -> 4 -> 8 -> 16 -> 32 -> 64
```

So one and the same coarse jump may carry different exact phase resolutions.

This is one of the most important structural facts in the whole track.

It can also be read as a family of synchronized tempos:

```text
1, 2, 4, 8, 16, 32, 64
```

- base `64` marks only the endpoints
- base `8` lands every three steps of the base-`2` phase line
- base `4` lands every two steps of the base-`2` phase line
- base `2` fills the whole line

So a coarser base looks like a sparse rhythm, while a finer exact ruler fills more of the same path.
All of them still sync at `64`.

If we project all of them onto the finest exact line, the alignment becomes even clearer:

```text
level:  0   1   2   3   4   5   6
value:  1   2   4   8   16  32  64

b=64:   x                       x
b=8:    x           x           x
b=4:    x       x       x       x
b=2:    x   x   x   x   x   x   x
```

Here the levels are measured on the finest exact ruler, namely base `2`.

This is why the comparison can start to look almost linear:

- base `2` shows every exact jump
- base `4` lands every two of those jumps
- base `8` lands every three of those jumps
- base `64` only marks the full span

So the phases are linear in depth levels even when the resulting node counts are exponential.

One natural question is: why not `16`?

The answer is that `16` does lie on the shared line, but it does not sync exactly with the endpoint `64` by an integer number of its own jumps.

Indeed:

$$
64 \neq 16^m
\qquad
\text{for any integer } m \ge 2
$$

More precisely:

$$
\log_{16}(64)=\frac{3}{2}
$$

So `16` reaches `64` only at a fractional exponent, not at an exact integer jump count.
That is why `16` is not an exact ruler for endpoint `64`, even though it becomes one for a later endpoint such as:

$$
256 = 16^2
$$

---

## 9. Primitive vs Accumulated Phase

Now we can say this clearly.

The primitive question is:

$$
b^{1/a}
$$

The accumulated question is:

$$
b^{n/a}
$$

But the second only makes sense after the first one has been stabilized.

So:

- `1/a` asks for the first exact micro-jump
- `n/a` asks how far we travel on that same ruler

That is why a value like `2/4` may be valid, but it is not primitive.

It is already:

$$
2\cdot\frac{1}{4}
$$

So the phase theory always starts with the first phase, not with a later accumulated one.

---

## 10. Phases Outside the First Window

So far the phase ruler has been presented on the first exponent interval:

$$
0 \le e \le 1
$$

But this is only the first window.

The same ruler can be shifted to any later interval:

$$
m \le e \le m+1
$$

for integer `m`.

Then the phase points are:

$$
b^m,\quad
b^{m+1/a},\quad
b^{m+2/a},\quad
\dots,\quad
b^{m+1}
$$

So phases are attached to depth windows, not only to the origin.

---

## 11. Phases Inside Later Jumps

The same idea reappears after the origin.

For example, on the base-`9` depth path:

```text
9 -> 81
```

is one coarse jump from:

$$
9^1 \to 9^2
$$

If we inspect that jump with the same two-phase ruler, we get:

$$
9^1,\qquad
9^{3/2},\qquad
9^2
$$

which becomes:

```text
9 -> 27 -> 81
```

So the phase ruler is not only about the first coarse jump from the origin.
It can also reveal exact intermediate layers inside later jumps of the same depth path.

This will matter more in the later note on local spans.

One more example makes the depth reading even clearer.

Inside the base-`64` depth path, the interval

$$
64^1 \to 64^2
$$

can also be cut by the two-phase ruler.

Then the phase points are:

$$
64^1,\qquad 64^{3/2},\qquad 64^2
$$

and:

$$
64^{3/2}=64\cdot 64^{1/2}=64\cdot 8=512
$$

So:

```text
64 -> 512 -> 4096
```

This is important because the halfway phase is halfway in exponent steps, not halfway in the final value.
Phase rulers are linear in depth position, not linear in absolute node count.

---

## 12. What This Note Has Added

The previous paper introduced fractional exponents as depth rulers.

This note adds four refinements:

1. a ruler is a partition of the exponent interval `[0,1]`
2. the phase coordinate `1/a` is always primitive
3. exactness is decided entirely by the first phase step `b^{1/a}`
4. later phases are only accumulated repetitions of that primitive step

So the first clean rule of the theory is now:

> a phase ruler is exact if and only if its first phase step is exact.

---

## 13. Next Note

The next natural question is no longer what a ruler is.

It is:

> what exactly is the hidden generator that appears when a ruler is exact?

That will be the subject of the next paper.
