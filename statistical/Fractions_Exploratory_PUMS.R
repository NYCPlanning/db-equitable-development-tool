reset(list=ls())
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(survey)
library(base)
PUMS = read.csv('../data/PUMS_demographics_2019.csv')

PUMS['wnh'] <- ifelse(PUMS['RAC1P'] == 'White alone' & PUMS['HISP'] =='Not Spanish/Hispanic/Latino', 1, 0)

rw = vector()
for (i in c(1:80)){
  print(i)
  rw = append(rw, paste('PWGTP', as.character(i), sep=""))
}
weight_col = 'PWGTP'
geo_col = 'PUMA'
total_pop = sum(PUMS['PWGTP'])
PUMS_design <- svrepdesign(variables= PUMS[c('RAC1P', 'a')],
                         repweights=PUMS[rw],
                         weights=PUMS$PWGTP, combined.weights = TRUE, type='other',
                         scale=4/80, rscales=1)

aggregated <- svyby(
  formula=PUMS["wnh"],
  by=PUMS[geo_col],
  design=PUMS_design,
  FUN=svymean,
)

aggregated_ciprop <- svyby(
  formula=PUMS["wnh"]==1,
  by=PUMS[geo_col],
  design=PUMS_design,
  FUN=svyciprop,
)
svytotal(~interaction(RAC1P/total_pop), PUMS_design)


