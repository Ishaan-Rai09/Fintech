"""
Tax calculation service
"""
from typing import Dict, Any, List


class TaxCalculator:
    """Indian Income Tax calculator"""
    
    # FY 2025-26 Tax Slabs (New Regime)
    NEW_REGIME_SLABS = [
        (300000, 0),      # Up to 3L - 0%
        (700000, 0.05),   # 3L to 7L - 5%
        (1000000, 0.10),  # 7L to 10L - 10%
        (1200000, 0.15),  # 10L to 12L - 15%
        (1500000, 0.20),  # 12L to 15L - 20%
        (float('inf'), 0.30)  # Above 15L - 30%
    ]
    
    # FY 2025-26 Tax Slabs (Old Regime)
    OLD_REGIME_SLABS = [
        (250000, 0),      # Up to 2.5L - 0%
        (500000, 0.05),   # 2.5L to 5L - 5%
        (1000000, 0.20),  # 5L to 10L - 20%
        (float('inf'), 0.30)  # Above 10L - 30%
    ]
    
    # Standard Deduction
    STANDARD_DEDUCTION = 50000
    
    # Common Deductions (Old Regime)
    DEDUCTIONS = {
        "80C": {"max": 150000, "description": "PPF, ELSS, Life Insurance, etc."},
        "80D": {"max": 25000, "description": "Health Insurance"},
        "80G": {"description": "Donations"},
        "24": {"description": "Home Loan Interest"}
    }
    
    @staticmethod
    def calculate_tax_new_regime(gross_income: float) -> Dict[str, Any]:
        """Calculate tax under new regime"""
        taxable_income = gross_income - TaxCalculator.STANDARD_DEDUCTION
        
        tax = 0
        prev_slab = 0
        
        for slab_limit, rate in TaxCalculator.NEW_REGIME_SLABS:
            if taxable_income <= prev_slab:
                break
            
            taxable_in_slab = min(taxable_income, slab_limit) - prev_slab
            tax += taxable_in_slab * rate
            prev_slab = slab_limit
            
            if taxable_income <= slab_limit:
                break
        
        # Add cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            "regime": "New",
            "gross_income": gross_income,
            "standard_deduction": TaxCalculator.STANDARD_DEDUCTION,
            "taxable_income": taxable_income,
            "tax_before_cess": round(tax, 2),
            "cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / gross_income * 100), 2) if gross_income > 0 else 0,
            "net_income": round(gross_income - total_tax, 2)
        }
    
    @staticmethod
    def calculate_tax_old_regime(gross_income: float, deductions: Dict[str, float]) -> Dict[str, Any]:
        """Calculate tax under old regime with deductions"""
        # Apply deductions
        total_deductions = TaxCalculator.STANDARD_DEDUCTION
        deduction_details = {"standard_deduction": TaxCalculator.STANDARD_DEDUCTION}
        
        for deduction_type, amount in deductions.items():
            if deduction_type in TaxCalculator.DEDUCTIONS:
                max_allowed = TaxCalculator.DEDUCTIONS[deduction_type].get("max", float('inf'))
                allowed = min(amount, max_allowed)
                total_deductions += allowed
                deduction_details[deduction_type] = allowed
        
        taxable_income = max(0, gross_income - total_deductions)
        
        tax = 0
        prev_slab = 0
        
        for slab_limit, rate in TaxCalculator.OLD_REGIME_SLABS:
            if taxable_income <= prev_slab:
                break
            
            taxable_in_slab = min(taxable_income, slab_limit) - prev_slab
            tax += taxable_in_slab * rate
            prev_slab = slab_limit
            
            if taxable_income <= slab_limit:
                break
        
        # Add cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            "regime": "Old",
            "gross_income": gross_income,
            "total_deductions": total_deductions,
            "deduction_details": deduction_details,
            "taxable_income": taxable_income,
            "tax_before_cess": round(tax, 2),
            "cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / gross_income * 100), 2) if gross_income > 0 else 0,
            "net_income": round(gross_income - total_tax, 2)
        }
    
    @staticmethod
    def compare_regimes(gross_income: float, deductions: Dict[str, float] = None) -> Dict[str, Any]:
        """Compare tax under both regimes"""
        if deductions is None:
            deductions = {}
        
        new_regime = TaxCalculator.calculate_tax_new_regime(gross_income)
        old_regime = TaxCalculator.calculate_tax_old_regime(gross_income, deductions)
        
        savings = old_regime["total_tax"] - new_regime["total_tax"]
        
        return {
            "new_regime": new_regime,
            "old_regime": old_regime,
            "recommended_regime": "New" if new_regime["total_tax"] < old_regime["total_tax"] else "Old",
            "savings_with_recommended": abs(savings),
            "comparison": f"{'New regime saves' if savings > 0 else 'Old regime saves'} ₹{abs(savings):.2f}"
        }
    
    @staticmethod
    def tax_planning_suggestions(gross_income: float) -> List[Dict[str, str]]:
        """Provide tax planning suggestions"""
        suggestions = []
        
        if gross_income > 1000000:
            suggestions.append({
                "category": "80C Investments",
                "suggestion": "Invest in ELSS, PPF, or EPF to save up to ₹46,800 in taxes",
                "potential_saving": "₹46,800"
            })
        
        if gross_income > 500000:
            suggestions.append({
                "category": "Health Insurance",
                "suggestion": "Buy health insurance to claim 80D deduction (up to ₹25,000)",
                "potential_saving": "₹7,800"
            })
        
        suggestions.append({
            "category": "NPS",
            "suggestion": "Invest in NPS for additional 80CCD(1B) benefit of ₹50,000",
            "potential_saving": "₹15,600"
        })
        
        return suggestions
