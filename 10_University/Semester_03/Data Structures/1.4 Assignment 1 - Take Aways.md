In Question 3, we were given n number of coordinates and we had to find the number of roads needed to join each coordinate to every other. The question also demanded the calculation of the number of intersection and assuming each would have 4 signals we had to return the number of signals for n coordinates as well.
The naïve approach was to use the combinations formula:

**n C r: Total n objects taking r at a time**

---
### Roads
For the roads we needed 2 points at a time. So putting in r = 2 simplified the formula to:

$\binom{n}{2} = \frac{n!}{2!(n-2)!} = \frac{n(n-1)}{2}$

### Signals
For the signals, we need 4 points at a time because that's the only time we gat at least 1 intersection. So the formula for that is going to be:

$\binom{n}{4} = \frac{n!}{4!(n-4)!} = \frac{n(n-1)(n-2)(n-3)}{24}$

Since each intersection has 4 signals:

$4\binom{n}{4} = 4 \cdot \frac{n(n-1)(n-2)(n-3)}{24} = \frac{n(n-1)(n-2)(n-3)}{6}$

---
But this approach is naïve for a reason and that reason is this breaks when a set of 3 or more collinear points is present.
So the next best thing is to calculate how many collinear triples are there and subtract that from the formulas above. 

For collinearity of 3 points we an use:

$\text{Area} = \frac{1}{2}\left|\det\begin{pmatrix}x_1 & y_1 & 1 \\x_2 & y_2 & 1 \\x_3 & y_3 & 1\end{pmatrix}\right| = 0$

But building this matrix would require 3 points at a time and building every possible 3 point combination is O(n<sup>3</sup>). Which is eww.

---
### Slopes
What if we take a point $i$ and we calculate the slope from $i$ to every point in the array. The slope calculation itself is O(1) and when we do it with every point it's O(n). We store the slopes in an array and now we check how many times the same slope is repeated and that will tell us the number of points lying on a line P<sub>i</sub> from the initial point. But that requires O(n<sup>2</sup>). So, we sort the array using Quick sort (O(n log n)) so that equal slopes are continuous in the array and we can simply count the points on equal slopes.

Suppose there are k points lying on the line P<sub>i</sub> meaning number of collinear points is k + 1. But what we need is the number of sets of 3 of collinear points. For that we already have the point $i$. So, we take combinations of k, 2 at a time:

$\binom{k}{2} = \frac{k!}{2!(k-2)!} = \frac{k(k-1)}{2}$

This whole operation will be O(n).

---
### Complexity
Since the slope calculation was O(n) and the sorting was O(n log n) and the last counting part is O(n). So, the total for point $i$ is going to be:

O(n) + O(n log n) + O(n) = O(2n + log n) = O(n log n)

Now, we were doing this for 1 point $i$. Repeat for n points and we get the complexity:

**O(n<sup>2</sup> log n)**.

---
