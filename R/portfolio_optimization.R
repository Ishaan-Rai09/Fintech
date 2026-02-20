# Portfolio Optimization in R: Enhanced with Interactive Visualization
# Packages: quadprog, PortfolioAnalytics, PerformanceAnalytics, ggplot2, dplyr, plotly, viridis

# --- 1. SETUP & DATA PREPARATION ---
packages <- c("quadprog", "PortfolioAnalytics", "PerformanceAnalytics", 
              "zoo", "xts", "ggplot2", "dplyr", "plotly", "lubridate", "viridis")

for (pkg in packages) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org")
    library(pkg, character.only = TRUE)
  }
}

# Generate synthetic returns for 4 assets
set.seed(42)
n_obs <- 252 # 1 year of trading days
asset_names <- c("Equity_US", "Equity_Intl", "Bonds", "Real_Estate")
returns <- matrix(rnorm(n_obs * 4, mean = 0.0005, sd = 0.01), nrow = n_obs)
colnames(returns) <- asset_names

# Use lubridate for dates
start_date <- ymd("2023-01-01")
dates <- start_date + days(0:(n_obs - 1))
returns_xts <- xts(returns, order.by = dates)

# --- 2. CORE OPTIMIZATION WRAPPER ---
get_portfolio_stats <- function(returns_data) {
  mu <- colMeans(returns_data)
  sigma <- cov(returns_data)
  
  # Quadprog for Min Variance
  n_assets <- ncol(returns_data)
  Dmat <- sigma
  dvec <- rep(0, n_assets)
  Amat <- cbind(rep(1, n_assets), diag(n_assets))
  bvec <- c(1, rep(0, n_assets))
  qp_result <- solve.QP(Dmat = Dmat, dvec = dvec, Amat = Amat, bvec = bvec, meq = 1)
  
  return(list(mu = mu, sigma = sigma, weights = qp_result$solution))
}

# --- 3. ADVANCED OPTIMIZATION (PortfolioAnalytics) ---
optimize_advanced <- function(returns_data) {
  port_spec <- portfolio.spec(assets = colnames(returns_data))
  port_spec <- add.constraint(portfolio = port_spec, type = "full_investment")
  port_spec <- add.constraint(portfolio = port_spec, type = "long_only")
  port_spec <- add.objective(portfolio = port_spec, type = "risk", name = "StdDev")
  port_spec <- add.objective(portfolio = port_spec, type = "return", name = "mean")
  
  opt_results <- optimize.portfolio(R = returns_data, portfolio = port_spec, 
                                    optimize_method = "random", search_size = 1000)
  return(opt_results)
}

# --- 4. ENHANCED VISUALIZATION FUNCTIONS ---
plot_asset_performance <- function(returns_data) {
  df <- data.frame(Date = index(returns_data), coredata(returns_data)) %>%
    tidyr::pivot_longer(-Date, names_to = "Asset", values_to = "Return") %>%
    group_by(Asset) %>%
    mutate(Cumulative_Return = cumprod(1 + Return) - 1)
  
  p <- ggplot(df, aes(x = Date, y = Cumulative_Return, color = Asset)) +
    geom_line() +
    scale_color_viridis_d() +
    theme_minimal() +
    labs(title = "Cumulative Returns by Asset", y = "Growth", x = "Date")
  
  return(ggplotly(p))
}

plot_risk_return <- function(returns_data) {
  mu <- colMeans(returns_data) * 252
  sd <- apply(returns_data, 2, sd) * sqrt(252)
  
  df_scatter <- data.frame(
    Asset = names(mu),
    Return = mu,
    Risk = sd
  )
  
  p <- ggplot(df_scatter, aes(x = Risk, y = Return, label = Asset)) +
    geom_point(aes(color = Asset), size = 4) +
    geom_text(vjust = -1) +
    scale_color_viridis_d() +
    theme_minimal() +
    labs(title = "Annualized Risk vs Return", x = "Risk (Annualized StdDev)", y = "Return (Annualized Mean)")
  
  return(ggplotly(p))
}

# Run initial analysis
stats <- get_portfolio_stats(returns_xts)
opt_adv <- optimize_advanced(returns_xts)


