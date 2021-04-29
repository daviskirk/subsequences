import cython  # type: ignore


@cython.infer_types(True)
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def is_subsequence(subseq, seq):
    """Check if `subseq` is a subsequence of `seq`."""
    n = len(seq)
    m = len(subseq)

    if m > n:
        return False

    i = 0  # index of seq
    j = 0  # index of subseq

    while i < n and j < m:
        if seq[i] == subseq[j]:
            j += 1
        i += 1

    return j == m


@cython.infer_types(True)
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def is_subsequence_2d(subseq, seq):
    """Check if `subseq` is a subsequence of `seq`."""
    n = seq.shape[0]
    m = subseq.shape[0]
    w = seq.shape[1]

    if seq.shape[1] != subseq.shape[1]:
        return False

    if m > n:
        return False

    i = 0  # index of seq
    j = 0  # index of subseq
    k = 0  # index of second dimension

    while i < n and j < m:
        is_row_valid = True
        for k in range(w):
            if seq[i, k] != subseq[j, k]:
                is_row_valid = False
                break
        if is_row_valid:
            j += 1
        i += 1

    return j == m
