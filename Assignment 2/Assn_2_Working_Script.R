###################################################################################################


# Assignment Two for ETC3555, S2 2020


# author:         Ian Tongs, 27765369
# since:          9th September, 2020

###################################################################################################

# Imports
library(dplyr)
library(readr)
library(tidyverse)
library(ggplot2)
library(gridExtra)
library(grid)
library(cowplot)

######################          Convert into RMD Before submission          #######################




##############################          Practice Samples          #################################
set.seed(1900)
# Function taken from Friedman et al.
genx <- function(n,p,rho){
  # generate x's multivariate normal with equal corr rho
  # Xi = b Z + Wi, and Z, Wi are independent normal.
  # Then Var(Xi) = b^2 + 1
  # Cov(Xi, Xj) = b^2 and so cor(Xi, Xj) = b^2 / (1+b^2) = rho
  z <- rnorm(n)
  if(abs(rho) < 1){
    beta <- sqrt(rho/(1-rho))
    x <- matrix(rnorm(n*p), ncol=p)
    A <- matrix(rnorm(n), nrow=n, ncol=p, byrow=F)
    x <- beta * A + x
  }
  if(abs(rho)==1){ x=matrix(rnorm(n),nrow=n,ncol=p,byrow=F)}
  return(x)
}
N <- 100
p <- 10
rho <- 0.2
X <- genx(N, p, rho)
w_true <- ((-1)^(1:p))*exp(-2*((1:p)-1)/20)
eps <- rnorm(N)
k <- 3
y <- X %*% w_true + k * eps



###################################################################################################
# Compute In Sample Error - Linreg:
###################################################################################################


Ein_linreg <- function(X, y, w){
  # Calculates the Input Error for linear regression with a vector w of weights and X and y inputs
  n <- nrow(y)
  Ein_raw <- 0
  
  # Main loop for calculating error:
  for (i in 1:n) {
    Ein_raw <- Ein_raw + (t(w) %*% X[i, ] - y[i])^2
  }
  Ein <- (1/n)*Ein_raw
  
  return(Ein)
}

# Subtle testing with random inputs and w_true
Ein_linreg(X, y, w_true)



###################################################################################################
# Compute In Sample Error - Logreg:
###################################################################################################


Ein_logreg <- function(X, y, w){
  # Calculates the Input Error for linear regression with a vector w of weights and X and y inputs
  n <- nrow(y)
  Ein_raw <- 0
  
  # Main loop for calculating error:
  for (i in 1:n) {
    Ein_raw <- Ein_raw + log(1 + exp(- y[i]*(t(w) %*% X[i, ])))
  }
  Ein <- (1/n)*Ein_raw
  
  return(Ein)
}

# Subtle testing with random inputs and w_true
Ein_logreg(X, y, w_true)






###################################################################################################
# Compute In Gradient - Linreg:
###################################################################################################



gEin_linreg <- function(X, y, w){
  # Computes the (linear) gradient for a set of weights and an input X and y matrices
  n <- nrow(y)
  grad_raw <- 0
  
  # Main loop for calculating gradient:
  for (i in 1:n) {
    grad_raw <- grad_raw + (t(w) %*% X[i, ] - y[i])*X[i, ]
  }
  grad <- (2/n)*grad_raw
  
  return(grad)
}

# Subtle testing with random inputs and w_true
gEin_linreg(X, y, w_true)





###################################################################################################
# Compute In Gradient - Logreg:
###################################################################################################



gEin_logreg <- function(X, y, w){
  # Computes the (logistic) gradient for a set of weights and an input X and y matrices
  n <- nrow(y)
  grad_raw <- 0
  
  # Main loop for calculating gradient:
  for (i in 1:n) {
    grad_raw <- grad_raw + (y[i]*X[i, ])/(1 + exp(y[i]*(t(w) %*% X[i, ])))
  }
  grad <- (-1/n)*grad_raw
  
  return(grad)
}

# Subtle testing with random inputs and w_true
gEin_logreg(X, y, w_true)




###################################################################################################
# Compute Gradient Descent
###################################################################################################

# X: an input matrix of dimension n × p.
# y: a response vector of dimension n × 1.
# Ein: a function which takes arguments X, y and w, and computes the in-sample error for w.
# gEin: a function which takes arguments X, y and w, and computes the gradient of Ein at w.
# w0: the initial weights
# eta: the learning rate
# precision: a small value
# nb_iters: the maximum number of iterations




GD <- function(X, y, Ein, gEin, w0, eta, precision, nb_iters){
  # Initial values as defined by the question:
  allw <- vector("list", nb_iters)
  cost <- numeric(nb_iters)
  allw[[1]] <- w0
  cost[1] <- Ein(X, y, allw[[1]])
  
  # Termination Variables:
  i <- 2
  Ein_old <- 0
  Ein_cur <- cost[1]
  Ein_diff <- abs(Ein_cur- Ein_old)

  # Main Loop - while less than the number of iterations and while precision above target:
  while (Ein_diff >= precision && i <= nb_iters) {
    
    # Add new results to results lists
    allw[[i]] <- allw[[i-1]] - eta * gEin(X, y,allw[[i-1]])
    cost[i] <- Ein(X, y, allw[[i-1]])
    
    # Update termination conditions
    Ein_old <- Ein_cur
    Ein_cur <- Ein(X, y, allw[[i]])
    Ein_diff <- abs(Ein_cur- Ein_old)
    i <- i + 1
  }
  
  # For making sure 'bottom row' is correct if terminated before max iterations:
  while (i <= nb_iters) {
    
    # Add new results to results lists
    allw[[i]] <- allw[[i-1]]
    cost[i] <- cost[i-1]
    
    # Update termination conditions
    i <- i + 1
  }  

  # Return the required values as a list, as required:
  list(allw = allw, cost = cost)
}











###################################################################################################
# Testing with GD.


set.seed(1900)
# Function taken from Friedman et al.
genx <- function(n,p,rho){
  # generate x's multivariate normal with equal corr rho
  # Xi = b Z + Wi, and Z, Wi are independent normal.
  # Then Var(Xi) = b^2 + 1
  # Cov(Xi, Xj) = b^2 and so cor(Xi, Xj) = b^2 / (1+b^2) = rho
  z <- rnorm(n)
  if(abs(rho) < 1){
    beta <- sqrt(rho/(1-rho))
    x <- matrix(rnorm(n*p), ncol=p)
    A <- matrix(rnorm(n), nrow=n, ncol=p, byrow=F)
    x <- beta * A + x
  }
  if(abs(rho)==1){ x=matrix(rnorm(n),nrow=n,ncol=p,byrow=F)}
  return(x)
}


N <- 100
p <- 10
rho <- 0.2
X <- genx(N, p, rho)
w_true <- ((-1)^(1:p))*exp(-2*((1:p)-1)/20)
eps <- rnorm(N)
k <- 3
y <- X %*% w_true + k * eps


res <- GD(X, y, Ein_linreg, gEin_linreg, rep(0, p), 0.01, 0.0001, 100)
plot(res$cost)

print(w_true)
print(unlist(tail(res$allw, 1)))





######## Testing Part 2:


set.seed(1900)
N <- 100
l <- -5; u <- 5
x <- seq(l, u, by = 0.1)
w_true <- matrix(c(-3, 1, 1), ncol = 1)
a <- -w_true[2]/w_true[3]
b <- -w_true[1]/w_true[3]

X0 <- matrix(runif(2 * N, l, u), ncol = 2)

X <- cbind(1, X0)
y <- sign(X %*% w_true)

res <- GD(X, y, Ein_logreg, gEin_logreg, rep(0, 3), 0.05, 0.0001, 500)
plot(res$cost)

print(w_true)
w_best <- unlist(tail(res$allw, 1))
print(w_best)

plot(c(l, u), c(u, l), type = 'n', xlab = "x1", ylab = "x2")
lines(x, a*x +b)
points(X0, col = ifelse(y == 1, "red", "blue"))

a_best <- -w_best[2]/w_best[3]
b_best <- -w_best[1]/w_best[3]
lines(x, a_best*x + b_best, col = "red")





###################################################################################################
# Stochastic gradient descent - change the grad functions
###################################################################################################


# Not required for the assignment!





###################################################################################################
# L2 - Add resularisations parameters to the grad vectors (?)
###################################################################################################


# Not required for the assignment!






