import pytest 

def test_xyz():
    from devtools import api
    app = api.app()
    assert app is not None