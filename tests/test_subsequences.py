import numpy as np
import pytest

from subsequences import is_subsequence, is_subsequence_2d, is_substring


def test_is_substring():
    seq = ["a", "b", "c", "d"]

    r = is_substring(["b", "c"], seq)
    assert r is True

    r = is_substring(["b", "d"], seq)
    assert r is False

    r = is_substring(["b", "a"], seq)
    assert r is False


def test_is_subsubsequence():
    seq = ["a", "b", "c", "d"]

    r = is_subsequence(["b", "c"], seq)
    assert r is True

    r = is_subsequence(["b", "d"], seq)
    assert r is True

    r = is_subsequence(["b", "a"], seq)
    assert r is False

    r = is_subsequence(["a", "b", "c", "d", "e"], seq)
    assert r is False


def test_is_subsubsequence_2d():
    seq = np.array(
        [
            ["a", "b", "c"],
            ["t", "t", "t"],
            ["b", "b", "c"],
            ["a", "b", "c"],
            ["b", "b", "a"],
        ],
        dtype=object,
    )

    subseq = np.array(
        [
            ["t", "t", "t"],
            ["b", "b", "a"],
        ],
        dtype=object,
    )

    r = is_subsequence_2d(subseq, seq)
    assert r is True

    subseq = np.array(
        [
            ["t", "t", "t"],
            ["b", "b", "d"],
        ],
        dtype=object,
    )

    r = is_subsequence_2d(subseq, seq)
    assert r is False

    # objects break
    with pytest.raises(TypeError):
        is_subsequence_2d(["a", "b"], ["a", "b", "c"])

    # 1d breaks
    with pytest.raises(TypeError):
        is_subsequence_2d(np.array([1, 2, 3]), np.array([1, 2, 3, 4]))

    # 2d works
    r = is_subsequence_2d(np.array([[1], [2], [3]]), np.array([[1], [2], [3], [4]]))
    assert r is True

    # 3d breaks
    with pytest.raises(TypeError):
        is_subsequence_2d(
            np.array([[[1]], [[2]], [[3]]]), np.array([[[1]], [[2]], [[3]], [[4]]])
        )

    # When column dimension doesn't match always return False
    r = is_subsequence_2d(
        np.array([[1], [2], [3]]), np.array([[1, 1], [2, 2], [3, 3], [4, 4]])
    )
    assert r is False

    # larger sub that seq always returns False
    r = is_subsequence_2d(np.array([[1], [2], [3], [4]]), np.array([[1], [2], [3]]))
