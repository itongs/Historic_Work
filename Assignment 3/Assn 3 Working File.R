###################################################################################################


# Assignment Three for ETC3555, S2 2020


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
library(keras)


######################          Convert into RMD Before submission          #######################



# NB: re-run all of the model when retraining - refresh the R session!




###################################################################################################
# Question One:
###################################################################################################

# Stuff from the Lab:
# Import dataset:
library(keras)
mnist <- dataset_mnist()
x_train <- mnist$train$x
y_train <- mnist$train$y
x_test <- mnist$test$x
y_test <- mnist$test$y


## Re-arrange dataset:
# reshape
x_train <- array_reshape(x_train, c(nrow(x_train), 784))
x_test <- array_reshape(x_test, c(nrow(x_test), 784))
# rescale
x_train <- x_train / 255
x_test <- x_test / 255

# Categorise output data:
y_train <- to_categorical(y_train, 10)
y_test <- to_categorical(y_test, 10)




## Define the model:
model <- keras_model_sequential() 
model %>% 
  layer_dense(units = 256, activation = 'relu', input_shape = c(784)) %>% 
  layer_dropout(rate = 0.4) %>% 
  layer_dense(units = 128, activation = 'relu') %>%
  layer_dropout(rate = 0.3) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model)

# Compile the model with an appropriate Loss Function and Optimizer:
model %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)




## Training and Fitting the model:
history <- model %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history)

# Evaluate the model's performance:
model %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model %>% predict_classes(x_test)






#--------------------------------------------------------------------------------------------------
# Q1 Part A:
#--------------------------------------------------------------------------------------------------


mnist <- dataset_mnist()
x_train <- mnist$train$x
y_train <- mnist$train$y
x_test <- mnist$test$x
y_test <- mnist$test$y

## Re-arrange dataset:
# reshape
x_train_1a <- array_reshape(x_train, c(nrow(x_train), 784))
x_test_1a <- array_reshape(x_test, c(nrow(x_test), 784))
# rescale
x_train_1a <- x_train / 255
x_test_1a <- x_test / 255

# Categorise output data:
y_train_1a <- to_categorical(y_train, 10)
y_test_1a <- to_categorical(y_test, 10)




## Define the model:
model_1a <- keras_model_sequential() 
model_1a %>% 
  layer_dense(units = 256, activation = 'relu', input_shape = c(784)) %>% 
  layer_dropout(rate = 0.4) %>% 
  layer_dense(units = 64, activation = 'relu') %>%
  layer_dropout(rate = 0.3) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_1a)

# Compile the model with an appropriate Loss Function and Optimizer:
model_1a %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)




## Training and Fitting the model:
history_1a <- model_1a %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history_1a)

# Evaluate the model's performance:
model_1a %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_1a %>% predict_classes(x_test)







#--------------------------------------------------------------------------------------------------
# Q1 Part B:
#--------------------------------------------------------------------------------------------------




## Define the model:
model_1b <- keras_model_sequential() 
model_1b %>% 
  layer_dense(units = 256, activation = 'relu', input_shape = c(784)) %>% 
  layer_activity_regularization(l1 = 0.01) %>%
  layer_dense(units = 128, activation = 'relu') %>%
  layer_activity_regularization(l1 = 0.01) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_1b)

# Compile the model with an appropriate Loss Function and Optimizer:
model_1b %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)




## Training and Fitting the model:
history_1b <- model_1b %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history_1b)

# Evaluate the model's performance:
model_1b %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_1b %>% predict_classes(x_test)






#--------------------------------------------------------------------------------------------------
# Q1 Part C:
#--------------------------------------------------------------------------------------------------

## Define the model:
model_1c <- keras_model_sequential() 
model_1c %>% 
  layer_dense(units = 256, activation = 'relu', input_shape = c(784)) %>% 
  layer_dense(units = 128, activation = 'relu') %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_1c)

# Compile the model with an appropriate Loss Function and Optimizer:
model_1c %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)




## Training and Fitting the model:
history_1c <- model_1c %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2,
  # Early stopping clause:
  callbacks = list(callback_early_stopping(monitor = "val_loss"))
)

# Plot the loss and accuracy:
plot(history_1c)

# Evaluate the model's performance:
model_1c %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_1c %>% predict_classes(x_test)













###################################################################################################
# Question Two:
###################################################################################################

# Need to use 'grid search' to find the optimal connections
# Link for the documentation:
# https://github.com/tidymodels/rsample/blob/8333b7bb441e0097418205dd735bd3f0cc418916/vignettes/Applications/Keras.Rmd


# Define d:
d <- c(16,32,64,128)

# Define q:
q <- c(0,0.25,0.5,0.75)


# Create output data frame:
All_Tested_Models <- data.frame("d" = NA, "q" = NA, "Loss" = NA, "Accuracy" = NA)


# Outer Loop for q values for the dropout rate
for (i in 1:length(q)){
  
  # Inner Loop for values of d for the hidden layer size
  for (j in 1:length(d)){
    
    # Start Model:
    tested_model <- keras_model_sequential()
    
    # Define Model:
    tested_model %>%
      layer_dense(units = d[j], activation = 'relu', input_shape = c(784)) %>%
      layer_dropout(rate = q[i]) %>%
      layer_dense(units = 10, activation = 'softmax')
    
    # Compile Model
    tested_model %>% compile(
      loss = 'categorical_crossentropy',
      optimizer = optimizer_rmsprop(),
      metrics = c('accuracy')
    )
    
    # Analyse History of the Model:
    tested_history <- tested_model %>% fit(
      x_train, y_train,
      epochs = 30, batch_size = 128,
      validation_split = 0.2
    )
    
    # Evaluate model:
    tested_result <- tested_model %>% evaluate(x_test, y_test)
    
    # Add models to the main list of models
    tested_model <- c(d[j], q[i], tested_result[[1]], tested_result[[2]])
    All_Tested_Models <- rbind(All_Tested_Models, tested_model)
  }
}

# Remove top row of NAs
All_Tested_Models <- All_Tested_Models[-c(1),]
# Renumber:
row.names(All_Tested_Models) <- 1:nrow(All_Tested_Models)


print(All_Tested_Models)


# Transform the data appropriately
All_Tested_Models$q_value <- as.factor(All_Tested_Models[,'q'])
All_Tested_Models$d_value <- as.factor(All_Tested_Models[,'d'])



# Heatmap Code
library(hrbrthemes)
library(viridis)
Loss.Heatmap <- ggplot(data = All_Tested_Models, 
                       mapping = aes(x = q_value,
                                     y = d_value,
                                     fill = Loss)) +
  geom_tile() +
  geom_text(aes(label = 
                  paste("Loss: \n", 
                        round(Loss, 4), 
                        "\nAccuracy:\n", 
                        round(All_Tested_Models$Accuracy, 4))), 
            color = "white") +
  scale_fill_gradient(low = "palegreen3", high = "orange", trans = 'log' ) +
  ggtitle("Heatmap of Hyperparameter Combinations",
          subtitle = "Low Loss is Green, High Loss is Orange") +
  ylab(label = "Hidden Layer Size (d)") + 
  xlab(label = "Dropout Rate (q)")

Loss.Heatmap













###################################################################################################
# Question Three:
###################################################################################################

# Easy but confusement - add a new line


# Random link, may not be associated:
# https://github.com/natanielruiz/deep-head-pose






#-----------------------------------------------------------------------------------------------
# Momentum:
#-----------------------------------------------------------------------------------------------


## Define the model:
model_3M <- keras_model_sequential() 
model_3M %>% 
  layer_dense(units = 128, activation = 'relu', input_shape = c(784)) %>%
  layer_dropout(rate = 0.25) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_3M)

# Compile the model with an appropriate Loss Function and Optimizer:
model_3M %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_sgd(momentum=0.9),
  metrics = c('accuracy')
)



## Training and Fitting the model:
history_3M <- model_3M %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history_3M)

# Evaluate the model's performance:
model_3M %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_3M %>% predict_classes(x_test)




#-----------------------------------------------------------------------------------------------
# ADAM:
#-----------------------------------------------------------------------------------------------


## Define the model:
model_3Ad <- keras_model_sequential() 
model_3Ad %>% 
  layer_dense(units = 128, activation = 'relu', input_shape = c(784)) %>%
  layer_dropout(rate = 0.25) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_3Ad)

# Compile the model with an appropriate Loss Function and Optimizer:
model_3Ad %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_adam(),
  metrics = c('accuracy')
)



## Training and Fitting the model:
history_3Ad <- model_3Ad %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history_3Ad)

# Evaluate the model's performance:
model_3Ad %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_3Ad %>% predict_classes(x_test)








#-----------------------------------------------------------------------------------------------
# RMSProp:
#-----------------------------------------------------------------------------------------------


## Define the model:
model_3RMS <- keras_model_sequential() 
model_3RMS %>% 
  layer_dense(units = 128, activation = 'relu', input_shape = c(784)) %>%
  layer_dropout(rate = 0.25) %>%
  layer_dense(units = 10, activation = 'softmax')

# Inspect the defined model:
summary(model_3RMS)

# Compile the model with an appropriate Loss Function and Optimizer:
model_3RMS %>% compile(
  loss = 'categorical_crossentropy',
  optimizer = optimizer_rmsprop(),
  metrics = c('accuracy')
)



## Training and Fitting the model:
history_3RMS <- model_3RMS %>% fit(
  x_train, y_train, 
  epochs = 30, batch_size = 128, 
  validation_split = 0.2
)

# Plot the loss and accuracy:
plot(history_3RMS)

# Evaluate the model's performance:
model_3RMS %>% evaluate(x_test, y_test)


# Generate predictions on the new data:
model_3RMS %>% predict_classes(x_test)































df_1c_hist



tl <- ggplot(aes(x = index, y = loss), data = df_1c_hist) +  
  geom_point(color = "red") + geom_line(color = "red", linetype="dotted")
vl <- ggplot(aes(x = index, y = val_loss), data = df_1c_hist) +  
  geom_point(color = "red") + geom_line(color = "red")
ta <- ggplot(aes(x = index, y = accuracy), data = df_1c_hist) +  
  geom_point(color = "red") + geom_line(color = "red", linetype="dotted")
va <- ggplot(aes(x = index, y = val_accuracy), data = df_1c_hist) +  
  geom_point(color = "red") + geom_line(color = "red")


































