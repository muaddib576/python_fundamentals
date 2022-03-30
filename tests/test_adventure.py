import pytest
from python_fundamentals.adventure import (Go, error)



def test_error(capsys):
    error("test1")
    output = capsys.readouterr().out
    
    assert output == "Error: test1\n"

def test_go(capsys):
    Go(['east']).do()
    output = capsys.readouterr().out
    # print(output)
    assert "The square part of town." in output

# test_go()