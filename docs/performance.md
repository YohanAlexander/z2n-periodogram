# The Core computation on the software

The $`Z^2_n`$ Software was designed to the be both simple to use by the available command line interface, and yet very fast on perfoming the power spectrum computation.

The speed is achieved by the union of 3 methods:

* [Vectorizing operations](https://en.wikipedia.org/wiki/Array_programming)
* [Parallel threads](https://en.wikipedia.org/wiki/Parallel_computing)
* [Compilation to assembly code](https://numba.pydata.org/)

Keep in mind the pseudocode for the algorithm of the $`Z^2_N`$ power computation:

```bash
function PERIODOGRAM(T[N], F[M])
    Input: T[N]: array with photon arrival times
    Input: F[M]: array with frequency spectrum
    for i = 0 to M − 1 do
        - compute Z2n power for each frequency
        for j = 0 to N − 1 do
            - compute phase for each photon arrival time
            ϕj = T[j] * F[i]
            ϕj = ϕj - ⌊ϕj⌋
            sines[j] = SIN(2π * ϕj)
            cosines[j] = COS(2π * ϕj)
        end for
        sin = SUM(sines)
        cos = SUM(cosines)
        Z2n[j] = sin**2 + cos**2
    end for
    Z2n[j] = Z2n * (2/LEN(T))
    return Z2n
end function
```

```math
Z^2_n = \frac{2}{N} \cdot \sum_{k=1}^{n} [(\sum_{j=1}^{N} cos(k\phi_j)) ^ 2 + (\sum_{j=1}^{N} sin(k\phi_j)) ^ 2]
```

Each result on the power spectrum will be obtained by the computation of the following graph. There are two different subtrees on the computation graph, both can be executed in parallel on different threads.

![vector](https://user-images.githubusercontent.com/39287022/86088759-52242400-ba7d-11ea-9e34-f7cd0d45071f.png)

# Vectorization

Besides the parallel threads, the operations on each blue node encapsulate the full range of the photon arrival times, therefore can be vectorized as shown on the following graph.

![array](https://user-images.githubusercontent.com/39287022/86088427-b5fa1d00-ba7c-11ea-9693-6352b81c1f66.png)

# Parallel Loops

The resulting power spectrum will be the blue node on the following graph, that is the product of the parallel computation of many threads (according to the processor CPU) each of a different frequency graph.

![paralelo](https://user-images.githubusercontent.com/39287022/86088434-ba263a80-ba7c-11ea-8c73-6bc8fb7853eb.png)

# Compilation

The process of compiling the `Python` source code into machine code (assembly x86) optimized for each function is achieved by the `Numba` JIT (just-in-time) compiler, with the available decorators for wrapping functions. Taking advantage of this process makes it easy to avoid the GIL (global interpreter lock) of the `Python` language.
