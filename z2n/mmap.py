#! /usr/bin/python
# -*- coding: utf-8 -*-

# Other Libraries
import numpy as np
import dask.array as da
from tqdm import trange


def map_array(array: da.array, name: str) -> np.array:
    """
    Maps a dask array from RAM to disk.

    Parameters
    ----------
    array : da.array
        An array partitioned in n chunks.
    name : str
        A string the represents the output file.

    Returns
    -------
    disk : np.array
        An array mapped to disk memory.
    """
    disk = np.lib.format.open_memmap(
        f'/tmp/{name}.npy', mode='w+', dtype=array.dtype, shape=array.shape)
    for chunk in trange(len(array.chunks[0])):
        lower = chunk * array.blocks[0].size
        upper = (chunk + 1) * array.blocks[0].size
        disk[lower:upper] = array.blocks[chunk].compute()
    return disk
