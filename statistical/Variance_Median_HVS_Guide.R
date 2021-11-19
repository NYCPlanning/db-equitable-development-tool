# Example 6.4 Estimating variance of a mean

hu <- read.csv("../data/HVS_data.csv", header=TRUE)

#Clean data. Eventually may want to do this in python, unsure about that 
weights_correction <- 10^5
rep_weights_cols = c(187:266)
hu[,rep_weights_cols] <- hu[,rep_weights_cols] / weights_correction
hu$fw <- hu$fw / weights_correction
