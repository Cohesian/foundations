# Formula Sheet

## Vector From Point To Point

$$
v = B - A
$$

## Linear Combination

$$
p = a_1v_1 + a_2v_2 + \cdots + a_nv_n
$$

## Span

$$
\text{span}(v_1,\ldots,v_n)
=
\{a_1v_1 + \cdots + a_nv_n \mid a_i \in \mathbb{R}\}
$$

## Matrix With Basis Columns

$$
B =
\begin{bmatrix}
| & | & | \\
u & v & w \\
| & | & |
\end{bmatrix}
$$

## Local To Global

For vectors:

$$
p_{global} = B p_{local}
$$

For points with anchor $A$:

$$
p_{global} = A + B p_{local}
$$

## Global To Local

For vectors:

$$
p_{local} = B^{-1} p_{global}
$$

For points with anchor $A$:

$$
p_{local} = B^{-1} (p_{global} - A)
$$

## Dot Product

$$
a \cdot b = a_xb_x + a_yb_y + a_zb_z
$$

Geometric form:

$$
a \cdot b = \|a\|\|b\|\cos(\theta)
$$

## Orthogonality

$$
a \cdot b = 0
$$

means $a$ and $b$ are perpendicular.

## Length

$$
\|v\| = \sqrt{v \cdot v}
$$

In coordinates:

$$
\|v\| = \sqrt{x^2 + y^2 + z^2}
$$

## Unit Direction

$$
\hat{v} = \frac{v}{\|v\|}
$$

## Projection Onto A Line

Projection of $d$ onto the line direction $u$:

$$
\text{proj}_u(d) =
\frac{d \cdot u}{u \cdot u}u
$$

If $u$ is unit length:

$$
\text{proj}_u(d) = (d \cdot u)u
$$

## Projection Onto A Plane By Normal

If $n$ is a unit normal:

$$
d_{plane} = d - (d \cdot n)n
$$

If $n$ is not unit length:

$$
d_{plane} = d - \frac{d \cdot n}{n \cdot n}n
$$

## Plane Membership

If $n$ is normal to a plane, then $d$ lies in the plane when:

$$
d \cdot n = 0
$$

## Normal From Two Plane Vectors

$$
n = u \times v
$$

## Determinant

In 3D, determinant measures signed volume.

$$
\det[u \ v \ w]
$$

If:

$$
\det[u \ v \ w] = 0
$$

then the vectors do not span full 3D.

## Rank

Rank counts independent directions.

```text
rank 0 -> point/no mobility
rank 1 -> line mobility
rank 2 -> plane mobility
rank 3 -> 3D mobility
```

