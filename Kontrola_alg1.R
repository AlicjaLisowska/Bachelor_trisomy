# Dane
x <- c(86, 26)
y <- c("Obecna trisomia", "Brak trisomii")

# Kolory w formacie hex (RGB w hex)
color1 <- "#9B56B6"  # Kolor czerwony w formacie hex
color2 <- "#34495E"  # Kolor niebieski w formacie hex

# Tworzenie wykresu słupkowego
barplot_heights <- barplot(x, 
                           names.arg = y,  # Etykiety dla każdego słupka
                           main = "Liczba przypadków trisomii",  # Tytuł wykresu
                           col = c(color1, color2),  # Użycie kolorów hex
                           border = "white",  # Brak obramowania słupków
                           xlab = "Stan",  # Etykieta osi X
                           ylab = "Liczba przypadków",  # Etykieta osi Y
                           cex.main = 1.8,  # Powiększony tytuł wykresu
                           cex.lab = 1.2,  # Powiększenie etykiet osi
                           cex.axis = 1.1,  # Powiększenie etykiet osi
                           font.lab = 2,  # Grubsza czcionka etykiet
                           ylim = c(0, max(x) + 20),  # Wydłużenie zakresu Y, by dało się dodać liczby
                           axes = FALSE)  # Brak domyślnych osi

# Dodanie osi X i Y ręcznie z siatką
#axis(1, at = barplot_heights, labels = y, cex.axis = 1.2, font.axis = 2, col = "black")  # Oś X
axis(2, cex.axis = 1.2, font.axis = 2, col = "black")  # Oś Y
#grid(col = "gray", lty = "dotted")  # Dodanie siatki w tle

# Dodanie liczb na środku słupków
text(x = barplot_heights,  # Współrzędne X słupków
     y = x / 2,  # Ustawienie Y na połowie wysokości słupka (czyli w środku)
     labels = x,  # Wartości liczbowe
     cex = 1.5,  # Wielkość czcionki
     col = "black",  # Kolor tekstu
     font = 2)  # Pogrubiona czcionka
