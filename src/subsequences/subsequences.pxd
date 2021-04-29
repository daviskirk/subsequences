import cython

ctypedef fused anyarray:
    short[:]
    int[:]
    long[:]
    object[:]
    object


cpdef bint is_subsequence(anyarray subseq, anyarray seq)

ctypedef fused anytype:
    short
    int
    long
    object

cpdef bint is_subsequence_2d(anytype[:, ::1] subseq, anytype[:, ::1] seq)
