# 00-utils.R - Utility functions and CUD colors
# Load this first in all other scripts

library(jsonlite)

# Load config
load_config <- function(path = "config/parameters.json") {
  fromJSON(path)
}

# CUD Color Palette (Okabe-Ito)
CUD_COLORS <- c(
  black = "#000000",
  orange = "#E69F00",
  skyblue = "#56B4E9",
  bluishgreen = "#009E73",
  yellow = "#F0E442",
  blue = "#0072B2",
  vermilion = "#D55E00",
  reddishpurple = "#CC79A7"
)

# Get CUD color by name
cud <- function(name) {
  CUD_COLORS[name]
}

# Save JSON helper
save_json <- function(data, path) {
  write_json(data, path, pretty = TRUE, auto_unbox = TRUE)
  message(paste("Saved:", path))
}

# Load JSON helper
load_json <- function(path) {
  fromJSON(path)
}
