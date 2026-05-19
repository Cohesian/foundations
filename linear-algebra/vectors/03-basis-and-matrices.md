# 3. Basis And Matrices

## Standard Basis

In 3D, the usual global basis is:

$$
i =
\begin{bmatrix}
1 \\
0 \\
0
\end{bmatrix},
\quad
j =
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix},
\quad
k =
\begin{bmatrix}
0 \\
0 \\
1
\end{bmatrix}
$$

So:

$$
\begin{bmatrix}
2 \\
3 \\
4
\end{bmatrix}
=
2i + 3j + 4k
$$

## Identity Matrix

The identity matrix stores the standard basis as columns:

$$
I =
\begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

Applying identity changes nothing:

$$
I
\begin{bmatrix}
2 \\
3 \\
4
\end{bmatrix}
=
\begin{bmatrix}
2 \\
3 \\
4
\end{bmatrix}
$$

The inverse of doing nothing is doing nothing:

$$
I^{-1} = I
$$

## Matrix As Basis Encoder

A matrix can store basis vectors as columns.

If:

$$
B =
\begin{bmatrix}
| & | & | \\
u & v & w \\
| & | & |
\end{bmatrix}
$$

then:

$$
B
\begin{bmatrix}
a \\
b \\
c
\end{bmatrix}
=
au + bv + cw
$$

So $B$ translates local scalars into global coordinates.

Important: the columns of $B$ are already written as global/world vectors.

That means this expression:

$$
B p_{local}
$$

already produces a displacement in the global world.

The anchor $A$ does not change how $B$ stretches or rotates that displacement.

The anchor only places the already-global displacement somewhere in the world:

$$
p_{global} = A + B p_{local}
$$

## Matrix As Transformation

The same matrix can also be viewed as transforming a vector.

Example:

$$
B =
\begin{bmatrix}
2 & 0 \\
0 & 3
\end{bmatrix}
$$

Then:

$$
B
\begin{bmatrix}
1 \\
1
\end{bmatrix}
=
\begin{bmatrix}
2 \\
3
\end{bmatrix}
$$

Transformation view:

> $(1,1)$ got stretched into $(2,3)$.

Basis view:

> local coordinates $(1,1)$ mean global point $(2,3)$ in this basis.

Both are valid.

## Inverse Matrix

The inverse matrix is the undo machine.

If:

$$
B x = y
$$

then:

$$
B^{-1} y = x
$$

For:

$$
B =
\begin{bmatrix}
2 & 0 \\
0 & 3
\end{bmatrix}
$$

the inverse is:

$$
B^{-1} =
\begin{bmatrix}
\frac{1}{2} & 0 \\
0 & \frac{1}{3}
\end{bmatrix}
$$

because scaling by $2$ is undone by multiplying by $\frac{1}{2}$, and scaling by $3$ is undone by multiplying by $\frac{1}{3}$.

So:

$$
B^{-1}
\begin{bmatrix}
2 \\
3
\end{bmatrix}
=
\begin{bmatrix}
1 \\
1
\end{bmatrix}
$$

## Why Reciprocals Undo Scaling

The reason $\frac{1}{2}$ undoes $2$, and $\frac{1}{3}$ undoes $3$, is proportional.

Start with one unit segment $a$:

```text
___
```

Scaling by $3$ means making three equal copies of that unit:

```text
___ | ___ | ___
```

So:

$$
y = 3a
$$

The result $y$ looks like one larger segment, but it is made of three equal parts.

To recover the original unit $a$, take one of those three equal parts:

$$
a = \frac{1}{3}y
$$

So:

$$
\frac{1}{3}(3a) = a
$$

More generally, if a quantity is scaled by $b$:

$$
y = ba
$$

then the undo operation is taking the $\frac{1}{b}$ part of the result:

$$
a = \frac{1}{b}y
$$

So:

$$
\frac{1}{b}(ba) = a
$$

This is why a scaling matrix uses reciprocal values in its inverse.

If a basis vector was stretched by $2$, the inverse takes half.

If a basis vector was stretched by $3$, the inverse takes a third.

Plain:

> scaling makes a bigger segment from equal parts; the reciprocal asks for the original one-part unit again.


## Anchored Basis

For points, we usually need an anchor/origin $A$.

This is where one distinction matters a lot:

- a **displacement** is a movement amount.
- a **point** is a location in the world.

A basis matrix $B$ naturally transforms displacements:

$$
d_{global} = B d_{local}
$$

So if the displacement is already isolated, we can invert directly:

$$
d_{local} = B^{-1} d_{global}
$$

No anchor is needed there.

But an anchored point has two pieces:

$$
p_{global} = A + B p_{local}
$$

Read this as:

> global point = anchor bias + basis-transformed local displacement.

The term $B p_{local}$ is the displacement from the anchor.

The term $A$ places that displacement somewhere in the world.

So to decode a global point back into local coordinates, we must undo those two pieces in reverse order.

First remove the anchor bias:

$$
p_{global} - A = B p_{local}
$$

Now the displacement is isolated.

Then undo the basis transform:

$$
B^{-1} (p_{global} - A) = p_{local}
$$

So:

$$
p_{local} = B^{-1} (p_{global} - A)
$$

Plain:

> remove anchor bias, then undo basis transform.

## Anchored Basis In 1D

Use a tiny 1D example.

Let the anchor be:

$$
A = 10
$$

Let the basis scale be:

$$
B = 2
$$

Let the local coordinate be:

$$
p_{local} = 3
$$

Local to global:

$$
p_{global} = A + B p_{local}
$$

So:

$$
p_{global} = 10 + 2(3) = 16
$$

The global point is $16$.

But $16$ contains two things:

- the anchor bias $10$.
- the transformed local displacement $2(3)=6$.

To recover the local coordinate, first subtract the anchor:

$$
p_{global} - A = 16 - 10 = 6
$$

Now $6$ is the isolated transformed displacement.

Then undo the scale by multiplying by $\frac{1}{2}$:

$$
B^{-1} (p_{global} - A) = \frac{1}{2}(6) = 3
$$

So:

$$
p_{local} = 3
$$

This matches the original local coordinate.

## Why Not Invert First?

If we invert the global point directly:

$$
B^{-1} p_{global} = \frac{1}{2}(16) = 8
$$

But $8$ is not the local coordinate.

Why?

Because we also inverted the anchor bias.

The global point was:

$$
p_{global} = A + B p_{local}
$$

So:

$$
B^{-1} p_{global} = B^{-1} (A + B p_{local})
$$

Distribute:

$$
B^{-1} p_{global} = B^{-1} A + B^{-1} B p_{local}
$$

So:

$$
B^{-1} p_{global} = B^{-1} A + p_{local}
$$

The extra term is:

$$
B^{-1} A
$$

This is the anchor expressed in local units.

In the 1D example:

$$
B^{-1} A = \frac{1}{2}(10) = 5
$$

So direct inversion gave:

$$
8 = 5 + 3
$$

It contains:

- $5$: the anchor in local units.
- $3$: the local point we wanted.

To fix that path, we would have to subtract the inverted anchor too:

$$
p_{local} = B^{-1} p_{global} - B^{-1} A
$$

This is equivalent to:

$$
p_{local} = B^{-1} (p_{global} - A)
$$

But subtracting $A$ first is easier to understand because it says:

> isolate the displacement from the anchor before decoding it.

## Points Versus Displacements

If you have only a displacement:

$$
d_{global} = B d_{local}
$$

then:

$$
d_{local} = B^{-1} d_{global}
$$

But if you have an anchored point:

$$
p_{global} = A + B p_{local}
$$

then:

$$
p_{local} = B^{-1} (p_{global} - A)
$$

Same inverse matrix, different object.

The anchor matters only because it was already added into the final global point.

