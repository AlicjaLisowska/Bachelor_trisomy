#!/usr/bin/env python3
"""
Autor: Alicja Lisowska
Data: 2024-11-30
"""

# Importowanie niezbędnych bibliotek
import sys
import os

# Funkcje pomocnicze
def pobieranie_z_pliku(param1):
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



def standard_dev(col3):
    if not col3:
        raise ValueError("Lista danych nie może być pusta.")
    
        # Oblicz średnią
    
    srednia = sum(col3) / len(col3)
    
    # Oblicz wariancję (średnia kwadratów odchyleń od średniej)
    wariancja = sum((x - srednia) ** 2 for x in col3) / len(col3)
    
    # Odchylenie standardowe to pierwiastek z wariancji
    odchylenie_standardowe = round (wariancja ** 0.5,5)
    
    return odchylenie_standardowe

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
    decision = 0
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
    
    
    

def output_file_alg1(data,filename,standardd,decision):
    counter = 0
    file = filename
    description = ["Numer chromosomu: ", "Dlugosc chromosomu referyncyjneg: ", "Dopasowane: ", "Stopien pokrycia [%]: ", "Decyzja: "]
    for row in data:
        row.append(decision[counter])
        counter = counter + 1

    
    with open("/home/vboxuser/Desktop/Licencjat/output/output_" + str(file) + ".csv", "w") as plik:
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



def alg1(data,filename):

    column_3 = []
    column_1 = []
    for row in data:
        coverage= round(float(row[2])/float(row[1])*100,3)
        #print("Pokrycie:"+ str(coverage))
        #row[3]=coverage
        row.insert(3,coverage)
        row.pop(4)
        print(row)
        column_3.append(row[3])
        column_1.append(row[0])
        
    #print(column_3)    
    srednia = average(column_3)
    print("Srednia arytmetyczna: " + str(srednia))
    standardd= standard_dev(column_3)
    print("Odchylenie standardowe: "+ str(standardd))
    output_file_alg1(data,filename, standardd, is_within_range(column_1, column_3, srednia, standardd, data))
    
    

    
# Główna funkcja programu
def main(): 
    """
    Główna funkcja programu, która obsługuje logikę działania skryptu.
    """
    # Sprawdzenie, czy skrypt jest uruchamiany jako główny
    for f in sys.argv[1:]:
        print(f"Przetwarzam plik: {f}")
        if len(f) > 1:
            file = pobieranie_z_pliku(f)
            alg1(file,f)
 
        else:
            print("Brak podanych argumentów.")



# Sprawdzenie, czy skrypt jest uruchamiany jako główny program
if __name__ == "__main__":
    main()