from python_fundamentals.contacts import (
    selection_validation,
    name_validation,
    number_validation,
    email_validation
)

def test_selection_validation():
    assert selection_validation("view") == True, '"view" should return True'
    assert selection_validation("copy") == False, '"copy" should return False'
    assert selection_validation("") == False, 'Blank string should return False'
    assert selection_validation(5) == False, 'Int should return False'

def test_name_validation():
    assert name_validation('') == False, 'Blank should return False'
    assert name_validation('blah') == True, 'Non-blank string should be True'
    assert name_validation('bl,ah') == False, 'string w/ a comma should be False'

def test_number_validation():
    assert number_validation('3249023445') == True, 'a string of only numbers should be True'
    assert number_validation('(324)902-3234') == True, 'a string of only numbers, parethesis, hyphens should be True'
    assert number_validation('(324)90/2-3234') == False, 'a string with "/" should be False'
    assert number_validation('Mah digits') == False, 'a string with letters should be False'
    assert number_validation('') == False, 'a blank string should be False'

def test_email_validation():
    assert email_validation('blah@gmail.com') == True, 'a str w/ ??? then "@" then ??? then "." then ??? should be True'
    assert email_validation('bl.ah@gmail.com') == True, 'a str w/ a "." before the first "@" should be True'
    assert email_validation('blahgmail.com') == False, 'a str without "@" should be False'
    assert email_validation('blah@gmailcom') == False, 'a str without "." should be False'
    assert email_validation('blah@gm@ail.com') == False, 'a str more than one "@" should be False'
    assert email_validation('blah@gm.ail.com') == False, 'a str more than one "." after the "@" should be False'
    assert email_validation('@.') == False, 'a str with no characters outside "@" and "." should be False'
    assert email_validation('') == False, 'a blank str should be False'
    assert email_validation(5) == False, 'an int should be False'