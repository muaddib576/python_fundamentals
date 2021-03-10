"""Returns a recomended tip based on a given bill and service satisfaction level

1. ask the user to input the bill total $
2. ask the user their level of satisfaction with service
    a. low = 15%
    b. avg = 20%
    c. high = 25%
3. give the user both the recomended tip and new total (original + tip)
"""

#static tipping levels based on satisfaction
tipping_buckets = {"low" : .15,
                   "avg" : .2,
                   "high" : .25}



def tip_calc(bill, sat_level):
    """takes the given total bill and satisfaction level and returns a recomended tip $"""
    #determines the correct % bucket based on satisfaction level
    tip_percent = tipping_buckets[sat_level]
    #multiplies bill total by the correct %
    tip = bill * tip_percent
    #retruns the calculated tip
    return tip

def bill_validation(bill_check):
    """Checks to make sure provided bill is a positive number"""

    #converts to float and returns false if error
    try:
        float(bill_check)
    except ValueError:
        return "You shouldnt need letters to give me a number. Try again."   

    #ensures number is positive
    if float(bill_check) <= 0:
        return "A bill is usually a POSITIVE number. Try again."
    return True

def satisfaction_validation(sat_level):
    """Checks to ensure the given satisfaction is one of the three"""

def main():
    """asks user for bill total and satisfaction level, then prints tip and new total"""
    #asks user for their bill's total ()
    provided_bill = ""    
    while bill_validation(provided_bill) != True: 
        provided_bill = input("What is your bill total? ")

        if bill_validation(provided_bill) != True:
            print(bill_validation(provided_bill))

    #asks user how satisfied they are
    provided_sat = ""
    #calls tip_calc
    #prints recomended tip
    #prints new bill with tip included

def test_tip_calc():
    assert tip_calc(10, "low") == 1.5, "10 and low = 1.5"
    assert tip_calc(10, "avg") == 2, "10 and avg = 2"
    assert tip_calc(10, "high") == 2.5, "10 and high = 2.5"


# test_tip_calc()
main()
