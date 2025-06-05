# Instalacja (jeśli trzeba)
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("patchwork")) install.packages("patchwork")
if (!require("readr")) install.packages("readr")
if (!require("scales")) install.packages("scales")

# Biblioteki
library(ggplot2)
library(patchwork)
library(readr)
library(scales)


# Import danych
dane <- read_delim("~/Desktop/Licencjat/output_1/srednie.txt", delim = "\n", col_names = FALSE)
colnames(dane) <- c("Srednie_pokrycie")
# Wykres punktowy
plot_punkty <- ggplot(dane, aes(x = Srednie_pokrycie, y = 0)) +
  geom_jitter(width = 0, height = 0.2, color = "#1f77b4", alpha = 0.6) +
  scale_x_continuous(labels = label_percent(scale = 1), breaks = seq(0, max(dane$Srednie_pokrycie), by = 1)) +
  labs(
    title = "Rozkład punktowy średniego pokrycia",
    x = "Średnie pokrycie (%)",
    y = NULL
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text.y = element_blank(),  # usuń etykiety y
    axis.ticks.y = element_blank()  # usuń kreski y
  )

# Boxplot
plot_box <- ggplot(dane, aes(x = "", y = Srednie_pokrycie)) +
  geom_boxplot(
    fill = "#1f77b4", alpha = 0.5,
    outlier.colour = "#F8766D", outlier.size = 2
  ) +
  scale_y_continuous(labels = label_percent(scale = 1), breaks = seq(0, max(dane$Srednie_pokrycie), by = 1)) +
  labs(
    title = "Rozkład średniego pokrycia (boxplot)",
    y = "Średnie pokrycie (%)",
    x = ""
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold")
  )

# Połączenie
plot_punkty 
plot_box 
plot_layout(ncol = 2)
