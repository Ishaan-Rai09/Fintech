"""
Startup script for FinSight AI application
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 Starting FinSight AI Platform")
    print("=" * 70)
    print("\n📊 Feature Modules:")
    print("  ✅ Data Management & Analysis")
    print("  ✅ Transaction Analysis & Fraud Detection")
    print("  ✅ Machine Learning Pipeline")
    print("  ✅ Time Series Forecasting")
    print("  ✅ Portfolio Optimization (MPT)")
    print("  ✅ VaR Risk Calculator (3 Methods)")
    print("  ✅ Robo Advisory Engine")
    print("  ✅ Tax Calculator (Indian FY 2025-26)")
    print("  ✅ Compliance Checker (RBI/SEBI/KYC)")
    print("  ✅ Web Scraping (Yahoo Finance, NSE, BSE)")
    print("  ✅ Capstone Dashboard (Dual-Stock VaR Analysis)")
    print("\n🌐 Server will be available at:")
    print("  • Frontend: http://localhost:8000")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • ReDoc:    http://localhost:8000/redoc")
    print("  • Health:   http://localhost:8000/health")
    print("\n💡 Login with your credentials or register a new account")
    print("=" * 70)
    print("\n")
    
    # Run the application
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
