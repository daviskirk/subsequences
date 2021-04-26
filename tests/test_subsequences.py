from subsequences import is_subsequence, is_substring


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
