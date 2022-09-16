# Follow technical documentation for HVS
# Follow examples from documentation in https://www2.census.gov/programs-surveys/nychvs/technical-documentation/variances/2017-NYCHVS-Guide-to-Estimating-Variances.pdf

#Load libraries, set working directory
rm(list=ls())

library(survey)
library(spatstat)
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


#Step one: get data in tabular format. Hopefully our HVS ingestion does this correctly. Find out here

hu <- read.csv("../data/HVS_data.csv", header=TRUE)

#Clean data. Eventually may want to do this in python, unsure about that 
weights_correction <- 10^5
rep_weights_cols = c(187:266)
hu[,rep_weights_cols] <- hu[,rep_weights_cols] / weights_correction
hu$fw <- hu$fw / weights_correction

#
hu$occ_final = ifelse(hu$recid==1, 1, 0)

#UF_CSR is "New control status recode" which says who occupies unit and whether it's stabilizied
hu$rent_bronx = ifelse(( (hu$uf_csr == 30 |hu$uf_csr==31 ) & (hu$boro==1)), 1,0)
hu$rent_manh = ifelse(( (hu$uf_csr == 30 |hu$uf_csr==31 ) & (hu$boro==3)), 1,0)

# Difference? Doesn't make much sense to me to have measure per housing unit. Point is 
# to run 'svrepdesign' in R
hu$stable_diff = hu$rent_manh - hu$rent_bronx


#Proper subdomain for differences
hu$rent_boro = ifelse((
  ((hu$uf_csr == 30 | hu$uf_csr == 31) & (hu$boro == 3)) |
    ((hu$uf_csr == 30 | hu$uf_csr == 31) & (hu$boro == 1))), 1, 0)

#Mean/median example
# Subdomain is renters only with non-missing rent values
# sc here refers to source code, we are looking at item number 9c on 
# page 5 of person occupied units data dictionary
hu$renters = ifelse(
  ((hu$sc116==2 | hu$sc116==3) & hu$uf26 != 99999), 
  1, 0
)

#Gross rent
hu$gross_rent <- hu$uf26
hu$gross_rent[hu$uf26 == 99999] <- NA

#Odds ratio example 
hu$defect = ifelse((hu$rec53 == 4 | hu$rec53 == 5 | hu$rec53 == 6 |
                      hu$rec53 == 7 | hu$rec53 == 8), 1, 0)


# Need binaries for time demarcation:
hu$time_stable <- ifelse(hu$uf_csr == 30, 0, NA)
hu$time_stable[hu$uf_csr == 31] <- 1 

# Adding vacancy dummy:
hu$vac <- ifelse((hu$recid == 3 ), 1, 0)

# Setting survey design parameters
# in our df, variables run from columns 1 to 187 and 268 to 276
# weights run from 188 to 267 

hu$a <-1
hu_design <- svrepdesign(variables= hu[,c(1:186, 267:280)],
                         repweights=hu[,rep_weights_cols],
                         weights=hu$fw, combined.weights = TRUE, type='other',
                         scale=4/80, rscales=1)

occ_hus <- subset(hu_design, occ_final==1)
survey_total = svytotal(~occ_final, design=occ_hus)


whole_city_gb = svyby(~occ_final, ~a, design=hu_design, svytotal)

#By sub-borough area
by_sub_borough_area = svyby(~occ_final, ~boro+cd, design=hu_design, svytotal)

# group by borough instead
by_boro = svyby(~occ_final, ~boro, design=hu_design, svytotal)

# Example 6.2 Estimating variance of a difference
rent_boros <- subset(hu_design, rent_boro == 1)
boro_difference = svytotal(~stable_diff, design = rent_boros)

# Example 6.3
renter_hus <- subset(hu_design, renters == 1)
mean_rent = svymean(~gross_rent, design = renter_hus)

#Do median variance calculation

renter_hus <- subset(hu_design, renters == 1)
median_rent <- svyquantile(~gross_rent, design = renter_hus, 
                        interval.type = "quantile",
                        quantiles=c(.5))
median_rent

#HVS Guide says SE should be 8.794271 
