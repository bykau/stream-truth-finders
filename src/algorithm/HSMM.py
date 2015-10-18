'''
The implementation of Hidden semi-Markovian Model for streaming data truth detection presented in 
Pal, A., Rastogi, V., Machanavajjhala, A., & Bohannon, P. (2012). Information integration over time in unreliable and uncertain environments. In WWW (p. 789). New York, New York, USA: ACM Press. http://doi.org/10.1145/2187836.2187943

@author: Siarhei Bykau (sbykau@purdue.edu)
'''
import numpy as np

def computeO(Z, S, gamma, lambda1, p):
    ''' Compute the mapping vector.
    '''
    O = [0]*len(S)
    O[0] = 0
    for i in range(len(S)-1):
        pass
    return O

if __name__ == '__main__':
    Z = [(0, 'A'), (10, 'B'), (30, 'C')]
    S1 = [(1, 'A'), (12, 'D'), (13,'E'), (35, 'C')]
    O1 = computeO(Z, S1, 0.5, 0.5, 0.5)