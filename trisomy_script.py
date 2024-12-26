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

    # Wyświetl dane (opcjonalne)
        #print("Wczytane dane:")
        #for row in data:
            #print(row)

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


def alg1(data):
    column_3=[]
    for row in data:
        coverage= round(float(row[2])/float(row[1])*100,3)
        #print("Pokrycie:"+ str(coverage))
        #row[3]=coverage
        row.insert(3,coverage)
        row.pop(4)
        print(row)
        column_3.append(row[3])
    #print(column_3)    
    standardd= standard_dev(column_3)
    print("Odchylenie standardowe: "+ str(standardd))
    

    
# Główna funkcja programu
def main(): 
    """
    Główna funkcja programu, która obsługuje logikę działania skryptu.
    """
    # Sprawdzenie, czy skrypt jest uruchamiany jako główny
    if len(sys.argv) > 1:
        file = pobieranie_z_pliku(sys.argv[1])
        alg1(file)
 
    else:
        print("Brak podanych argumentów.")



# Sprawdzenie, czy skrypt jest uruchamiany jako główny program
if __name__ == "__main__":
    main()