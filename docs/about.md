# About The Project

The Z2n Software was developed by Yohan Alexander as a research project, funded by the CNPq Institution, and it is a Open Source initiative. The program allows the user to calculate periodograms using the Z2n statistics a la Buccheri et al. 1983, which is defined as follows.

![\Large \phi_j \[0,1\] = frac(v_i\Delta t_{ij} + \dot v_i \frac{\Delta t^2_{ij}}{2} + \dot v_i \frac{\Delta t^3_{ij}}{6})](https://render.githubusercontent.com/render/math?math=%5CLarge%20%5Cphi_j%20%5B0%2C1%5D%20%3D%20frac(v_i%5CDelta%20t_%7Bij%7D%20%2B%20%5Cdot%20v_i%20%5Cfrac%7B%5CDelta%20t%5E2_%7Bij%7D%7D%7B2%7D%20%2B%20%5Cdot%20v_i%20%5Cfrac%7B%5CDelta%20t%5E3_%7Bij%7D%7D%7B6%7D))

![\Large Z^2_n = \frac{2}{N} \cdot \sum_{k=1}^{n} \[(\sum_{j=1}^{N} cos(k\phi_j)) ^ 2 + (\sum_{j=1}^{N} sin(k\phi_j)) ^ 2\]](https://render.githubusercontent.com/render/math?math=%5CLarge%20Z%5E2_n%20%3D%20%5Cfrac%7B2%7D%7BN%7D%20%5Ccdot%20%5Csum_%7Bk%3D1%7D%5E%7Bn%7D%20%5B(%5Csum_%7Bj%3D1%7D%5E%7BN%7D%20cos(k%5Cphi_j))%20%5E%202%20%2B%20(%5Csum_%7Bj%3D1%7D%5E%7BN%7D%20sin(k%5Cphi_j))%20%5E%202%5D)

The standard Z2n statistics calculates the phase of each photon and the sinusoidal functions above for each photon. Be advised that this is very computationally expensive if the number of photons is high, since the algorithm grows at a exponential rate ![\large O(n^2)](https://render.githubusercontent.com/render/math?math=%5Clarge%20O(n%5E2)).

## Built With

The Z2n Software was built using the `Python` open source language.

* [Python](https://python.org)
