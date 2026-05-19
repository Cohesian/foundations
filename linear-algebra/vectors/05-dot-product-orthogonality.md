# 5. Dot Product And Orthogonality

## Direction Agreement

The dot product measures directional agreement.

If two vectors point in similar directions, their dot product is positive.

If they point in opposite directions, their dot product is negative.

If they are perpendicular, their dot product is zero.

## Formula

For:

$$
a =
\begin{bmatrix}
a_x \\
a_y \\
a_z
\end{bmatrix},
\quad
b =
\begin{bmatrix}
b_x \\
b_y \\
b_z
\end{bmatrix}
$$

the dot product is:

$$
a \cdot b = a_xb_x + a_yb_y + a_zb_z
$$

Example:

$$
\begin{bmatrix}
1 \\
1 \\
0
\end{bmatrix}
\cdot
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix}
=
1(1) + 1(-1) + 0(0)
=
0
$$

So these vectors are orthogonal.

## Why $90^\circ$ Is Special

The geometric dot product is:

$$
a \cdot b = \|a\|\|b\|\cos(\theta)
$$

At $90^\circ$:

$$
\cos(90^\circ) = 0
$$

So:

$$
a \cdot b = 0
$$

This means no directional agreement.

Plain:

> walking east does not move you north.

## Independent Directions

Orthogonal directions are independent in the cleanest way.

If:

$$
u \cdot v = 0
$$

then movement along $u$ does not help or oppose movement along $v$.

This is why orthogonal bases are easier to work with.

## Normal Vector

For a plane spanned by $u$ and $v$, the normal vector is:

$$
n = u \times v
$$

The normal is perpendicular to the plane.

If a vector $d$ lies inside the plane, then:

$$
d \cdot n = 0
$$

If:

$$
d \cdot n \neq 0
$$

then $d$ has some component outside the plane.

