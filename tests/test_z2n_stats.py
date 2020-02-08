import numpy as np
from stats import z2n

time = np.array([1.90508838e+08, 1.90508838e+08, 1.90508839e+08, 1.90508840e+08,
       1.90508840e+08, 1.90508841e+08, 1.90508842e+08, 1.90508842e+08,
       1.90508843e+08, 1.90508844e+08])

freq = np.array([0.0007])

def test_period():
    p = z2n.period(time)
    test = 6.0
    assert(np.isclose(p, test))


def test_frequency():
    f = z2n.frequency(time)
    test = 0.16666666666666666
    assert(np.isclose(f, test))

def test_phases():
    v = z2n.phases(time, freq)
    test = np.array([[0.],
                    [0.],
                    [0.0007],
                    [0.0014],
                    [0.0014],
                    [0.0021],
                    [0.0028],
                    [0.0028],
                    [0.0035],
                    [00.0042]])
    assert(np.isclose(v, test).all())

def test_periodogram():
    z = z2n.periodogram(time, freq)
    test = np.array([[19.998526]])
    assert(np.isclose(z, test).all())

def test_lightcurve():
    l = z2n.lightcurve(time, freq)
    test = np.array([[0.00189]])
    assert(np.isclose(l, test).all())

def test_peak():
    k = z2n.peak(freq, [19.998526])
    test = 0.0007
    assert(np.isclose(k, test).all())

def test_forest():
    r = z2n.forest(freq, [19.998526])
    test = 19.998526
    assert(np.isclose(r, test).all())

def test_bandwidth():
    b = z2n.bandwidth(freq, [19.998526])
    test = 0.0
    assert(np.isclose(b, test).all())

def test_pfraction():
    o = z2n.pfraction(time, [19.998526])
    test = 0.0
    assert(np.isclose(o, test).all())