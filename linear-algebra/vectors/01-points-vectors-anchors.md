# 1. Points, Vectors, And Anchors

## Point

A point is a location.

In 3D:

$$
P =
\begin{bmatrix}
x \\
y \\
z
\end{bmatrix}
$$

Example:

$$
P =
\begin{bmatrix}
2 \\
1 \\
0
\end{bmatrix}
$$

This says: there is a location at $x=2$, $y=1$, $z=0$.

## Vector

A vector is a displacement or direction.

If:

$$
A =
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix}
$$

and:

$$
B =
\begin{bmatrix}
1 \\
0 \\
0
\end{bmatrix}
$$

then the vector from $A$ to $B$ is:

$$
u = B - A
$$

So:

$$
u =
\begin{bmatrix}
1 \\
0 \\
0
\end{bmatrix}
-
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix}
=
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix}
$$

This vector says:

> move $1$ in $x$, move $-1$ in $y$, move $0$ in $z$.

## Same Numbers, Two Meanings

The same tuple can be read as either a point or a vector.

$$
\begin{bmatrix}
2 \\
1 \\
0
\end{bmatrix}
$$

As a point:

> location $(2,1,0)$.

As a vector:

> move by $(2,1,0)$.

Context decides.

## Anchored Vector

Sometimes we want a vector that starts at a specific point.

If anchor/origin is $A$, and direction is $u$, then a point along that vector is:

$$
P(s) = A + su
$$

$s$ is a scalar knob.

If:

$$
A =
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix},
\quad
u =
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix}
$$

then:

$$
P(s) =
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix}
+
s
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix}
$$

When $s=0$:

$$
P(0) = A
$$

When $s=1$:

$$
P(1) = A + u
$$

When $s=\frac{1}{2}$:

$$
P\left(\frac{1}{2}\right) = A + \frac{1}{2}u
$$

## Mental Model

Point:

> Where am I?

Vector:

> How do I move?

Anchor:

> From where do I start measuring?

Scalar:

> How much of this direction do I take?

