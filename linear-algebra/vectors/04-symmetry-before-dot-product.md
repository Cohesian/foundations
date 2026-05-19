# 4. Symmetry Before Dot Product

This chapter is intentionally before dot product.

The goal is not to memorize:

$$
u \cdot v = 0
$$

The goal is to understand what direction symmetry is trying to say before formulas compress it.

## The Primitive Picture

A vector has two ideas mixed together:

- **direction**: where it points.
- **magnitude**: how long it is.

For now, we mostly ignore magnitude.

Think of all nonzero movements as simple direction choices.

In 1D, there are only two directions:

```text
left      right
<---- 0 ---->
```

In 2D, there are infinitely many directions around the origin:

```text
        up
        ^
        |
left <--0--> right
        |
        v
       down
```

In 3D, directions live around the origin in all spatial ways, not just on a flat circle.

The origin is the anchor of direction thinking.

A vector says:

> from the origin, move this way.

## Direction Without Magnitude

If we ignore magnitude, then these two vectors have the same direction:

$$
\begin{bmatrix}
1 \\
2
\end{bmatrix}
\quad
\text{and}
\quad
\begin{bmatrix}
2 \\
4
\end{bmatrix}
$$

because:

$$
\begin{bmatrix}
2 \\
4
\end{bmatrix}
=
2
\begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

One is just a longer version of the other.

Direction-only thinking treats them as living on the same ray.

## Opposite Direction

The opposite of a vector is made by flipping every component.

If:

$$
u =
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

then:

$$
-u =
\begin{bmatrix}
-x \\
-y
\end{bmatrix}
$$

This is a $180^\circ$ turn.

Example:

$$
\begin{bmatrix}
1 \\
2
\end{bmatrix}
\rightarrow
\begin{bmatrix}
-1 \\
-2
\end{bmatrix}
$$

Opposite does not mean perpendicular.

Opposite means:

> same line, reverse direction.

## 1D Symmetry

In 1D, a vector has only one component:

$$
[x]
$$

There are only two direction signs:

$$
[+1]
\quad
\text{and}
\quad
[-1]
$$

They are opposites.

There is no perpendicular direction inside 1D.

Why?

Because there is no second independent way to move.

In 1D:

```text
rank / mobility = line only
```

No sideways exists.

## 2D Sign Symmetry Toy

Now look at equal-magnitude diagonal directions.

Use only signs first:

$$
[+,+]
$$

The four sign patterns are:

$$
[+,+]
$$

$$
[-,-]
$$

$$
[+,-]
$$

$$
[-,+]
$$

For the vector $[1,1]$:

- $[1,1]$ is same direction.
- $[-1,-1]$ is opposite direction.
- $[1,-1]$ is perpendicular.
- $[-1,1]$ is also perpendicular.

Visually:

```text
        [-1,1]
           ^
           |
[-1,-1] <--0--> [1,1]
           |
           v
        [1,-1]
```

This symmetry is beautiful, but dangerous.

It works cleanly here because the magnitudes match:

$$
|x| = |y|
$$

The vector sits on a $45^\circ$ diagonal.

## Why Sign Symmetry Is Not Enough

For:

$$
u =
\begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

just flipping one sign gives:

$$
\begin{bmatrix}
1 \\
-2
\end{bmatrix}
$$

This is not generally perpendicular.

It is a reflection across the $x$-axis.

Reflection is not the same as a quarter-turn.

This is the trap:

> sign flips can describe symmetry, but they do not fully describe perpendicularity once magnitudes differ.

Magnitude starts changing the angle.

## Swap Alone Is Reflection

Take:

$$
u =
\begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

Swapping coordinates gives:

$$
\begin{bmatrix}
2 \\
1
\end{bmatrix}
$$

This is a reflection across the line $y=x$.

The line $y=x$ acts like a mirror.

Points sitting exactly on the mirror do not move:

$$
[1,1] \rightarrow [1,1]
$$

because swapping equal coordinates changes nothing.

But a point away from the mirror crosses to the symmetric position on the other side:

$$
[1,2] \rightarrow [2,1]
$$

The distance to the mirror is preserved, like a real reflection.

So:

$$
[x,y] \rightarrow [y,x]
$$

means mirror across the diagonal.

It does not mean perpendicular.

## Mirror Plus Flip

The perpendicular operation can be seen as two simpler moves:

1. mirror across $y=x$ by swapping coordinates.
2. flip one axis.

Start with:

$$
[x,y]
$$

Mirror across $y=x$:

$$
[x,y] \rightarrow [y,x]
$$

Now flip the new $y$ coordinate:

$$
[y,x] \rightarrow [y,-x]
$$

This gives the clockwise perpendicular direction.

Or flip the new $x$ coordinate:

$$
[y,x] \rightarrow [-y,x]
$$

This gives the counterclockwise perpendicular direction.

So perpendicularity in 2D can be remembered as:

> mirror, then flip one axis.

This is the same as:

> swap components, then flip exactly one sign.

For:

$$
u =
\begin{bmatrix}
1 \\
2
\end{bmatrix}
$$

mirror first:

$$
\begin{bmatrix}
1 \\
2
\end{bmatrix}
\rightarrow
\begin{bmatrix}
2 \\
1
\end{bmatrix}
$$

then flip one axis:

$$
\begin{bmatrix}
2 \\
1
\end{bmatrix}
\rightarrow
\begin{bmatrix}
2 \\
-1
\end{bmatrix}
$$

or:

$$
\begin{bmatrix}
2 \\
1
\end{bmatrix}
\rightarrow
\begin{bmatrix}
-2 \\
1
\end{bmatrix}
$$

Those are the two perpendicular directions.

The mirror alone gives symmetry.

The mirror plus an axis flip gives the quarter-turn.


## Axis Flips Are Also Mirrors

Flipping only one coordinate is also a reflection.

If we flip the $x$ coordinate:

$$
[x,y] \rightarrow [-x,y]
$$

that is a mirror across the $y$-axis.

The $y$-axis stays fixed, and the point folds to the other side horizontally.

If we flip the $y$ coordinate:

$$
[x,y] \rightarrow [x,-y]
$$

that is a mirror across the $x$-axis.

The $x$-axis stays fixed, and the point folds to the other side vertically.

So the perpendicular construction can be read as two reflections:

1. reflect across the diagonal mirror $y=x$.
2. reflect across one coordinate-axis mirror.

Start with:

$$
u = [x,y]
$$

After diagonal reflection, call the reflected vector:

$$
u_{mirror} = [y,x]
$$

Here the old $y$ now sits in the new $x$ coordinate, and the old $x$ now sits in the new $y$ coordinate.

Then flip the new $y$ coordinate:

$$
[y,x] \rightarrow [y,-x]
$$

This is reflection across the $x$-axis.

Or flip the new $x$ coordinate:

$$
[y,x] \rightarrow [-y,x]
$$

This is reflection across the $y$-axis.

So the two perpendiculars are:

$$
u_{cw} = [y,-x]
$$

and:

$$
u_{ccw} = [-y,x]
$$

The two-step geometry is:

```text
original vector
  -> mirror across y = x
  -> mirror across x-axis or y-axis
  -> perpendicular vector
```

This is why it feels like folding paper.

The first fold swaps the coordinate roles.

The second fold opposes one of the new coordinate directions.

Together they produce a $90^\circ$ turn.

## Quarter-Turn In 2D

A perpendicular direction in 2D is a quarter-turn.

A counterclockwise quarter-turn sends:

```text
right -> up
up    -> left
```

So if:

$$
u =
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

then counterclockwise perpendicular is:

$$
\begin{bmatrix}
-y \\
x
\end{bmatrix}
$$

Clockwise quarter-turn sends:

```text
right -> down
up    -> right
```

So clockwise perpendicular is:

$$
\begin{bmatrix}
y \\
-x
\end{bmatrix}
$$

This is why the operation is:

> swap components, then flip exactly one sign.

Example:

$$
\begin{bmatrix}
1 \\
2
\end{bmatrix}
\rightarrow
\begin{bmatrix}
-2 \\
1
\end{bmatrix}
$$

or:

$$
\begin{bmatrix}
1 \\
2
\end{bmatrix}
\rightarrow
\begin{bmatrix}
2 \\
-1
\end{bmatrix}
$$

Both are perpendicular directions.

They are opposites of each other.

## The 2D Perpendicular Line

In 2D, one nonzero vector has one perpendicular line.

If $u$ points this way:

```text
      u
     /
    /
---0---------
```

then all perpendicular vectors live on the line crossing it at $90^\circ$:

```text
      | perpendicular line
      |
      |   u
      |  /
------0-/------
      |
      |
```

There are two unit directions on that perpendicular line, but infinitely many magnitudes.

So the perpendicular family is:

$$
\{s[-y,x] \mid s \in \mathbb{R}\}
$$

for:

$$
u = [x,y]
$$

Plain:

> in 2D, perpendicularity leaves one degree of freedom: how far along the perpendicular line.

## 3D Changes The Picture

In 3D, a single vector does not have one perpendicular line.

It has a whole perpendicular plane.

Example:

$$
u =
\begin{bmatrix}
1 \\
0 \\
1
\end{bmatrix}
$$

A vector:

$$
v =
\begin{bmatrix}
x \\
y \\
z
\end{bmatrix}
$$

is perpendicular to $u$ when its $x$ and $z$ contributions cancel.

The $y$ direction is free because $u$ has no $y$ component.

So all vectors like this are perpendicular to $u$:

$$
\begin{bmatrix}
x \\
y \\
-x
\end{bmatrix}
$$

Examples:

$$
\begin{bmatrix}
1 \\
0 \\
-1
\end{bmatrix}
$$

$$
\begin{bmatrix}
1 \\
100 \\
-1
\end{bmatrix}
$$

$$
\begin{bmatrix}
-3 \\
7 \\
3
\end{bmatrix}
$$

All of them live in the perpendicular plane.

This is why sign tables stop being enough.

In 3D, perpendicularity is no longer just two options.

It becomes a whole space of options.

## Orthogonal Complement Preview

The full set of vectors perpendicular to a vector $u$ is called its orthogonal complement.

Written:

$$
u^\perp
$$

Read:

> all directions with no net agreement with $u$.

In 1D:

$$
u^\perp
$$

has dimension $0$.

In 2D:

$$
u^\perp
$$

is a line.

In 3D:

$$
u^\perp
$$

is a plane.

In $n$ dimensions, the perpendicular space to one nonzero vector has dimension:

$$
n - 1
$$

## What We Learned Before Dot Product

Before formulas, the symmetry picture is:

- same direction: scale by a positive number.
- opposite direction: scale by a negative number, especially $-1$ for exact reversal.
- reflection: flip signs or swap coordinates depending on the mirror.
- perpendicular in 2D: quarter-turn, swap components and flip one sign.
- perpendicular in 3D: a whole plane of possible directions.

So dot product will not be magic.

It will become the accounting system for this question:

> how much directional agreement remains after all coordinates contribute?
