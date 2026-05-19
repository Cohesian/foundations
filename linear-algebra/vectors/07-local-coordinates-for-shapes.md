# 7. Local Coordinates For Shapes

## Shape As Anchor Plus Basis

A tilted square in 3D can be described by:

- anchor/origin $A$
- local basis vector $u$
- local basis vector $v$
- scalar bounds

Example:

$$
A =
\begin{bmatrix}
0 \\
1 \\
0
\end{bmatrix}
$$

$$
u =
\begin{bmatrix}
1 \\
-1 \\
0
\end{bmatrix}
$$

$$
v =
\begin{bmatrix}
0 \\
0 \\
1
\end{bmatrix}
$$

Any point on the square's plane can be written:

$$
P(s,t) = A + su + tv
$$

## Corner-Origin Square

If the square starts at corner $A$, then:

$$
0 \leq s \leq 1
$$

$$
0 \leq t \leq 1
$$

Corners:

$$
P(0,0) = A
$$

$$
P(1,0) = A + u
$$

$$
P(0,1) = A + v
$$

$$
P(1,1) = A + u + v
$$

## Centered Square

If $A$ is the center of the square, then:

$$
-\frac{1}{2} \leq s \leq \frac{1}{2}
$$

$$
-\frac{1}{2} \leq t \leq \frac{1}{2}
$$

Corners:

$$
A + \frac{u}{2} + \frac{v}{2}
$$

$$
A + \frac{u}{2} - \frac{v}{2}
$$

$$
A - \frac{u}{2} + \frac{v}{2}
$$

$$
A - \frac{u}{2} - \frac{v}{2}
$$

## Boundary Of A Centered Rectangle

Suppose the shape uses local coordinates:

$$
P(s,t) = A + su + tv
$$

and bounds:

$$
-\frac{w}{2} \leq s \leq \frac{w}{2}
$$

$$
-\frac{h}{2} \leq t \leq \frac{h}{2}
$$

If a direction in local coordinates is:

$$
d_{local} =
\begin{bmatrix}
d_s \\
d_t
\end{bmatrix}
$$

then scale it until the first bound is hit.

Candidate scale for $s$ wall:

$$
\lambda_s =
\frac{w/2}{|d_s|}
$$

Candidate scale for $t$ wall:

$$
\lambda_t =
\frac{h/2}{|d_t|}
$$

Use:

$$
\lambda = \min(\lambda_s, \lambda_t)
$$

Then:

$$
s_{hit} = \lambda d_s
$$

$$
t_{hit} = \lambda d_t
$$

World boundary point:

$$
P_{hit} = A + s_{hit}u + t_{hit}v
$$

## Why Local Coordinates Help

The global world may be tilted and confusing.

But inside the shape's own basis, a square is just:

$$
-\frac{1}{2} \leq s \leq \frac{1}{2}
$$

$$
-\frac{1}{2} \leq t \leq \frac{1}{2}
$$

So the workflow is:

1. Translate into local coordinates.
2. Do simple boundary math.
3. Translate back to global coordinates.

