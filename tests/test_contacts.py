from python_fundamentals.contacts import (
    name_validation
)

def test_name_validation():
    assert name_validation('') == False, 'Blank should return False'
    assert name_validation('blah') == True, 'Non-blank string should be True'