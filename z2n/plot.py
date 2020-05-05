#! /usr/bin/python
# -*- coding: utf-8 -*-

# Generic/Built-in
import click
import matplotlib.pyplot as plt
from click_shell import shell

# Other Libraries
import z2n.globals as glob
import z2n.main as main


@shell(prompt=click.style('(plt) >>> ', fg='magenta', bold=True), intro=glob.__plot__)
def plot() -> None:
    """Open the interactive periodogram plotting window."""


@plot.command()
def style() -> None:
    """Change the plotting style (type style)."""

    try:

        click.secho("This will reset the figure.", fg='yellow')

        st = click.prompt("Which style")

        plt.style.use(st)

        main.plot()

        click.secho(f"Style changed to {st}.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def peak() -> None:
    """Add vertical line to the peak value (type peak)."""

    try:

        if glob.axis == 0:

            glob.axes.axvline(glob.peak, color='tab:red',
                              label="Correct Frequency")

        else:

            glob.axes[0].axvline(glob.peak, color='tab:red',
                                 label="Correct Frequency")

        click.secho("Peak line added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def band() -> None:
    """Add horizontal line to the bandwidth value (type band)."""

    try:

        if glob.axis == 0:

            glob.axes.axhline(glob.band, color='tab:gray', label="Bandwidth")

        else:

            glob.axes[0].axhline(
                glob.band, color='tab:gray', label="Bandwidth")

        click.secho("Bandwidth line added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def legend() -> None:
    """Add legend to the figure (type legend)."""

    try:

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):

                glob.axes[opt - 1].legend(loc='best')
                click.secho("Legend added.", fg='green')

            else:

                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.legend(loc='best')
            click.secho("Legend added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def title() -> None:
    """Change the title on the figure (type title)."""

    try:

        t = click.prompt("Which title")

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_title(t)
                click.secho(f"Title '{t}' added.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_title(t)
            click.secho(f"Title '{t}' added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def xlabel() -> None:
    """Change the label on the x axis (type xlabel)."""

    try:

        lab = click.prompt("Which label")

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_xlabel(lab)
                click.secho(f"X axis label '{lab}' added.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_xlabel(lab)
            click.secho(f"X axis label '{lab}' added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def xscale() -> None:
    """Change the scale on the x axis (type xscale)."""

    try:

        scale = click.prompt("Which scale [linear, log, symlog, logit]")

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_xscale(scale)
                click.secho(f"X axis scale changed to {scale}.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_xscale(scale)
            click.secho(f"X axis scale changed to {scale}.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def xlim() -> None:
    """Change the limites on the x axis (type xlim)."""

    try:

        low = click.prompt("Which lower limit", type=float)

        up = click.prompt("Which upper limit", type=float)

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_xlim([low, up])
                click.secho(f"X axis limits changed to {low, up}.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_xlim([low, up])
            click.secho(f"X axis limits changed to {low, up}.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def ylabel() -> None:
    """Change the label on the y axis (type ylabel)."""

    try:

        lab = click.prompt("Which label")

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_ylabel(lab)
                click.secho(f"Y axis label '{lab}' added.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_ylabel(lab)
            click.secho(f"Y axis label '{lab}' added.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def yscale() -> None:
    """Change the scale on the y axis (type yscale)."""

    try:

        scale = click.prompt("Which scale [linear, log, symlog, logit]")

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_yscale(scale)
                click.secho(f"Y axis scale changed to {scale}.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_yscale(scale)
            click.secho(f"Y axis scale changed to {scale}.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def ylim() -> None:
    """Change the limites on the y axis (type ylim)."""

    try:

        low = click.prompt("Which lower limit", type=float)

        up = click.prompt("Which upper limit", type=float)

        if glob.axis != 0:

            opt = click.prompt(
                "Change the periodogram [1] or the background [2]", type=int)

            if opt in (1, 2):
                glob.axes[opt - 1].set_ylim([low, up])
                click.secho(f"Y axis limits changed to {low, up}.", fg='green')

            else:
                click.secho("Select '1' or '2'.", fg='red')

        else:
            glob.axes.set_ylim([low, up])
            click.secho(f"Y axis limits changed to {low, up}.", fg='green')

    except Exception as error:
        click.secho(f'{error}', fg='red')


@plot.command()
def save() -> None:
    """Save the plot into a file (type save)."""

    plt.tight_layout()

    txt = click.prompt("Name of the output file")

    out = click.prompt("Which format [png, pdf, ps, eps]")

    if out == 'png':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'pdf':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'ps':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    elif out == 'eps':
        plt.savefig(f'{txt}.{out}', format=out)
        click.secho(f"Image file saved at {txt}.{out}", fg='green')

    else:
        click.secho(f"{out} format not supported.", fg='red')
