reset(list=ls())
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(survey)
library(base)
PUMS = read.csv('../data/PUMS_demographics_2019.csv')

PUMS['a'] <-1
rw = vector()
for (i in c(1:80)){
  print(i)
  rw = append(rw, paste('PWGTP', as.character(i), sep=""))
}
weight_col = 'PWGTP'
geo_col = 'PUMA'
total_pop = sum(PUMS['PWGTP'])
PUMS_design <- svrepdesign(variables= PUMS$a,
                           repweights=PUMS[rw],
                           weights=PUMS$PWGTP, combined.weights = TRUE, type='other',
                           scale=4/80, rscales=1)
survey <- svyby(formula=PUMS$a, by=PUMS[, c('PUMA','ENG')], design = PUMS_design, FUN=svytotal)
cv(survey)
