def mortgage_interest_calculator(principal, annual_rate, years):
    """
    Calculate the monthly mortgage payment and the total interest paid.

    Parameters:
    principal (float): The initial loan amount
    annual_rate (float): The annual interest rate (in percentage)
    years (int): The term of the loan in years

    Returns:
    tuple: A tuple containing the monthly payment and the total interest paid
    """
    monthly_rate = annual_rate / 100 / 12
    total_payments = years * 12

    # Monthly payment calculation using the formula for an annuity
    monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -total_payments)

    # Total interest paid calculation
    total_interest = (monthly_payment * total_payments) - principal

    return monthly_payment, total_interest

print ("")
print ("-"*80)

principal_amount = float(input("Loan Amount: "))
annual_interest_rate = float(input("Annual interest rate: "))
loan_term_years = int(input("Loan term in Years: "))

monthly_payment, total_interest = mortgage_interest_calculator(principal_amount, annual_interest_rate, loan_term_years)

print ("-"*80)

print(f"Monthly Payment: {monthly_payment:.2f}")
print(f"Total Interest Paid: {total_interest:.2f}")
