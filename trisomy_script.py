#!/usr/bin/env python3
"""
Autor: Alicja Lisowska
Data: 2024-11-30
"""

# Importowanie niezbędnych bibliotek
import sys
import os

# Funkcje pomocnicze

# Wyciagniecie danych z plikow
def open_file(param1):
    filepath = "/home/vboxuser/Desktop/Licencjat/3x21_idxstats/" + param1
    try:
        data = []
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
               # Pomijamy puste linie
             if line.strip():
                # Rozdzielamy linie na kolumny
                columns = line.strip().split('\t')  # Dostosuj separator ('\t' dla tabulatora, ',' dla przecinka)
                # pobranie jedynie chromosomow autosomalnych
                if columns[0] == "X":
                    break
                data.append(columns)  # Przechowujemy dane w liście
        return data

    except FileNotFoundError:
        print(f"Plik {filepath} nie istnieje.")
    except ValueError:
        print("Podano niepoprawne dane wejściowe.")


#Obliczanie odchylenia standardowego
def standard_dev(col3):
    if not col3:
        raise ValueError("Lista danych nie może być pusta.")
    
    # Oblicz średnią
    srednia = sum(col3) / len(col3)
    
    # Oblicz wariancję
    wariancja = sum((x - srednia) ** 2 for x in col3) / len(col3)
    
    # Odchylenie standardowe
    odchylenie_standardowe = round (wariancja ** 0.5,5)
    
    return odchylenie_standardowe


#Obliczenie Sredniej
def average(col3):
    if not col3:
        raise ValueError("Lista danych nie może być pusta.")
    
    # Oblicz średnią
    srednia = sum(col3) / len(col3)
    return round(srednia,5)


def is_within_range(chrom_value,value, mean, std_dev, data, k=1):
    """
    Sprawdza, czy dana liczba mieści się w zakresie zdefiniowanym
    przez podaną średnią i odchylenie standardowe.

    :param chrom_value: Numer chromosomu.
    :param value: Liczba do sprawdzenia.
    :param mean: Średnia arytmetyczna.
    :param std_dev: Odchylenie standardowe.
    :param k: Współczynnik mnożnika odchylenia standardowego (domyślnie 1).
    :return: True, jeśli liczba mieści się w zakresie, False w przeciwnym razie.
    """
    # Oblicz granice zakresu
    lower_bound = mean - k * std_dev
    upper_bound = mean + k * std_dev
    
    
    counter = 0
    decision = 0 #Decyzja czy wykazuje pokrycie nizsze/wyzsze od zalozonego
    col_4 = [] 
    for i in value:
        if i >= lower_bound and i <= upper_bound:
            print("Chromosom " + str(chrom_value[counter]) + " nie wykazuje aberracji")
            decision = 0
            col_4.insert(counter,decision)
            counter = counter + 1   
            
        if i > upper_bound:
            print("Chromosom " + str(chrom_value[counter]) + " wskazuje na mozliwa aberracje")
            decision = 1
            col_4.insert(counter,decision)
            counter = counter + 1
            
        if i < lower_bound:
            print("Chromosom " + str(chrom_value[counter]) + " ponizej dolnego progu odchylenia")
            decision = -1
            col_4.insert(counter,decision)
            counter = counter + 1
            
    print("dane:" + str(col_4))
    return col_4
    
    
#Generowanie pliku koncowego    
def output_file_alg1(data,filename,standardd,decision):
    counter = 0
    file = filename[:-4]
    description = ["Numer chromosomu: ", "Dlugosc chromosomu referyncyjneg: ", "Liczba odczytow: ", "Srednie pokrycie [%]: ", "Decyzja: "]
    for row in data:
        row.append(decision[counter])
        counter = counter + 1

    
    with open("/home/vboxuser/Desktop/Licencjat/output_1/output_" + str(file) + ".csv", "w") as plik:
        for item in description:
            plik.write(str(item)+"\t")
        
        plik.write("\n")
        for row in data:
            plik.write(str(row[0]) + "\t")
            plik.write(str(row[1]) + "\t")
            plik.write(str(row[2]) + "\t")
            plik.write(str(row[3]) + "\t")
            plik.write(str(row[4]) + "\n")
            
        plik.write("Odchylenie standardowe dla osobnika: " + str(standardd) + "\n")
    print("Plik zostal zapisany")


# Algorytm wywolujacy pozostale funkcje
def alg1(data,filename):
    """
    Zmienna column_*  przechowuja dane potrzebne do pozniejszego oznaczenia czy pokrycie danego chromosomu znajduje sie w zakresie
    """
    column_3 = [] 
    column_1 = []
    for row in data:
        coverage= round(float(row[2])/float(row[1])*100,3) # Srednie pokrycie
        row.insert(3,coverage) # Dodanie pokrycia do odpowiedniego wiersza z danymi
        row.pop(4)
        print(row)
        column_3.append(row[3]) 
        column_1.append(row[0])
        
    srednia = average(column_3)
    print("Srednia arytmetyczna: " + str(srednia))
    standardd= standard_dev(column_3)
    print("Odchylenie standardowe: "+ str(standardd)) #Kontrolne wypisane wyniku w konsoli
    output_file_alg1(data,filename, standardd, is_within_range(column_1, column_3, srednia, standardd, data)) # Wywolanie zapisu wyniku do pliku
    
    
    
# Główna funkcja programu
def main(): 
    """
    Główna funkcja programu, która obsługuje logikę działania skryptu.
    """
    # Uruchomienie algorytmu nr.1
    for f in sys.argv[1:]:
        print(f"Przetwarzam plik: {f}")
        if len(f) > 1:
            file = open_file(f)
            alg1(file,f)
 
        else:
            print("Brak podanych argumentów.")



# Sprawdzenie, czy skrypt jest uruchamiany jako główny program
if __name__ == "__main__":
    main()