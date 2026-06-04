Calculate the monthly mortgage payment and the total interest paid.

## Run the desktop UI

```bash
python3 mortgage_ui.py
```

The UI includes:

- Mortgage payment, total interest, and total paid
- Home sale net proceeds, tax-free gain, taxable gain, estimated tax, and profit after tax

The home sale tax estimate uses a simplified capital-gains calculation with a
`$500,000` qualifying gain exclusion:

```text
total gain = sale price - initial cost - selling costs
taxable gain = max(0, total gain - 500000)
estimated tax = taxable gain * tax rate
```

## Run the command-line version

```bash
python3 mortgage.py
```

    Parameters:
    principal (float): The initial loan amount
    annual_rate (float): The annual interest rate (in percentage)
    years (int): The term of the loan in years

    Returns:
    tuple: A tuple containing the monthly payment and the total interest paid
