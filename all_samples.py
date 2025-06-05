# Importowanie niezbędnych bibliotek standardowych
import sys
import os
import math
import statistics

# Lista przechowująca dane z plików genomowych
genomes_list = []
counter = 0

# Słownik z kluczami chr_1 do chr_22; każdy klucz zawiera pustą listę do przechowywania danych
chromosomes = {f'chr_{i}': [] for i in range(1, 23)}

# Funkcja wczytująca dane z pliku, tworzy listę pokryć chromosomów autosomalnych (1–22)
def create_tables(file):
    try:
        lists = []
        filepath = "/home/vboxuser/Desktop/Licencjat/3x21_idxstats/" + file
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Pominięcie pustych linii
                    columns = line.strip().split('\t')  # Podział wiersza na kolumny
                    if columns[0].isdigit():  # Filtracja tylko autosomalnych chromosomów (1–22)
                        lists.append(columns[2])  # Pobieranie wartości z 3. kolumny (pokrycie)
                    else:
                        break  # Przerywamy, jeśli trafimy na inny typ chromosomu (np. X, Y)
        return genomes_list.append(lists)
    except FileNotFoundError:
        print(f"Plik {filepath} nie istnieje.")
    except ValueError:
        print("Podano niepoprawne dane wejściowe.")

# Funkcja przypisująca wartości pokrycia do odpowiadających chromosomów w słowniku `chromosomes`
def chromosomes_sort(genomes_list):
    for lists in genomes_list:  # Iteracja po listach genomów
        for i in range(1, 23):
            chromosomes[f'chr_{i}'].append(int(lists[i - 1]))  # Dodanie wartości pokrycia do odpowiedniego chromosomu

# Funkcja obliczająca średnią i odchylenie standardowe dla każdego chromosomu
def chr_SD_mean():
    for i in range(1, 23):
        if chromosomes[f'chr_{i}']:  # Upewniamy się, że lista nie jest pusta
            sd_value = statistics.stdev(chromosomes[f'chr_{i}'])  # Obliczenie odchylenia standardowego
            mean_value = statistics.mean(chromosomes[f'chr_{i}'])  # Obliczenie średniej
            chromosomes[f'chr_{i}'].append(round(mean_value, 0))  # Dodanie zaokrąglonej średniej
            chromosomes[f'chr_{i}'].append(sd_value)  # Dodanie odchylenia standardowego

# Funkcja analizująca, czy dane pokrycie chromosomu odbiega od normy (aberracja)
def decision(file, k=1):
    data = open_file(file)  # Wczytanie danych z pliku
    for key, value in chromosomes.items():
        print(key, ":", value)  # Wyświetlenie zawartości chromosomów (debug)

    for d in data:
        decision = 0
        chrom = f'chr_{int(d[0])}'  # Identyfikator chromosomu (np. chr_21)
        sd = float(chromosomes[chrom][-1])  # Odchylenie standardowe z końca listy
        mean = float(chromosomes[chrom][-2])  # Średnia z przedostatniego elementu listy
        lower_bound = mean - k * sd  # Dolna granica
        upper_bound = mean + k * sd  # Górna granica

        print("CHROM:", chrom)
        print("SD:", sd)
        print("MEAN:", mean)
        print("Lower:", lower_bound, "Upper:", upper_bound)

        with open("/home/vboxuser/Desktop/Licencjat/alg_4_endfile.txt", "a") as plik_end:
            coverage = float(d[2])  # Rzeczywiste pokrycie dla danego chromosomu
            if lower_bound <= coverage <= upper_bound:
                print(f"Chromosom {chrom} nie wykazuje aberracji")
            elif coverage > upper_bound:
                print(f"Chromosom {chrom} wskazuje na możliwą aberrację (pokrycie powyżej normy)")
                if int(d[0]) == 21:  # Dodatkowy warunek dla trisomii 21
                    plik_end.write(f"{file}\n")
            elif coverage < lower_bound:
                print(f"Chromosom {chrom} poniżej dolnego progu odchylenia")

# Funkcja wczytująca pełne dane z pliku — wersja używana w `decision()`
def open_file(file):
    filepath = "/home/vboxuser/Desktop/Licencjat/3x21_idxstats/" + file
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():  # Pominięcie pustych linii
                columns = line.strip().split('\t')
                if columns[0] == "X":  # Przerwanie przy chromosomie X (analizujemy tylko autosomalne)
                    break
                data.append(columns)
    return data
