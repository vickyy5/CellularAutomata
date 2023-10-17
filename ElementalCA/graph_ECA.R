library(tidyverse)
library(readr)

densy <- read_csv("data/density.csv", col_types = cols(...1 = col_integer(), 
                                                         Density = col_integer()))

n <- nrow(densy)

densy <- densy %>% 
  mutate( l10 = log10(Density)) %>% 
  mutate( ent = -( (Density/n)*log2(Density/n) ) )


densplot <- ggplot(densy, aes(x= ...1, y= Density, color=Density)) +
  geom_point() +
  labs(x="N Evolution") +
  geom_smooth() 

ggsave('./img/density.png')

log10plot <- ggplot(densy, aes(x= ...1, y= l10, color = Density)) +
  geom_point() +
  labs(x="N Evolution", y="Density Log10") +
  geom_smooth() 

ggsave('./img/log10.png')

entplot <- ggplot(densy, aes(x= ...1, y= ent, color = ent)) +
  geom_point() +
  labs(x="N Evolution", y="Entropy") +
  geom_smooth() 

ggsave('./img/entropy.png')

denvsent <- ggplot(densy, aes(x= Density, y= ent)) +
  geom_point(color="red") +
  labs(x="Density", y="Entropy")

ggsave('./img/density_vs_entropy.png')

