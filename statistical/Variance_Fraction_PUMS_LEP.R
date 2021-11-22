# Calculate variance of a fraction. Use lep_2019 as example
rm(list=ls())
library(survey)
library(spatstat)
library(dplyr)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


#Step one: get data in tabular format. Hopefully our HVS ingestion does this correctly. Find out here

PUMS <- read.csv("../data/PUMS_demographics_2019.csv", header=TRUE)

PUMS$LEP = ifelse((PUMS$LANX=='Yes, speaks another language')& (PUMS$AGEP>5)& (PUMS$ENG!='Very well'), TRUE, FALSE)

LEP_gb = PUMS %>% group_by(PUMA) %>% summarize(total=n(), LEP = sum(LEP))
                  