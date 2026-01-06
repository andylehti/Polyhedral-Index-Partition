from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Iterable, List, Sequence, Tuple

def polyHedralIndex(x: int, y: int) -> int:
    if y < 1:
        raise ValueError("dimension d must be >= 1")
    if x < 0:
        raise ValueError("magnitude m must be >= 0")
    return comb(x + y - 1, y)

def getInverse(n: Sequence[int], y: bool = False) -> int:
    if not n:
        raise ValueError("coords must be non-empty")
    a = list(n)
    if y:
        a = [zigzagEncode(z) for z in a]
    if any((not isinstance(v, int)) for v in a):
        raise TypeError("all coordinates must be integers")
    if any(v < 0 for v in a):
        raise ValueError("coordinates must be >= 0 (or use signed=True)")
    t = len(a)
    c = [0] * t
    s = 0
    for i in range(t - 1, -1, -1):
        s += a[i]
        c[i] = s
    k = 0
    for i in range(t):
        k += polyHedralIndex(c[i], t - i)
    return k

def partition(k: int, y: int, *, signed: bool = False) -> Tuple[int, ...]:
    if not isinstance(k, int) or k < 0:
        raise ValueError("index must be an integer >= 0")
    if not isinstance(y, int) or y < 1:
        raise ValueError("dim must be an integer >= 1")
    r = k
    p: List[int] = []
    for t in range(y, 0, -1):
        x = approximate(r, t)
        p.append(x)
        r -= polyHedralIndex(x, t)
    a: List[int] = []
    for i in range(y - 1):
        a.append(p[i] - p[i + 1])
    a.append(p[-1])
    if signed:
        a = [zigzagDecode(n) for n in a]
    return tuple(a)

def approximate(n: int, t: int) -> int:
    if n < 0:
        raise ValueError("remainder r must be >= 0")
    if n == 0:
        return 0
    l, h = 0, 1
    while polyHedralIndex(h, t) <= n:
        h *= 2
    l = h // 2
    while l + 1 < h:
        m = (l + h) // 2
        if polyHedralIndex(m, t) <= n:
            l = m
        else:
            h = m
    return l

def zigzagEncode(z: int) -> int:
    if not isinstance(z, int):
        raise TypeError("z must be int")
    return 2 * z if z >= 0 else -2 * z - 1

def zigzagDecode(n: int) -> int:
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be int >= 0")
    return n // 2 if (n % 2 == 0) else -(n // 2) - 1


### ---------------------------------- old

import sys
from functools import lru_cache
from math import log10, ceil
import math
from mpmath import mp
import mpmath as mpm
sys.set_int_max_str_digits(0)
sys.setrecursionlimit(100000)

@lru_cache(maxsize=None)
def old_polyHedralIndex(x, y):
    if x < 1: return 0
    return int(mp.binomial(x + y - 1, y))

def old_approximate(n, t, x=1):
    e = old_polyHedralIndex(x, t)
    while n > e:
        x *= 10
        e = old_polyHedralIndex(x, t)
    if x == 10:
        while e > n:
            x -= 1
            e = old_polyHedralIndex(x, t)
        return x
    l, h = x // 10, x
    while l <= h:
        m = (l + h) // 2
        e = old_polyHedralIndex(m, t)
        if e == n: return m
        elif e < n: l = m + 1
        else: h = m - 1
    return l - 1 if old_polyHedralIndex(l - 1, t) < n else l

def old_getPair(k):
    k = mpm.mpf(k)
    s = mpm.floor(((-1 + (1 + 8 * k) ** 0.5) / 2))
    i = old_polyHedralIndex(s, 2)
    return int(s - (k - i)), int(k - i)

def old_getPartition(n, y):
    if y < 2: return [n]
    if y == 2: return old_getPair(n)
    a = old_approximate(n, y)
    p = old_polyHedralIndex(a, y)
    r = int(n - p)
    c = old_getPartition(r, y - 1)
    a = int(a - sum(c))
    return (a,) + c

def old_partition(n, y=2):
    mpm.mp.dps = 100
    mpm.mp.dps = 100 + len(str(n)) * 2
    return list(old_getPartition(n, y))

def old_pairInverse(a, b):
    a, b = mpm.mpf(a), mpm.mpf(b)
    n = a + b
    return int(mpm.nint(n * (n + 1) / 2 + b))

def old_getInverse(*a):
    a = list(a)
    s = len(''.join(map(str, a)))
    mpm.mp.dps = s * 2
    if len(a) <= 1: return a[-1]
    return old_inversePartition(*a)

def old_inversePartition(*c):
    if len(c) == 2: return old_pairInverse(*c)
    n = sum(c)
    r = old_inversePartition(*c[1:])
    return int(old_polyHedralIndex(n, len(c)) + r)

import random
import time

def timerTest(e = 0, n = 20):
    tests = [
        (
            random.randint(10 ** (d - 1), 10 ** d - 1),
            random.randint(2, 2 ** 12)
        )
        for d in (random.randint(1, 100) for _ in range(n))
    ]

    newTotal = 0.0
    oldTotal = 0.0

    for i, (a, b) in enumerate(tests, 1):
        t0 = time.perf_counter()
        rNew = partition(a, b)
        t1 = time.perf_counter()
        dtNew = t1 - t0
        newTotal += dtNew

        if e == 1:
            t2 = time.perf_counter()
            rOld = old_partition(a, b)
            t3 = time.perf_counter()
            dtOld = t3 - t2
            oldTotal += dtOld
            same = tuple(rNew) == tuple(rOld)
            print(f"{i:02d} a={a} b={b} new={dtNew:.6f}s old={dtOld:.6f}s same={same}")
        else:
            print(f"{i:02d} a={a} b={b} new={dtNew:.6f}s")

    print(f"\npartition total: {newTotal:.6f}s")
    if e == 1:
        print(f"old_partition total: {oldTotal:.6f}s")

timerTest(1)
