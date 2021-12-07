# cython: language_level=3, boundscheck=False, cdivision=True
# distutils: language=c++
#import cython
import os

import numpy as np
cimport numpy as np

from libcpp cimport bool
from libc.stdlib cimport malloc, free

from cython.parallel import prange
cimport openmp
cimport libc.stdio
from cython.parallel cimport parallel, threadid

CTYPE = np.complex128
DTYPE = np.float64
FTYPE = np.float32
ITYPE = np.int32

ctypedef np.int_t ITYPE_t
ctypedef np.float64_t DTYPE_t
ctypedef np.float32_t FTYPE_t
ctypedef np.complex128_t CTYPE_t

cdef extern from "lj.h" nogil:
   void ljAB(double *xyzA, double *xyzB, double eps, double sig12,
             double sig6, int nA, int nB, double *box, double E)

   void ljAA(double *xyzA, double eps, double sig12, double sig6,
             int nA, double *box, double E)

def fitness_function(xyz1, xyz2, box=np.array([1e10,1e10,1e10]), eps11=0.03114525, eps12=0.07178825, sig11=2.586674, sig12=2.106555, nthr=1):

   cdef int num_threads = nthr

   cdef int nA = xyz1.shape[0]
   cdef int nB = xyz2.shape[0]

   cdef double Etot = 0.0
   cdef double EAA, EAB

   cdef double eps4AA  = 4.0*eps11
   cdef double eps4AB  = 4.0*eps12

   cdef double sigAA   = sig11
   cdef double sigAA2  = sigAA*sigAA
   cdef double sigAA4  = sigAA2*sigAA2
   cdef double sigAA6  = sigAA4*sigAA2
   cdef double sigAA12 = sigAA6*sigAA6

   cdef double sigAB   = sig12
   cdef double sigAB2  = sigAB*sigAB
   cdef double sigAB4  = sigAB2*sigAB2
   cdef double sigAB6  = sigAB4*sigAB2
   cdef double sigAB12 = sigAB6*sigAB6

   cdef np.ndarray[DTYPE_t, ndim=2] xyzA  = np.zeros([nA,3], dtype=DTYPE)
   cdef np.ndarray[DTYPE_t, ndim=2] xyzB  = np.zeros([nB,3], dtype=DTYPE)
   cdef np.ndarray[DTYPE_t, ndim=1] boxx  = np.zeros([3], dtype=DTYPE)

   xyzA[:,:] = xyz1.astype(DTYPE)
   xyzB[:,:] = xyz2.astype(DTYPE)
   boxx[:]   = box.astype(DTYPE)

   with nogil:
      with parallel(num_threads=num_threads):
         ljAA(&xyzA[0,0], eps4AA, sigAA12, sigAA6, nA, &boxx[0], EAA)
         ljAB(&xyzA[0,0], &xyzB[0,0], eps4AB, sigAB12, sigAB6, nA, nB, &boxx[0], EAB)

   Etot = EAA + EAB

   return Etot


