from python_fundamentals.contacts import (
    search_contacts,
    selection_validation,
    name_validation,
    number_validation
)

def test_search_contacts():
    pass

def test_selection_validation():
    assert selection_validation("view") == True, '"view" should return True'
    assert selection_validation("copy") == False, '"copy" should return False'
    assert selection_validation("") == False, 'Blank string should return False'
    assert selection_validation(5) == False, 'Int should return False'

def test_name_validation():
    assert name_validation('') == False, 'Blank should return False'
    assert name_validation('blah') == True, 'Non-blank string should be True'

def test_number_validation():
    assert number_validation('3249023445') == True, 'a string of only numbers should be True'
    assert number_validation('(324)902-3234') == True, 'a string of only numbers, parethesis, hyphens should be True'
    assert number_validation('(324)90/2-3234') == False, 'a string with "/" should be False'
    assert number_validation('Mah digits') == False, 'a string with letters should be False'
    assert number_validation('') == False, 'a blank string should be False'