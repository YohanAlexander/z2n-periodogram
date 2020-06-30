# Interactive Plotting Window

The $`Z^2_n`$ Software has a special window for interactive plotting of the periodogram, that makes possible selecting regions on the power spectrum, or changing parameters on the generated figure, just type `plot` on the terminal, for more information on the usage type `help`.

```bash
(z2n) >>> plot

        Interactive plotting window of the Z2n Software.
        Type "help" for more information.

(plt) >>> help

Documented commands (type help <topic>):
========================================
save  title  xlabel  xlim  xscale  ylabel  ylim  yscale

Undocumented commands:
======================
exit  help  quit

(plt) >>>
```

You can verify if you are interacting with the periodogram itself or the plot figure at any point by checking the prefix on the terminal.

```bash
(z2n) >>> 'Interacting with the periodogram'

(plt) >>> 'Interacting with the plot figure'
```

!!! Important

        If you are unable to see the plot of the power spectrum, it means that a required component is missing, and the $`Z^2_n`$ Software will not be able to execute the interactive backend and plot the periodogram. See [known issues](/install/#known-issues) to better understand the problem and the solutions.
