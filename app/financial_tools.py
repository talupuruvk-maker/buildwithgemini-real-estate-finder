# Copyright 2026 Google LLC
# Financial & Mortgage Calculator Tools for Real-Estate Agent

from typing import Dict, Any


def calculate_mortgage_payment(
    home_price: float,
    down_payment_pct: float = 20.0,
    interest_rate_pct: float = 6.5,
    loan_term_years: int = 30,
    annual_tax_rate_pct: float = 1.2,
    monthly_hoa_fee: float = 0.0,
) -> Dict[str, Any]:
    """Calculate estimated monthly mortgage payment, taxes, HOA fees, and total housing cost.

    Args:
        home_price: Total purchase price of the home in USD (e.g., 850000).
        down_payment_pct: Down payment percentage (e.g., 20 for 20%). Default is 20.0.
        interest_rate_pct: Annual mortgage interest rate percentage (e.g., 6.5 for 6.5%). Default is 6.5.
        loan_term_years: Duration of the loan in years (e.g., 30 or 15). Default is 30.
        annual_tax_rate_pct: Estimated annual property tax percentage (e.g., 1.2 for 1.2%). Default is 1.2.
        monthly_hoa_fee: Monthly HOA or condo maintenance fee in USD. Default is 0.0.

    Returns:
        Dictionary with detailed financial breakdown including down payment amount, loan principal,
        monthly principal & interest, monthly property tax, monthly HOA, and total monthly payment.
    """
    down_payment_amount = home_price * (down_payment_pct / 100.0)
    principal = home_price - down_payment_amount
    
    monthly_interest_rate = (interest_rate_pct / 100.0) / 12.0
    num_payments = loan_term_years * 12
    
    if monthly_interest_rate > 0:
        monthly_pi = principal * (
            (monthly_interest_rate * ((1 + monthly_interest_rate) ** num_payments))
            / (((1 + monthly_interest_rate) ** num_payments) - 1)
        )
    else:
        monthly_pi = principal / num_payments if num_payments > 0 else 0
        
    monthly_property_tax = (home_price * (annual_tax_rate_pct / 100.0)) / 12.0
    total_monthly_payment = monthly_pi + monthly_property_tax + monthly_hoa_fee
    
    return {
        "home_price": round(home_price, 2),
        "down_payment_pct": down_payment_pct,
        "down_payment_amount": round(down_payment_amount, 2),
        "loan_principal": round(principal, 2),
        "interest_rate_pct": interest_rate_pct,
        "loan_term_years": loan_term_years,
        "monthly_principal_and_interest": round(monthly_pi, 2),
        "monthly_property_tax": round(monthly_property_tax, 2),
        "monthly_hoa_fee": round(monthly_hoa_fee, 2),
        "total_monthly_payment": round(total_monthly_payment, 2),
    }
