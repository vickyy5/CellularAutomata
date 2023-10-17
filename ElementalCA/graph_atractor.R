library(tidygraph)
library(tidyverse)
library(readr)
library(ggraph)
attr <- read_csv("data/attr.csv", col_types = cols(State = col_integer(), 
                                                   `Go to` = col_integer()))

gr <- as_tbl_graph(attr)

gr1 <- ggraph(gr) +
  geom_edge_link() +
  geom_node_point(shape=20,colour='blue')

ggsave('./img/attractor.png')