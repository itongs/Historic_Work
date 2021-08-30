###################################################################################################


# Assignment 5 Simple Exponential Smoothing Script


# author:         Ian Tongs, 27765369
# since:          30 April 2020

###################################################################################################



library(fpp3)
library(forecast)



###################################################################################################
# Main Function:
###################################################################################################


simple_exponential_smoothing_function <- function(y) {
  # Function taking a vector of numeric values
  # Returns a vector of the next 10 forecast values predicted by SES
  
  # Auxiliary function for smoothing with a given alpha an initial level
  simple_exponential_smoothing_auxiliary <- function(y, alpha, level){
    t <- length(y)
    l <- numeric(t + 1) # numeric creates a vector of zeroes of length t+1 (+1 for the forecast)
    l[1] <- level
    for (i in 2:(t+1)) {
      l[i] <- alpha * y[i-1] + (1 - alpha) * l[i - 1]
    }
    fcast <- l[t + 1]
    return(fcast)
  }
  
  # Returns the value of the SSE for the SES with par = c(alpha, level) )
  SSE_SES_aux <- function(y, par){
    alpha <- par[1]
    level <- par[2]
    t <- length(y)
    l <- numeric(t + 1) # numeric creates a vector of zeroes of length t+1 (+1 for the forecast)
    l[1] <- level
    for (i in 2:(t+1)) {
      l[i] <- alpha * y[i-1] + (1 - alpha) * l[i - 1]
    }
    SSE <- 0
    for (i in 1:t) {
      if (alpha>0) {
        SSE <- SSE + (y[i] - l[i])^2
      } else {
        SSE <- SSE + (y[i])^2
      }
    }
    return (SSE)
  }
  
  # Optimise the parameters for the forecast:
  optimised <- optim(par=c(0.6, y[1]), fn=SSE_SES_aux, y=y)
  alpha <- optimised$par[1]
  level_0 <- optimised$par[2]
  
  # Bug fixing:
  #print(optimised)
  #print(optimised$par)
  #print(SSE_SES_aux(y, optimised$par))
  #print(SSE_SES_aux(y, fit1$model$par))
  
  # Get the one step ahead forecast
  pred_val <- simple_exponential_smoothing_auxiliary(y, alpha, level_0)
  
  # As this is an SES model, all ten predictions are equal, so:
  forecast_vector <- numeric(10)
  for (i in 1:10) {
    forecast_vector[i] <- pred_val
  }
  
  # Return the forecast vector
  return (forecast_vector)
}




###################################################################################################
# Testing:
###################################################################################################

# y <- c(11,13,12,10,15,16,14,15,17,18,19,14,17,15,20)
# 
# simple_exponential_smoothing_function(y)       # Choose a y to get this to work
# 
# fit1 <- ses(y, h=1)
# fit1
# fit1$model$par