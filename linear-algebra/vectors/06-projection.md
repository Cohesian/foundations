# 6. Projection

Projection is the next knot.

The best intuition:

> projection is the closest reachable version of something outside a span.

## Point To Line

Imagine a line $L$ and a point $P$ not on that line.

Projection asks:

> which point $Q$ on $L$ is closest to $P$?

The answer is the perpendicular hit.

Why?

If $R$ is any other point on the line, then $PQR$ forms a right triangle.

The diagonal $PR$ is longer than the perpendicular segment $PQ$.

So $Q$ is closest.

## Shadow Intuition

Projection is also like a shadow.

But the usual math projection means an orthogonal shadow:

> light rays hit the line or plane at $90^\circ$.

Oblique projection exists too, but it depends on the chosen ray direction.

Orthogonal projection is special because it gives the closest point.

## Projection Onto A Line

Let a line direction be:

$$
u =
\begin{bmatrix}
1 \\
-1
\end{bmatrix}
$$

Every point on that line looks like:

$$
p(s) = su
$$

So:

$$
p(s) =
s
\begin{bmatrix}
1 \\
-1
\end{bmatrix}
=
\begin{bmatrix}
s \\
-s
\end{bmatrix}
$$

Now take:

$$
d =
\begin{bmatrix}
4 \\
-2
\end{bmatrix}
$$

$d$ is not on the line because points on the line must satisfy $y=-x$.

Projection asks:

> what point on the line is closest to $d$?

The answer is:

$$
\text{proj}_u(d) =
\frac{d \cdot u}{u \cdot u}u
$$

The scalar:

$$
\frac{d \cdot u}{u \cdot u}
$$

means:

> how much of $d$ points along $u$, adjusted for the length of $u$.

Compute:

$$
d \cdot u =
4(1) + (-2)(-1)
=
6
$$

$$
u \cdot u =
1^2 + (-1)^2
=
2
$$

So:

$$
\frac{d \cdot u}{u \cdot u} = 3
$$

Projection:

$$
\text{proj}_u(d) = 3u =
\begin{bmatrix}
3 \\
-3
\end{bmatrix}
$$

The leftover is:

$$
e = d - \text{proj}_u(d)
$$

$$
e =
\begin{bmatrix}
4 \\
-2
\end{bmatrix}
-
\begin{bmatrix}
3 \\
-3
\end{bmatrix}
=
\begin{bmatrix}
1 \\
1
\end{bmatrix}
$$

And:

$$
e \cdot u = 0
$$

So the leftover is perpendicular to the line.

That is the signature of orthogonal projection.

## Projection Onto A Plane

If a plane has orthogonal basis vectors $u$ and $v$, then a vector $d$ can be projected onto that plane by keeping its $u$ and $v$ parts.

If:

$$
u =
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix},
\quad
v =
\begin{bmatrix}
0 \\
0 \\
1
\end{bmatrix}
$$

and:

$$
d =
\begin{bmatrix}
4 \\
-2 \\
3
\end{bmatrix}
$$

then:

$$
s = \frac{d \cdot u}{u \cdot u}
$$

$$
t = \frac{d \cdot v}{v \cdot v}
$$

These are local coordinates of the projected vector.

Compute:

$$
s = 3
$$

$$
t = 3
$$

So the projected in-plane vector is:

$$
d_{plane} = 3u + 3v
$$

$$
d_{plane} =
\begin{bmatrix}
3 \\
-3 \\
3
\end{bmatrix}
$$

The leftover:

$$
d - d_{plane}
=
\begin{bmatrix}
1 \\
1 \\
0
\end{bmatrix}
$$

is perpendicular to the plane.

## Local Coordinate View

Projection is easiest after changing coordinates.

If a line is local $x$-axis:

$$
(x,y) \rightarrow (x,0)
$$

If a plane is local $xy$-plane:

$$
(x,y,z) \rightarrow (x,y,0)
$$

Plain:

> drop the coordinate pointing away from the space.

