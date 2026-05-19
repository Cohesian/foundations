# 2. Linear Combination, Span, And Rank

## Linear Combination

Linear algebra is mostly about scaling vectors and summing them.

Given:

$$
u =
\begin{bmatrix}
1 \\
0
\end{bmatrix},
\quad
v =
\begin{bmatrix}
0 \\
1
\end{bmatrix}
$$

we can make:

$$
au + bv
$$

where $a$ and $b$ are scalar knobs.

So:

$$
au + bv =
a
\begin{bmatrix}
1 \\
0
\end{bmatrix}
+
b
\begin{bmatrix}
0 \\
1
\end{bmatrix}
=
\begin{bmatrix}
a \\
b
\end{bmatrix}
$$

With two independent knobs, we can reach the whole 2D plane.

## Span

The span of vectors is everything reachable by scaling and summing them.

$$
\text{span}(u,v) = \{au + bv \mid a,b \in \mathbb{R}\}
$$

Plain:

> span is the reachable mesh.

Examples:

- one nonzero vector spans a line.
- two non-collinear vectors span a plane.
- three independent vectors in 3D span full 3D.

## Redundant Vector

Let:

$$
e_1 =
\begin{bmatrix}
1 \\
0
\end{bmatrix},
\quad
e_2 =
\begin{bmatrix}
0 \\
1
\end{bmatrix},
\quad
m =
\begin{bmatrix}
1 \\
1
\end{bmatrix}
$$

Then:

$$
m = e_1 + e_2
$$

So $m$ is useful, but not independent.

Any scaled version of $m$ can be recreated:

$$
sm = s(e_1 + e_2)
$$

Distribute:

$$
sm = se_1 + se_2
$$

So $m$ adds no new reachable dimension.

It is a shortcut direction inside a space we already had.

## Different Scalars Can Move Inside The Same Plane

If:

$$
c_1 =
\begin{bmatrix}
1 \\
0 \\
1
\end{bmatrix},
\quad
c_3 =
\begin{bmatrix}
0 \\
1 \\
1
\end{bmatrix}
$$

then:

$$
\alpha c_1 + \beta c_3
$$

can move in many directions inside the plane spanned by $c_1$ and $c_3$.

But it is still trapped inside that plane.

If:

$$
c_2 = c_1 + c_3 =
\begin{bmatrix}
1 \\
1 \\
2
\end{bmatrix}
$$

then $c_2$ also lives inside the same plane.

Adding $c_2$ can move your resulting vector inside the plane, but it cannot drift the plane itself.

## Rank

Rank means:

> dimension mobility.

Or:

> how many independent directions the columns give you.

In 3D:

- rank $0$: no mobility, stuck at origin.
- rank $1$: line mobility.
- rank $2$: plane mobility.
- rank $3$: full 3D mobility.

Example:

$$
M =
\begin{bmatrix}
1 & 1 & 0 \\
0 & 1 & 1 \\
1 & 2 & 1
\end{bmatrix}
$$

Columns:

$$
c_1 =
\begin{bmatrix}
1 \\
0 \\
1
\end{bmatrix},
\quad
c_2 =
\begin{bmatrix}
1 \\
1 \\
2
\end{bmatrix},
\quad
c_3 =
\begin{bmatrix}
0 \\
1 \\
1
\end{bmatrix}
$$

But:

$$
c_2 = c_1 + c_3
$$

So $c_2$ is redundant.

The matrix has only two independent directions.

$$
\text{rank}(M) = 2
$$

