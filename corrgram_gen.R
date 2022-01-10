library(corrgram)
library(tidyverse)


train_dat = read.csv('caffeine_cleaned.csv')


# png(filename="figures/corrgram.png")

corrgram(train_dat, order=TRUE, lower.panel=panel.shade,
         upper.panel=panel.pie, text.panel=panel.txt,
         main="Heart Disease Data Corrgram")

