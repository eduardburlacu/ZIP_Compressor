from itertools import groupby
from camzip import camzip
from camunzip import camunzip
from filecmp import cmp
from os import stat
from json import load
from math import log2
import sys
import os

#-------Insert main project directory so that we can resolve the src imports-------
src_path = os.path.dirname(__file__)
sys.path.insert(0, src_path)

canterbury = os.listdir(os.path.abspath(os.path.join(src_path,'canterbury')))
methods = ["shannon_fano","huffman","arithmetic"]
print(canterbury)
H = lambda pr: -sum([pr[a]*log2(pr[a]) for a in pr])

for file in canterbury:
    filename = os.path.abspath(os.path.join(src_path, 'canterbury',file))
    for method in methods:
        print(f"____________CAMZIP {file} WITH {method}_____________")
        camzip(method,filename)
        camunzip(filename+ ".cz" + method[0])
        Nin = stat(filename).st_size
        print(f'Length of original file: {Nin} bytes')
        Nout = stat(filename + '.cz' + method[0]).st_size
        print(f'Length of compressed file: {Nout} bytes')
        print(f'Compression rate: {8.0 * Nout / Nin} bits/byte')
        with open(filename + '.czp', 'r') as fp:
            freq = load(fp)
        pf = dict([(a, freq[a] / Nin) for a in freq])
        print(f'Entropy: {H(pf)} bits per symbol')
        if cmp(filename, filename + '.cuz'):
            print('The two files are the same')
        else:
            print('The files are different')

