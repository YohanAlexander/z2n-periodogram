#! /usr/bin/python
# -*- coding: utf-8 -*-

from tqdm import trange, tqdm
from multiprocessing import Pool, freeze_support, RLock

#Parallel
    #freeze_support()
    #with Pool(initializer=tqdm.set_lock, initargs=(RLock(),)) as pool:
    #    result = tuple(tqdm(pool.imap(func, object), total=len(object)))