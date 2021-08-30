###################################################################################################


# Assignment Onefor ETC3555, S2 2020


# author:         Ian Tongs, 27765369
# since:          26th August, 2020

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


###################################################################################################
# Exercise 1:
###################################################################################################


# What we need to do:
## Choose some function f in the 2D space
## Generate 20 random examples and assign by the function f
### This is now our training set
## Build a perceptron algorithm
## Train the perceptron algorithm on this dataset
## See how long it takes to converge as g -> f.


# Set Seed:
set.seed(27765369)

# Choose f, being a random line in two dimensions. As:
# Of the form: c1*X1 + c2*X2 + c3 = 0
# or rather: X2 = (-c1/c2)*X2 + (-c3/c2) 

c1 <- runif(1, -3, 3)
c2 <- runif(1, -3, 3)
c3 <- runif(1, -3, 3)


# Create the random dataset
X1 <- rnorm(20, mean=0, sd=3)
X2 <- rnorm(20, mean=0, sd=3)

# Check where to divide for X1:
dividing_line <- -(c1/c2)*X1 -(c3/c2)

# Use sign for Y if above this:
Y <- sign(X2 - dividing_line)


# Set the dataset:
Data_set <- tibble(X1, X2, 1, Y)


# Plot it:
Initial_plot <- ggplot(Data_set, aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(Y))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(c3/c2), slope = -(c1/c2), color="purple", linetype="solid", size=1.5) +
  ggtitle("Fig 1.1: Random 2D Classification Boundarty") +
  geom_vline(xintercept = 0, color="black") +
  geom_hline(yintercept = 0, color="black")

Initial_plot
# add legend for the line colours!

#### Now we want to implement perceptron:


# Set initial weights
weights = c(1, 2, 3)


# Use the sign to assign initial outcomes:
h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )


# Create a loop to repeatedly update the estimates:
while (sum(h_val == (Data_set %>% pull(Y))) < 20){
  for (i in (1:20)){
    if (h_val[i] != Y[i]){
      weights <- weights + Y[i] *  as.matrix(Data_set %>% select(1:3))[i, ]
    }
  }
  h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )
}



Later_Plot <- ggplot(Data_set, aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(Y))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(c3/c2), slope = -(c1/c2), color="purple", linetype="dashed", size=1.5) +
  ggtitle("Fig 1.2: Random 2D Classification Boundarty with Perceptron Boundary") +
  geom_vline(xintercept = 0, color="black") +
  geom_hline(yintercept = 0, color="black") +
  geom_abline(intercept = (-weights[3]/weights[2]), slope = (-weights[1]/weights[2]), color="red")

Later_Plot
# add legend for the line colours!

###################################################################################################
# Exercise 2:
###################################################################################################

# Build a coin flipper function - flipping 1000 coins 10 times each, and recording the frequency
# Select the following coins:
  # First coin flipped
  # A random coin
  # The minimum heads frequency 

sample_coins <- c("Tails", "Heads")
flip_matrix <- matrix(ncol = 10, nrow = 1000)

# Loop for flipping 1000 coins 10 times each
for (i in 1:1000) {
  flip_matrix[i, ] <- sample(sample_coins, 10, replace = TRUE)
}

# Loop to find the minimum value:
min_val <- 10
min_id <- 0
for (i in 1:1000) {
  cur_count <- sum(flip_matrix[i, ] == "Heads")
  # make min if min
  if (min_val > cur_count) {
    min_val <- cur_count
    min_id <- i
  }
}

# Choose the three bits:
c_1 <- flip_matrix[1, ]
c_min <- flip_matrix[min_id, ]
c_rand <- flip_matrix[sample(1000, 1), ]

# Find v vals:
v_1 <- mean(c_1 == "Heads")
v_min <- mean(c_min == "Heads")
v_rand <- mean(c_rand == "Heads")





###################################################################################################
############# Part A:

# mu for the three coins


# Find Mu:
mu <- mean(v_1, v_min, v_rand)
mu



###################################################################################################
############# Part B:

# repeat process 100000 times and plot the histograms

# Assign the number of runs:
runs <- 1000


# Define the output matrices:
mat_v_1 <- matrix(nrow=runs)
mat_v_min <- matrix(nrow=runs)
mat_v_rand <- matrix(nrow=runs)


# Run a loop of this fot each of the runs:
for (j in 1:runs) {
  
  # Loop to find the minimum value:
  min_val <- 10
  min_id <- 0
  
  # resamply flip matrix
  for (i in 1:1000) {
    flip_matrix[i, ] <- sample(sample_coins, 10, replace = TRUE)
  }
  
  # find min
  for (i in 1:1000) {
    cur_count <- sum(flip_matrix[i, ] == "Heads")
    # make min if min
    if (min_val > cur_count) {
      min_val <- cur_count
      min_id <- i
    }
  }
  
  # Choose each c:
  c_1 <- flip_matrix[1, ]
  c_min <- flip_matrix[min_id, ]
  c_rand <- flip_matrix[sample(1000, 1), ]

  
  # Put into result matrices:
  mat_v_1[j] <- mean(c_1 == "Heads")
  mat_v_min[j] <- mean(c_min == "Heads")
  mat_v_rand[j] <- mean(c_rand == "Heads")
}

# Now we should combine the results into a single dataframe:
Q2b_results_df <- data.frame(mat_v_1, mat_v_min, mat_v_rand)


# Plot each result:
plot_c1 <- ggplot(Q2b_results_df) +
  coord_cartesian(xlim = c(0,1), ylim = c(0,0.3*runs)) +
  scale_x_continuous(breaks=seq(0,1,0.05)) +
  labs(x="Probability", y="Frequency") + 
  geom_histogram(binwidth=0.1, aes(mat_v_1), fill="blue", colour="blue") +
  ggtitle(paste("First Coin from each Run"))

plot_crand <- ggplot(Q2b_results_df) +
  coord_cartesian(xlim = c(0,1), ylim = c(0,0.3*runs)) +
  scale_x_continuous(breaks=seq(0,1,0.05)) +
  labs(x="Probability", y="Frequency") + 
  geom_histogram(binwidth=0.1, aes(mat_v_rand), fill="green", colour="green") +
  ggtitle(paste("Random Coin from each Run"))

plot_cmin <- ggplot(Q2b_results_df) +
  coord_cartesian(xlim = c(0,1), ylim = c(0,0.75*runs)) +
  scale_x_continuous(breaks=seq(0,1,0.05)) +
  labs(x="Probability", y="Frequency") + 
  geom_histogram(binwidth=0.1, aes(mat_v_min), fill="red", colour="red") +
  ggtitle(paste("Minimum Heads Coin in each Run"))



# Combine all the plots into a single plot and display
plot_Q2B<- plot_grid(plot_c1, plot_crand, plot_cmin, nrow=3)

# Add the title:
q2b_title <- ggdraw() + draw_label(paste("Figure 2.1: \nSimulated Probability Distributions of \nHead Flips for Coins in", runs, "Coins"), fontface='bold')

#Combine the two and display
Full_plot_Q2B <- plot_grid(q2b_title, plot_Q2B, ncol=1, rel_heights=c(0.1, 1))
Full_plot_Q2B

# Make a comment on what this means!



###################################################################################################
############# Part C:

# Define the domain of epsilon:
epsilon <- seq(0, 0.50, 0.05)
n <- length(epsilon)
N <- 10

# Add dataset for the Hoffding bound:
hoeffding_bound <- function (epsilon, N = 10){
  bound_val <- 2*exp((-2*epsilon^2)*N)
  return (bound_val)
}

# Set up the values we want to analyse
Pr_c1 <- matrix(nrow = n)
Pr_crand <- matrix(nrow = n)
Pr_cmin <- matrix(nrow = n)

# Find the probability frequencies:
for (i in 1:length(epsilon)) {
  Pr_c1[i] <- sum(abs(mat_v_1 - mu) > epsilon[i])/runs
  Pr_crand[i] <- sum(abs(mat_v_rand - mu) > epsilon[i])/runs
  Pr_cmin[i] <- sum(abs(mat_v_min - mu) > epsilon[i])/runs
}

# Establish this as a dataframe
Pr_dataframe <- data.frame(epsilon, Pr_c1, Pr_crand, Pr_cmin)


# Plot the results:
plot_2ci <- ggplot(data = Pr_dataframe, aes(x=epsilon)) +
  stat_function(fun = hoeffding_bound) + 
  geom_histogram(binwidth=0.1, 
                          aes(y=Pr_c1), 
                          stat='identity', 
                          fill="yellow green", 
                          colour="forest green") + 
  ggtitle(paste("First Selected Coins selection:")) + 
  labs(y = "", x = "") 

plot_2cii <- ggplot(data = Pr_dataframe, aes(x=epsilon)) +
  stat_function(fun = hoeffding_bound) + 
  geom_histogram(binwidth=0.1, 
                 aes(y=Pr_crand), 
                 stat='identity', 
                 fill="sky blue", 
                 colour="blue") + 
  ggtitle(paste("Randomly Selected Coins selection:")) + 
  labs(y = "Pr[v-u] < epsilon ", x = "") 

plot_2ciii <- ggplot(data = Pr_dataframe, aes(x=epsilon)) +
  stat_function(fun = hoeffding_bound) + 
  geom_histogram(binwidth=0.1, 
                 aes(y=Pr_cmin), 
                 stat='identity', 
                 fill="salmon", 
                 colour="maroon") + 
  ggtitle(paste("Minimum Heads Coinsselection:")) + 
  labs(y = "", x = "Epsilon") 


# Combine all the plots into a single plot and display
plot_Q2C<- plot_grid(plot_2ci, plot_2cii, plot_2ciii, nrow=3)

# Add the title:
q2c_title <- ggdraw() + draw_label(paste("Figure 2.2: \nPr[v-u] < epsilon against epsilon \nOverlaid with Hoeffding's Bound"), fontface='bold')

#Combine the two and display
Full_plot_Q2C <- plot_grid(q2c_title, plot_Q2C, ncol=1, rel_heights=c(0.1, 1))
Full_plot_Q2C




###################################################################################################
############# Part D:

# The first coin and the randomly selected coin obey the Hoeffding bound. This is evident as their 
# probabilities at each level of epsilon are less than the bound. Both of these coin selections were
# made randomly - the random coins selected randomly at each step and the first coins set selected 
# once but as a random sample at each step. This indicates that these coins should be unbiased, as 
#is indicated by there adgerence to the bound. 

# The minimum proportion of heads coin, however, does not obey the bound. It may be observed that 
# by epsilon = ??????? is exceeds the bound. This may be explained from theory as the minimum heads
# coins is an inherently biased sample as a resuly of its selection method.







###################################################################################################
############# Part E:

# Different as the expected mu in each case should be 0.5 as each bin is drawn from the same sample

# Can be related as the c_min bin is drawn from a bin 'separate' from the main bin.











###################################################################################################
# Exercise 3:
###################################################################################################



###################################################################################################
############# Part A:

# Choose f, being a random line in two dimensions. As:
# Of the form: c1*X1 + c2*X2 + c3 = 0
# or rather: X2 = (-c1/c2)*X2 + (-c3/c2) 

c1 <- runif(1, -3, 3)
c2 <- runif(1, -3, 3)
c3 <- runif(1, -3, 3)


# Create the random dataset
X1 <- rnorm(20, mean=0, sd=3)
X2 <- rnorm(20, mean=0, sd=3)

# Check where to divide for X1:
dividing_line <- -(c1/c2)*X1 -(c3/c2)

# Use sign for Y if above this:
Y <- sign(X2 - dividing_line)


# Set the dataset:
Data_set <- tibble(X1, X2, 1, Y)


# Plot it:
Initial_plot <- ggplot(Data_set, aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(Y))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(c3/c2), slope = -(c1/c2), color="purple", linetype="solid", size=1.5) +
  ggtitle("Fig 3.1: Random 2D Classification Boundarty") +
  geom_vline(xintercept = 0, color="black") +
  geom_hline(yintercept = 0, color="black")

Initial_plot






###################################################################################################
############# Part B:

#### Now we want to implement perceptron:


# Set initial weights
weights = c(1, 2, 3)


# Use the sign to assign initial outcomes:
h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )

iterations <- 0
# Create a loop to repeatedly update the estimates:
while (sum(h_val == (Data_set %>% pull(Y))) < 20){
  for (i in (1:20)){
    # Primary if clause
    if (h_val[i] != Y[i]){
      weights <- weights + Y[i] *  as.matrix(Data_set %>% select(1:3))[i, ]
      # iterations += 1
      iterations <- iterations + 1
    }
  }
  h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )
}



# Print the number of iterations:
paste("For this dataset, for convergence to occue with with PLA, we required", iterations, "updates.")


Later_Plot <- ggplot(Data_set, aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(Y))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(c3/c2), slope = -(c1/c2), color="purple", linetype="dashed", size=1.5) +
  ggtitle("Fig 3.2: Random 2D Classification Boundarty with Perceptron Boundary") +
  geom_vline(xintercept = 0, color="black") +
  geom_hline(yintercept = 0, color="black") +
  geom_abline(intercept = (-weights[3]/weights[2]), slope = (-weights[1]/weights[2]), color="red")

Later_Plot
# add legend for the line colours!





###################################################################################################
############# Part C:

# Because of this repetition I'm going to make my sampling a function:
two_d_PLA_function <- function(sample_size){
  c1 <- runif(1, -3, 3)
  c2 <- runif(1, -3, 3)
  c3 <- runif(1, -3, 3)
  
  # record the real line values:
  real_weights <- c(c1, c2, c3)
  
  # Create the random dataset
  X1 <- rnorm(sample_size, mean=0, sd=3)
  X2 <- rnorm(sample_size, mean=0, sd=3)
  
  # Check where to divide for X1:
  dividing_line <- -(c1/c2)*X1 -(c3/c2)
  
  # Use sign for Y if above this:
  Y <- sign(X2 - dividing_line)
  
  
  # Set the dataset:
  Data_set <- tibble(X1, X2, 1, Y)
  
  # Set initial weights
  weights = c(1, 2, 3)
  
  
  # Use the sign to assign initial outcomes:
  h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )
  
  # record updates done:
  iterations <- 0
  
  # Create a loop to repeatedly update the estimates:
  while (sum(h_val == (Data_set %>% pull(Y))) < sample_size){
    for (i in (1:sample_size)){
      # Primary if clause
      if (h_val[i] != Y[i]){
        weights <- weights + Y[i] *  as.matrix(Data_set %>% select(1:3))[i, ]
        # iterations += 1
        iterations <- iterations + 1
      }
    }
    h_val <- sign( as.matrix(Data_set %>% select(1:3)) %*% weights )
  }
  
  return(list(iterations, weights, Data_set, real_weights, Y))
}

sample_size <- 20

sample_3c <- two_d_PLA_function(sample_size)

q3c_plot <- ggplot(sample_3c[[3]], aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(sample_3c[[5]]))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(sample_3c[[4]][[3]]/sample_3c[[4]][[2]]), slope = -(sample_3c[[4]][[1]]/sample_3c[[4]][[2]]), color="purple", linetype="dashed", size=1.5) +
  ggtitle("Fig 3.3: Another Random 2D Classification Boundarty with Perceptron Boundary, n=20") +
  geom_vline(xintercept = 0, color="grey") +
  geom_hline(yintercept = 0, color="grey") +
  geom_abline(intercept = (-sample_3c[[2]][3]/sample_3c[[2]][2]), slope = (-sample_3c[[2]][1]/sample_3c[[2]][2]), color="red")

q3c_plot

paste("For this dataset, for convergence to occue with with PLA, we required", sample_3c[1], "updates.")







###################################################################################################
############# Part D:
sample_size <- 100

sample_3d <- two_d_PLA_function(sample_size)

q3d_plot <- ggplot(sample_3d[[3]], aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(sample_3d[[5]]))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(sample_3d[[4]][[3]]/sample_3d[[4]][[2]]), slope = -(sample_3d[[4]][[1]]/sample_3d[[4]][[2]]), color="purple", linetype="dashed", size=1.5) +
  ggtitle("Fig 3.4: Random 2D Classification Boundarty with Perceptron Boundary, n=100") +
  geom_vline(xintercept = 0, color="grey") +
  geom_hline(yintercept = 0, color="grey") +
  geom_abline(intercept = (-sample_3d[[2]][3]/sample_3d[[2]][2]), slope = (-sample_3d[[2]][1]/sample_3d[[2]][2]), color="red")

q3d_plot

paste("For this dataset, for convergence to occue with with PLA, we required", sample_3d[1], "updates.")










###################################################################################################
############# Part E:
sample_size <- 1000

sample_3d <- two_d_PLA_function(sample_size)

q3d_plot <- ggplot(sample_3d[[3]], aes(x=X1, y=X2)) + 
  geom_point(aes(colour = factor(sample_3d[[5]]))) + labs(color = "Y Classification") +
  geom_abline(intercept = -(sample_3d[[4]][[3]]/sample_3d[[4]][[2]]), slope = -(sample_3d[[4]][[1]]/sample_3d[[4]][[2]]), color="purple", linetype="dashed", size=1.5) +
  ggtitle("Fig 3.5: Random 2D Classification Boundarty with Perceptron Boundary, n=1000") +
  geom_vline(xintercept = 0, color="grey") +
  geom_hline(yintercept = 0, color="grey") +
  geom_abline(intercept = (-sample_3d[[2]][3]/sample_3d[[2]][2]), slope = (-sample_3d[[2]][1]/sample_3d[[2]][2]), color="red")

q3d_plot

paste("For this dataset, for convergence to occue with with PLA, we required", sample_3d[1], "updates.")






###################################################################################################
############# Part F:


# Seems best to make a function for this:
ten_d_PLA_function <- function(sample_size){
  
  # Choose f, being a random line in two dimensions. As:
  # Of the form: c1*X1 + c2*X2 + c3*X3 + ... + c10*X10 + c11 = 0
  # or rather: X1 = (-c2/c1)*X2 + (-c3/c1)*X3 + (-c4/c1)*X4 + ... + (-c3/c2)
  
  c1 <- runif(1, -3, 3)
  c2 <- runif(1, -3, 3)
  c3 <- runif(1, -3, 3)
  c4 <- runif(1, -3, 3)
  c5 <- runif(1, -3, 3)
  c6 <- runif(1, -3, 3)
  c7 <- runif(1, -3, 3)
  c8 <- runif(1, -3, 3)
  c9 <- runif(1, -3, 3)
  c10 <- runif(1, -3, 3)
  c11 <- runif(1, -3, 3)

  # record the real line values:
  real_weights <- c(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)
  
  # Create the random dataset
  X1 <- rnorm(sample_size, mean=0, sd=3)
  X2 <- rnorm(sample_size, mean=0, sd=3)
  X3 <- rnorm(sample_size, mean=0, sd=3)
  X4 <- rnorm(sample_size, mean=0, sd=3)
  X5 <- rnorm(sample_size, mean=0, sd=3)
  X6 <- rnorm(sample_size, mean=0, sd=3)
  X7 <- rnorm(sample_size, mean=0, sd=3)
  X8 <- rnorm(sample_size, mean=0, sd=3)
  X9 <- rnorm(sample_size, mean=0, sd=3)
  X10 <- rnorm(sample_size, mean=0, sd=3)

  # Check where to divide for X1:
  dividing_line <- -(c2/c1)*X2 -(c3/c1)*X3 -(c4/c1)*X4 -(c5/c1)*X5 -(c6/c1)*X6 -(c7/c1)*X7 -(c8/c1)*X8 -(c9/c1)*X9 -(c10/c1)*X10 -(c11/c1)
  
  # Use sign for Y if above this:
  Y <- sign(X1 - dividing_line)
  
  
  # Set the dataset:
  Data_set <- tibble(X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, 1, Y)
  
  # Set initial weights
  weights = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
  
  
  # Use the sign to assign initial outcomes:
  h_val <- sign( as.matrix(Data_set %>% select(1:11)) %*% weights )
  
  # record updates done:
  iterations <- 0
  
  # Create a loop to repeatedly update the estimates:
  while (sum(h_val == (Data_set %>% pull(Y))) < sample_size){
    for (i in (1:sample_size)){
      # Primary if clause
      if (h_val[i] != Y[i]){
        weights <- weights + Y[i] *  as.matrix(Data_set %>% select(1:11))[i, ]
        # iterations += 1
        iterations <- iterations + 1
      }
    }
    h_val <- sign( as.matrix(Data_set %>% select(1:11)) %*% weights )
  }
  
  return(list(iterations, weights, Data_set, real_weights, Y, h_val))
}

q3f_sample <- ten_d_PLA_function(1000)

print(q3f_sample[[1]])

print(q3f_sample[[2]])

out_y <- tibble(q3f_sample[[6]])

test_y <- q3f_sample[[3]][12]

full_y <- list(out_y, test_y)


# Seems to work correctly


###################################################################################################
############# Part G:

# Simplify the function output:
# Seems best to make a function for this:
ten_d_PLA_function_simple <- function(sample_size){
  
  # Choose f, being a random line in two dimensions. As:
  # Of the form: c1*X1 + c2*X2 + c3*X3 + ... + c10*X10 + c11 = 0
  # or rather: X1 = (-c2/c1)*X2 + (-c3/c1)*X3 + (-c4/c1)*X4 + ... + (-c3/c2)
  
  c1 <- runif(1, -3, 3)
  c2 <- runif(1, -3, 3)
  c3 <- runif(1, -3, 3)
  c4 <- runif(1, -3, 3)
  c5 <- runif(1, -3, 3)
  c6 <- runif(1, -3, 3)
  c7 <- runif(1, -3, 3)
  c8 <- runif(1, -3, 3)
  c9 <- runif(1, -3, 3)
  c10 <- runif(1, -3, 3)
  c11 <- runif(1, -3, 3)
  
  # record the real line values:
  real_weights <- c(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)
  
  # Create the random dataset
  X1 <- rnorm(sample_size, mean=0, sd=3)
  X2 <- rnorm(sample_size, mean=0, sd=3)
  X3 <- rnorm(sample_size, mean=0, sd=3)
  X4 <- rnorm(sample_size, mean=0, sd=3)
  X5 <- rnorm(sample_size, mean=0, sd=3)
  X6 <- rnorm(sample_size, mean=0, sd=3)
  X7 <- rnorm(sample_size, mean=0, sd=3)
  X8 <- rnorm(sample_size, mean=0, sd=3)
  X9 <- rnorm(sample_size, mean=0, sd=3)
  X10 <- rnorm(sample_size, mean=0, sd=3)
  
  # Check where to divide for X1:
  dividing_line <- -(c2/c1)*X2 -(c3/c1)*X3 -(c4/c1)*X4 -(c5/c1)*X5 -(c6/c1)*X6 -(c7/c1)*X7 -(c8/c1)*X8 -(c9/c1)*X9 -(c10/c1)*X10 -(c11/c1)
  
  # Use sign for Y if above this:
  Y <- sign(X1 - dividing_line)
  
  
  # Set the dataset:
  Data_set <- tibble(X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, 1, Y)
  
  # Set initial weights
  weights = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
  
  
  # Use the sign to assign initial outcomes:
  h_val <- sign( as.matrix(Data_set %>% select(1:11)) %*% weights )
  
  # record updates done:
  iterations <- 0
  
  # Create a loop to repeatedly update the estimates:
  while (sum(h_val == (Data_set %>% pull(Y))) < sample_size){
    for (i in (1:sample_size)){
      # Primary if clause
      if (h_val[i] != Y[i]){
        weights <- weights + Y[i] *  as.matrix(Data_set %>% select(1:11))[i, ]
        # iterations += 1
        iterations <- iterations + 1
      }
    }
    h_val <- sign( as.matrix(Data_set %>% select(1:11)) %*% weights )
  }
  
  return(iterations)
}




# Main loop:

trials <- 100
sample_size <- 1000

updates <- matrix(nrow=trials)

for (i in 1:trials) {
  sample_output <- ten_d_PLA_function_simple(sample_size)
  
  updates[i] <- sample_output
}


# Plot Histogram:
Histogram_plot <- ggplot() + 
  aes(updates) +
  geom_histogram(fill="blue") +
  labs(title=paste("Fig 3.6: Ten Dimensional Perceptron Updates to \nConvergence from", trials, "trials"), 
       x = "Number of Updates until Convergence is achieved",
       y = "Frequency of Trials"
       )
Histogram_plot



###################################################################################################
############# Part H:
































