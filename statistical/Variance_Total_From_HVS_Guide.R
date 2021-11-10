# Follow technical documentation for HVS
# Follow examples from documentation in https://www2.census.gov/programs-surveys/nychvs/technical-documentation/variances/2017-NYCHVS-Guide-to-Estimating-Variances.pdf

#Load libraries, set working directory

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
hu$rent_bronx

hu$rent_manh = ifelse(( (hu$uf_csr == 30 |hu$uf_csr==31 ) & (hu$boro==3)), 1,0)

# Difference? Doesn't make much sense to me to have measure per housing unit. Point is 
# to run 'svrepdesign' in R
hu$stable_diff = hu$rent_manh - hu$rent_bronx


#Proper subdomain for differences
hu$rent_boro = ifelse(
  ((hu$uf_csr ==30 | hu$uf_csv ==31) & (hu$boro ==3 | hu$boro ==1)), 1, 0
)

#Mean/median example
# Subdomain is renters only with non-missing rent values
# sc here refers to source code, we are looking at item number 9c on 
# page 5 of person occupied units data dictionary
hu$renters = ifelse(
  ((hu$sc116==2 | hu$sc116==3) & hu$uf26 != 99999), 
  1, 0
)

#Gross rent

hu$gross_rent = ifelse(
  (hu$uf26 != 99999), 
  hu$uf26, NA
)

# Setting survey design parameters
# in our df, variables run from columns 1 to 187 and 268 to 276
# weights run from 188 to 267 


hu_design <- svrepdesign(variables= hu[,c(1:187, 268:275)],
                         repweights=hu[,rep_weights_cols],
                         weights=hu$fw, combined.weights = TRUE, type='other',
                         scale=4/80, rscales=1)

occ_hus <- subset(hu_design, occ_final==1)
survey_total = svytotal(~occ_final, design=occ_hus)

#By sub-borough area
by_sub_borough_area = svyby(~occ_final, ~boro+cd, design=hu_design, svytotal)

# group by borough instead
by_boro = svyby(~occ_final, ~boro, design=hu_design, svytotal)




