def test_bar_fixture(testdir):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.tolerance()
        def test_sth(tolerance):
            assert 1e-7 < tolerance
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
