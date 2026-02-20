"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import time
import os

from backend.config import settings
from backend.api import auth, data, transactions, ml, predictions, portfolio, risk, robo_advisory, tax, compliance, resume

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="End-to-End FinTech Analytics & Robo Advisory Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Session middleware (must be added before other middleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600  # 1 hour
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(data.router, prefix=settings.API_V1_PREFIX)
app.include_router(transactions.router, prefix=settings.API_V1_PREFIX)
app.include_router(ml.router, prefix=settings.API_V1_PREFIX)
app.include_router(predictions.router, prefix=settings.API_V1_PREFIX)
app.include_router(portfolio.router, prefix=settings.API_V1_PREFIX)
app.include_router(risk.router, prefix=settings.API_V1_PREFIX)
app.include_router(robo_advisory.router, prefix=settings.API_V1_PREFIX)
app.include_router(tax.router, prefix=settings.API_V1_PREFIX)
app.include_router(compliance.router, prefix=settings.API_V1_PREFIX)
app.include_router(resume.router, prefix=settings.API_V1_PREFIX)


# Mount static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates
templates = Jinja2Templates(directory="frontend/html") if os.path.exists("frontend/html") else None


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint - serve modern landing page
    """
    if templates:
        try:
            return templates.TemplateResponse("landing.html", {"request": request})
        except:
            pass
    
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FinSight AI</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .link { display: inline-block; margin: 10px; padding: 10px 20px; background: #10b981; color: white; text-decoration: none; border-radius: 5px; }
            .link:hover { background: #059669; }
        </style>
    </head>
    <body>
        <h1>🚀 FinSight AI Platform</h1>
        <p>Welcome to FinSight AI - Your End-to-End FinTech Analytics & Robo Advisory Platform</p>
        <h2>Quick Links</h2>
        <p>Please use the proper landing page template or dashboard.</p>
    </body>
    </html>
    """)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page"""
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Dashboard</h1><p>Template not found</p>")


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    """Portfolio management page"""
    if templates:
        try:
            return templates.TemplateResponse("portfolio.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Portfolio</h1><p>Template not found</p>")


@app.get("/risk", response_class=HTMLResponse)
async def risk_analysis(request: Request):
    """Risk analysis page"""
    if templates:
        try:
            return templates.TemplateResponse("risk.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Risk Analysis</h1><p>Template not found</p>")


@app.get("/predictions", response_class=HTMLResponse)
async def predictions(request: Request):
    """ML predictions page"""
    if templates:
        try:
            return templates.TemplateResponse("predictions.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>ML Predictions</h1><p>Template not found</p>")


@app.get("/robo-advisor", response_class=HTMLResponse)
async def robo_advisor(request: Request):
    """Robo advisor page"""
    if templates:
        try:
            return templates.TemplateResponse("robo-advisor.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Robo Advisor</h1><p>Template not found</p>")


@app.get("/tax", response_class=HTMLResponse)
async def tax_calculator(request: Request):
    """Tax calculator page"""
    if templates:
        try:
            return templates.TemplateResponse("tax.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Tax Calculator</h1><p>Template not found</p>")


@app.get("/transactions", response_class=HTMLResponse)
async def transactions(request: Request):
    """Transaction analysis page"""
    if templates:
        try:
            return templates.TemplateResponse("transactions.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Transaction Analysis</h1><p>Template not found</p>")


@app.get("/data", response_class=HTMLResponse)
async def data_management(request: Request):
    """Data management page"""
    if templates:
        try:
            return templates.TemplateResponse("data.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Data Management</h1><p>Template not found</p>")


@app.get("/compliance", response_class=HTMLResponse)
async def compliance(request: Request):
    """Compliance page"""
    if templates:
        try:
            return templates.TemplateResponse("compliance.html", {"request": request})
        except:
            pass
    return HTMLResponse(content="<h1>Compliance</h1><p>Template not found</p>")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Dashboard page
    """
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    return HTMLResponse(content="<h1>Dashboard not available</h1>")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Redirect to landing page - using Google OAuth only
    """
    return RedirectResponse(url="/")


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Redirect to landing page - using Google OAuth only
    """
    return RedirectResponse(url="/")


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(request: Request):
    """
    Portfolio page
    """
    if templates:
        return templates.TemplateResponse("portfolio.html", {"request": request})
    return HTMLResponse(content="<h1>Portfolio page not available</h1>")


@app.get("/risk", response_class=HTMLResponse)
async def risk_page(request: Request):
    """
    Risk assessment page
    """
    if templates:
        return templates.TemplateResponse("risk.html", {"request": request})
    return HTMLResponse(content="<h1>Risk assessment page not available</h1>")


@app.get("/predictions", response_class=HTMLResponse)
async def predictions_page(request: Request):
    """
    Predictions page
    """
    if templates:
        return templates.TemplateResponse("predictions.html", {"request": request})
    return HTMLResponse(content="<h1>Predictions page not available</h1>")


@app.get("/robo-advisor", response_class=HTMLResponse)
async def robo_advisor_page(request: Request):
    """
    Robo-advisor page
    """
    if templates:
        return templates.TemplateResponse("robo-advisor.html", {"request": request})
    return HTMLResponse(content="<h1>Robo-advisor page not available</h1>")


@app.get("/tax", response_class=HTMLResponse)
async def tax_page(request: Request):
    """
    Tax optimization page
    """
    if templates:
        return templates.TemplateResponse("tax.html", {"request": request})
    return HTMLResponse(content="<h1>Tax optimization page not available</h1>")


@app.get("/capstone", response_class=HTMLResponse)
async def capstone_page(request: Request):
    """
    Capstone project page
    """
    if templates:
        return templates.TemplateResponse("capstone.html", {"request": request})
    return HTMLResponse(content="<h1>Capstone project page not available</h1>")


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
