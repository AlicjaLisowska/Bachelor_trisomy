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
                data.append(columns)  # Przechowujemy dane w liście

    # Wyświetl dane (opcjonalne)
        print("Wczytane dane:")
        for row in data:
            print(row)

    # Wyciąganie konkretnej komórki
        row_index = int(input("Podaj numer wiersza (indeksowanie od 0): "))
        col_index = int(input("Podaj numer kolumny (indeksowanie od 0): "))

    # Sprawdzamy, czy indeksy są w zakresie
        if 0 <= row_index < len(data) and 0 <= col_index < len(data[row_index]):
            print(f"Wartość w komórce ({row_index}, {col_index}): {data[row_index][col_index]}")
            return data
        else:
            print("Błąd: Podane indeksy są poza zakresem.")
    except FileNotFoundError:
        print(f"Plik {filepath} nie istnieje.")
    except ValueError:
        print("Podano niepoprawne dane wejściowe.")





def obliczanie_trisomia(data):
    print("test_nowafunkjca")
    #for row in data:
     #   print(row)
    i =0
    for row in data[0:]:
        i=i+int(row[1])
        print(row[1])
            #print("I:"+i)
    print(i)

    



    
# Główna funkcja programu
def main():
    """
    Główna funkcja programu, która obsługuje logikę działania skryptu.
    """
    # Sprawdzenie, czy skrypt jest uruchamiany jako główny
    if len(sys.argv) > 1:
        file = pobieranie_z_pliku(sys.argv[1])
        obliczanie_trisomia(file)
       # print(f"Podano argumenty: {file}"
 
    else:
        print("Brak podanych argumentów.")



# Sprawdzenie, czy skrypt jest uruchamiany jako główny program
if __name__ == "__main__":
    main()

