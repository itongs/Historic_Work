###################################################################################################


# Assignment 7 AR(2) Model


# author:         Ian Tongs, 27765369
# since:          10 May 2020

###################################################################################################



library(fpp3)
library(forecast)



###################################################################################################
# Main Function:
###################################################################################################


ar2 <- function(n, c, phi1, phi2, sigma) {
  # Check stationarity:
  if ( (abs(phi2) >= 1) || (phi1 + phi2 >= 1) || (phi2 - phi1 >= 1) ) { 
    warning( "Stationarity conditions violated, cannot compute for given inputs." ) 
  }else {
    # Establish the starting values for the AR2 model:
    ar <- numeric(n)
    ar[1] <- c/(1-phi1-phi2)
    ar[2] <- c/(1-phi1-phi2)
    
    # Main loop:
    for (i in 3:n) {
      rnormvectorval <- rnorm(1, mean=0, sd=sigma)
      ar[i] <- c + phi1*ar[i-1] + phi2*ar[i-2] + rnormvectorval[1]
    }
    
    # Return the AR2 vector:
    return (ar) 
  }
}




###################################################################################################
# Testing:
###################################################################################################


#should_work <- ar2(100, 8, 1.3, 0.7, 1)
#should_work

