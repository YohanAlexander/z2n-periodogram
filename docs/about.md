# About The Project

The $`Z^2_n`$ Software was developed by Yohan Alexander as a research project, funded by the CNPq Institution, and it is a Open Source initiative. The program allows the user to calculate periodograms using the $`Z^2_n`$ statistics a la Buccheri et al. 1983.

The $`Z^2_n`$ is a periodogram based on the Rayleigh method, which applies the time samples in a signal to a Fourier analysis. This method has been shown to be useful in detecting periodic signals at high frequencies associated with the rotation of compact objects.

First, each event is reduced to a phase value $`\phi_j`$, in the range of 0 to 1, where $`frac (x) = x - \lfloor x \rfloor`$ such that for the $`j`$-th event we have the following equation, where $`\Delta t_{ij}`$ is the time of the event under analysis $`t_j`$ minus the time of the first detected event $`T_0`$.

```math
\phi_j [0,1] = frac(v_i\Delta t_{ij} + \dot v_i \frac{\Delta t^2_{ij}}{2} + \dot v_i \frac{\Delta t^3_{ij}}{6})
```

The $`Z^2_n`$ power spectrum, where $`n`$ is the number of harmonics included in the power, and $`N`$ is the number of events, is calculated from the equation which is defined as follows.

```math
{\color{red}Z^2_n =} {\color{blue}\frac{2}{N}} {\color{black}\cdot} {\color{green}\sum_{k=1}^{n}} [({\color{green}\sum_{j=1}^{N}} {\color{magenta}cos}({\color{red}k}{\color{blue}\phi_j})) ^ 2 + ({\color{green}\sum_{j=1}^{N}} {\color{magenta}sin}({\color{red}k}{\color{blue}\phi_j})) ^ 2]
```

Note that this is potentially very computationally expensive, as there are two variables by which we are doing a loop, $`\color{red}k`$ which represents the frequencies, and $`\color{blue}j`$ which are the indices of the event.

Think of the loop $`\color{blue}j`$ as being within the loop $`\color{red}k`$. For each new $`\color{red}k`$, we get the full range of $`\color{blue}j`$, which is why the periodogram can sometimes be very slow, since the execution time of the algorithm grows at a exponential rate $`O(n^2)`$.

## Built With

The Z2n Software was built using the `Python` open source language.

* [Python](https://python.org)
