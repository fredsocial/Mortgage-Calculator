import tkinter as tk
from tkinter import ttk

from mortgage import mortgage_interest_calculator


HOME_SALE_GAIN_EXCLUSION = 500000


class MortgageCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mortgage Calculator")
        self.geometry("680x650")
        self.minsize(560, 600)
        self.configure(bg="#f6f3ee")

        self.loan_amount = tk.StringVar(value="350000")
        self.annual_rate = tk.StringVar(value="6.75")
        self.loan_years = tk.StringVar(value="30")
        self.monthly_payment = tk.StringVar(value="$0.00")
        self.total_interest = tk.StringVar(value="$0.00")
        self.total_paid = tk.StringVar(value="$0.00")
        self.status = tk.StringVar(value="Enter mortgage details to estimate your payment.")

        self.initial_cost = tk.StringVar(value="350000")
        self.sale_price = tk.StringVar(value="525000")
        self.selling_costs = tk.StringVar(value="31500")
        self.tax_rate = tk.StringVar(value="15")
        self.net_proceeds = tk.StringVar(value="$0.00")
        self.excluded_gain = tk.StringVar(value="$0.00")
        self.taxable_gain = tk.StringVar(value="$0.00")
        self.estimated_tax = tk.StringVar(value="$0.00")
        self.profit_after_tax = tk.StringVar(value="$0.00")
        self.sale_status = tk.StringVar(value="Enter sale details to estimate proceeds and tax.")

        self.purchase_yearly_taxes = tk.StringVar(value="9000")
        self.purchase_price = tk.StringVar(value="650000")
        self.purchase_down_payment = tk.StringVar(value="150000")
        self.purchase_rate = tk.StringVar(value="6.75")
        self.purchase_years = tk.StringVar(value="30")
        self.purchase_monthly_payment = tk.StringVar(value="$0.00")
        self.purchase_monthly_taxes = tk.StringVar(value="$0.00")
        self.purchase_total_monthly = tk.StringVar(value="$0.00")
        self.purchase_annual_cost = tk.StringVar(value="$0.00")
        self.purchase_tax_savings = tk.StringVar(value="$0.00")
        self.tax_break_even_years = tk.StringVar(value="0.0 years")
        self.purchase_status = tk.StringVar(value="Enter yearly taxes first, then purchase details.")

        self._configure_style()
        self._build_ui()
        self.calculate_mortgage()
        self.calculate_sale()
        self.calculate_purchase()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f6f3ee")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f6f3ee", foreground="#222222", font=("Helvetica", 13))
        style.configure("Muted.TLabel", foreground="#6b6258", font=("Helvetica", 11))
        style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), foreground="#1f2933")
        style.configure("Result.TLabel", background="#ffffff", foreground="#0f766e", font=("Helvetica", 26, "bold"))
        style.configure("ResultLabel.TLabel", background="#ffffff", foreground="#6b6258", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 13, "bold"), padding=(16, 10))
        style.configure("Accent.TButton", foreground="#ffffff", background="#0f766e")
        style.map("Accent.TButton", background=[("active", "#115e59")])
        style.configure("TEntry", padding=8, font=("Helvetica", 14))
        style.configure("TNotebook", background="#f6f3ee", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 10), font=("Helvetica", 12, "bold"))

    def _build_ui(self):
        shell = ttk.Frame(self, padding=28)
        shell.pack(fill="both", expand=True)

        ttk.Label(shell, text="Mortgage Calculator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            shell,
            text="Estimate payments, sale proceeds, tax exposure, and purchase break-even timing.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(6, 22))

        tabs = ttk.Notebook(shell)
        tabs.pack(fill="both", expand=True)

        mortgage_tab = ttk.Frame(tabs, padding=(0, 20, 0, 0))
        sale_tab = ttk.Frame(tabs, padding=(0, 20, 0, 0))
        purchase_tab = ttk.Frame(tabs, padding=(0, 20, 0, 0))
        tabs.add(mortgage_tab, text="Mortgage")
        tabs.add(sale_tab, text="Sell Home")
        tabs.add(purchase_tab, text="New Purchase")

        self._build_mortgage_tab(mortgage_tab)
        self._build_sale_tab(sale_tab)
        self._build_purchase_tab(purchase_tab)

        self.bind("<Return>", lambda _event: self.calculate_active_tab(tabs))

    def _build_mortgage_tab(self, parent):
        form = ttk.Frame(parent)
        form.pack(fill="x")

        self._add_field(form, "Loan Amount", self.loan_amount, "$")
        self._add_field(form, "Annual Interest Rate", self.annual_rate, "%")
        self._add_field(form, "Loan Term", self.loan_years, "years")

        actions = ttk.Frame(parent)
        actions.pack(fill="x", pady=(18, 20))
        ttk.Button(actions, text="Calculate", style="Accent.TButton", command=self.calculate_mortgage).pack(side="left")
        ttk.Button(actions, text="Clear", command=self.clear_mortgage).pack(side="left", padx=(10, 0))

        results = ttk.Frame(parent, style="Panel.TFrame", padding=22)
        results.pack(fill="both", expand=True)

        ttk.Label(results, text="Monthly Payment", style="ResultLabel.TLabel").pack(anchor="w")
        ttk.Label(results, textvariable=self.monthly_payment, style="Result.TLabel").pack(anchor="w", pady=(4, 16))

        grid = ttk.Frame(results, style="Panel.TFrame")
        grid.pack(fill="x")
        self._add_result(grid, "Total Interest", self.total_interest, 0)
        self._add_result(grid, "Total Paid", self.total_paid, 1)

        ttk.Label(parent, textvariable=self.status, style="Muted.TLabel").pack(anchor="w", pady=(16, 0))

    def _build_sale_tab(self, parent):
        form = ttk.Frame(parent)
        form.pack(fill="x")

        self._add_field(form, "Initial Cost", self.initial_cost, "$")
        self._add_field(form, "Sale Price", self.sale_price, "$")
        self._add_field(form, "Selling Costs", self.selling_costs, "$")
        self._add_field(form, "Tax Rate", self.tax_rate, "%")

        actions = ttk.Frame(parent)
        actions.pack(fill="x", pady=(18, 20))
        ttk.Button(actions, text="Calculate", style="Accent.TButton", command=self.calculate_sale).pack(side="left")
        ttk.Button(actions, text="Clear", command=self.clear_sale).pack(side="left", padx=(10, 0))

        results = ttk.Frame(parent, style="Panel.TFrame", padding=22)
        results.pack(fill="both", expand=True)

        ttk.Label(results, text="Net Proceeds", style="ResultLabel.TLabel").pack(anchor="w")
        ttk.Label(results, textvariable=self.net_proceeds, style="Result.TLabel").pack(anchor="w", pady=(4, 16))

        grid = ttk.Frame(results, style="Panel.TFrame")
        grid.pack(fill="x")
        self._add_result(grid, "Tax-Free Gain", self.excluded_gain, 0)
        self._add_result(grid, "Taxable Gain", self.taxable_gain, 1)

        bottom_grid = ttk.Frame(results, style="Panel.TFrame")
        bottom_grid.pack(fill="x", pady=(18, 0))
        self._add_result(bottom_grid, "Estimated Tax", self.estimated_tax, 0)
        self._add_result(bottom_grid, "Profit After Tax", self.profit_after_tax, 1)

        ttk.Label(parent, textvariable=self.sale_status, style="Muted.TLabel").pack(anchor="w", pady=(16, 0))

    def _build_purchase_tab(self, parent):
        form = ttk.Frame(parent)
        form.pack(fill="x")

        self._add_field(form, "Yearly Taxes", self.purchase_yearly_taxes, "$")
        self._add_field(form, "Purchase Price", self.purchase_price, "$")
        self._add_field(form, "Down Payment", self.purchase_down_payment, "$")
        self._add_field(form, "Annual Interest Rate", self.purchase_rate, "%")
        self._add_field(form, "Loan Term", self.purchase_years, "years")

        actions = ttk.Frame(parent)
        actions.pack(fill="x", pady=(18, 20))
        ttk.Button(actions, text="Calculate", style="Accent.TButton", command=self.calculate_purchase).pack(side="left")
        ttk.Button(actions, text="Clear", command=self.clear_purchase).pack(side="left", padx=(10, 0))

        results = ttk.Frame(parent, style="Panel.TFrame", padding=22)
        results.pack(fill="both", expand=True)

        ttk.Label(results, text="Total Monthly Cost", style="ResultLabel.TLabel").pack(anchor="w")
        ttk.Label(results, textvariable=self.purchase_total_monthly, style="Result.TLabel").pack(
            anchor="w",
            pady=(4, 16),
        )

        grid = ttk.Frame(results, style="Panel.TFrame")
        grid.pack(fill="x")
        self._add_result(grid, "Mortgage Payment", self.purchase_monthly_payment, 0)
        self._add_result(grid, "Monthly Taxes", self.purchase_monthly_taxes, 1)

        cost_grid = ttk.Frame(results, style="Panel.TFrame")
        cost_grid.pack(fill="x", pady=(18, 0))
        self._add_result(cost_grid, "Annual Cost", self.purchase_annual_cost, 0)
        self._add_result(cost_grid, "Sale Tax Savings", self.purchase_tax_savings, 1)

        break_even_grid = ttk.Frame(results, style="Panel.TFrame")
        break_even_grid.pack(fill="x", pady=(18, 0))
        self._add_result(break_even_grid, "Yearly Tax Break-Even", self.tax_break_even_years, 0)

        ttk.Label(parent, textvariable=self.purchase_status, style="Muted.TLabel").pack(anchor="w", pady=(16, 0))

    def _add_field(self, parent, label, variable, suffix):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=7)

        ttk.Label(row, text=label, width=20).pack(side="left")
        entry = ttk.Entry(row, textvariable=variable)
        entry.pack(side="left", fill="x", expand=True)
        ttk.Label(row, text=suffix, width=7, anchor="e", style="Muted.TLabel").pack(side="left", padx=(10, 0))

    def _add_result(self, parent, label, variable, column):
        panel = ttk.Frame(parent, style="Panel.TFrame")
        panel.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 14, 0))
        parent.columnconfigure(column, weight=1)

        ttk.Label(panel, text=label, style="ResultLabel.TLabel").pack(anchor="w")
        ttk.Label(panel, textvariable=variable, background="#ffffff", font=("Helvetica", 18, "bold")).pack(
            anchor="w",
            pady=(4, 0),
        )

    def calculate_active_tab(self, tabs):
        if tabs.index(tabs.select()) == 0:
            self.calculate_mortgage()
        elif tabs.index(tabs.select()) == 1:
            self.calculate_sale()
        else:
            self.calculate_purchase()

    def calculate_mortgage(self):
        try:
            principal = self._number(self.loan_amount.get())
            annual_rate = self._number(self.annual_rate.get())
            years = int(self._number(self.loan_years.get()))

            monthly, interest = mortgage_interest_calculator(principal, annual_rate, years)
            total = principal + interest

            self.monthly_payment.set(self._money(monthly))
            self.total_interest.set(self._money(interest))
            self.total_paid.set(self._money(total))
            self.status.set("Estimate updated.")
        except ValueError as error:
            self.status.set(str(error) or "Please enter valid numbers.")

    def calculate_sale(self):
        try:
            sale = self._sale_summary()

            self.net_proceeds.set(self._money(sale["net_proceeds"]))
            self.excluded_gain.set(self._money(sale["excluded_gain"]))
            self.taxable_gain.set(self._money(sale["taxable_gain"]))
            self.estimated_tax.set(self._money(sale["estimated_tax"]))
            self.profit_after_tax.set(self._money(sale["profit_after_tax"]))
            self.sale_status.set("Sale estimate updated. First $500,000 of qualifying gain is excluded.")
        except ValueError as error:
            self.sale_status.set(str(error) or "Please enter valid numbers.")

    def calculate_purchase(self):
        try:
            yearly_taxes = self._number(self.purchase_yearly_taxes.get())
            purchase_price = self._number(self.purchase_price.get())
            down_payment = self._number(self.purchase_down_payment.get())
            annual_rate = self._number(self.purchase_rate.get())
            years = int(self._number(self.purchase_years.get()))

            if yearly_taxes <= 0:
                raise ValueError("Yearly taxes must be greater than zero.")
            if purchase_price <= 0:
                raise ValueError("Purchase price must be greater than zero.")
            if down_payment < 0:
                raise ValueError("Down payment cannot be negative.")
            if down_payment >= purchase_price:
                raise ValueError("Down payment must be less than the purchase price.")
            if annual_rate < 0:
                raise ValueError("Annual interest rate cannot be negative.")
            if years <= 0:
                raise ValueError("Loan term must be greater than zero.")

            loan_amount = purchase_price - down_payment
            monthly_payment, _interest = mortgage_interest_calculator(loan_amount, annual_rate, years)
            monthly_taxes = yearly_taxes / 12
            total_monthly = monthly_payment + monthly_taxes
            annual_cost = monthly_payment * 12 + yearly_taxes

            sale = self._sale_summary()
            tax_savings = sale["excluded_gain"] * sale["tax_rate"] / 100
            break_even_years = tax_savings / yearly_taxes

            self.purchase_monthly_payment.set(self._money(monthly_payment))
            self.purchase_monthly_taxes.set(self._money(monthly_taxes))
            self.purchase_total_monthly.set(self._money(total_monthly))
            self.purchase_annual_cost.set(self._money(annual_cost))
            self.purchase_tax_savings.set(self._money(tax_savings))
            self.tax_break_even_years.set(f"{break_even_years:,.1f} years")
            self.purchase_status.set("Purchase estimate updated using current Sell Home values.")
        except ValueError as error:
            self.purchase_status.set(str(error) or "Please enter valid numbers.")

    def clear_mortgage(self):
        self.loan_amount.set("")
        self.annual_rate.set("")
        self.loan_years.set("")
        self.monthly_payment.set("$0.00")
        self.total_interest.set("$0.00")
        self.total_paid.set("$0.00")
        self.status.set("Fields cleared.")

    def clear_sale(self):
        self.initial_cost.set("")
        self.sale_price.set("")
        self.selling_costs.set("")
        self.tax_rate.set("")
        self.net_proceeds.set("$0.00")
        self.excluded_gain.set("$0.00")
        self.taxable_gain.set("$0.00")
        self.estimated_tax.set("$0.00")
        self.profit_after_tax.set("$0.00")
        self.sale_status.set("Fields cleared.")

    def clear_purchase(self):
        self.purchase_yearly_taxes.set("")
        self.purchase_price.set("")
        self.purchase_down_payment.set("")
        self.purchase_rate.set("")
        self.purchase_years.set("")
        self.purchase_monthly_payment.set("$0.00")
        self.purchase_monthly_taxes.set("$0.00")
        self.purchase_total_monthly.set("$0.00")
        self.purchase_annual_cost.set("$0.00")
        self.purchase_tax_savings.set("$0.00")
        self.tax_break_even_years.set("0.0 years")
        self.purchase_status.set("Fields cleared.")

    def _sale_summary(self):
        initial_cost = self._number(self.initial_cost.get())
        sale_price = self._number(self.sale_price.get())
        selling_costs = self._number(self.selling_costs.get())
        tax_rate = self._number(self.tax_rate.get())

        if initial_cost < 0:
            raise ValueError("Initial cost cannot be negative.")
        if sale_price <= 0:
            raise ValueError("Sale price must be greater than zero.")
        if selling_costs < 0:
            raise ValueError("Selling costs cannot be negative.")
        if tax_rate < 0:
            raise ValueError("Tax rate cannot be negative.")

        net_proceeds = sale_price - selling_costs
        total_gain = max(0, sale_price - initial_cost - selling_costs)
        excluded_gain = min(total_gain, HOME_SALE_GAIN_EXCLUSION)
        taxable_gain = max(0, total_gain - HOME_SALE_GAIN_EXCLUSION)
        estimated_tax = taxable_gain * tax_rate / 100
        profit_after_tax = net_proceeds - initial_cost - estimated_tax

        return {
            "net_proceeds": net_proceeds,
            "total_gain": total_gain,
            "excluded_gain": excluded_gain,
            "taxable_gain": taxable_gain,
            "estimated_tax": estimated_tax,
            "profit_after_tax": profit_after_tax,
            "tax_rate": tax_rate,
        }

    @staticmethod
    def _number(value):
        return float(value.replace(",", "").replace("$", "").replace("%", "").strip())

    @staticmethod
    def _money(value):
        return f"${value:,.2f}"


if __name__ == "__main__":
    MortgageCalculatorApp().mainloop()
