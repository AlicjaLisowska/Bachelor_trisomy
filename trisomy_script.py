#!/usr/bin/env python3

"""
Autor: Alicja Lisowska
Data: 2024-11-30
"""


# Importowanie niezbędnych bibliotek
import sys
import os
import math

# import skryptow
import all_samples
#import R_X

#Atrybuty globalne:    
range_tab_1 = []
range_tab_2 = []
range_tab_3 = []
range_tab_4 = []

# Funkcje pomocnicze
def table_range_write():
    file = "capture_range"
    description = ["Capture"+ "\n"+
                   "Range 1."+"\t"+
                   "Range 2."+"\t"+
                   "Range 3."+"\t"+
                   "Range 4."+"\n"]
    with open("/home/vboxuser/Desktop/Licencjat/3x21_idxstats"+ str(file) + ".csv", "w") as plik:
        for item in description:
            plik.write(str(item))
    
        # Umieszczamy wszystkie listy w jednej liście
        tabele = [range_tab_1, range_tab_2, range_tab_3, range_tab_4]


         # Znajdujemy długość najdłuższej tablicy
        max_len = max(len(tab) for tab in tabele)
        # Iterujemy po indeksach (wierszach)
        for idx in range(max_len):
            # Dla każdej kolumny (listy)
            for tab in tabele:
                if idx < len(tab):
                    plik.write(str(tab[idx]))
                else:
                    plik.write("")  # jeśli lista krótsza, zostaw puste
                plik.write("\t")  # tabulator po każdej kolumnie
            plik.write("\n")  # nowa linia po każdym wierszu


# Wyciagniecie danych z plikow
def open_file(param1):
    filepath = "/home/vboxuser/Desktop/Licencjat/3x21_idxstats/" + param1
    #zapytanie o rodzaj algorytmu i zapisanie do zmiennej alg_number
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
        print("Podano niepoprawne dane wejściowe.")    #return data
    


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
def output_file_alg1(alg_number, data,filename,standardd,decision,srednia):
    counter = 0
    file = filename[:-4]


    description = ["Numer chromosomu: ", "Dlugosc chromosomu referyncyjneg: ", "Liczba odczytow: ", "Srednie pokrycie [%]: ", "Decyzja: "]
    
    for row in data:
        row.append(decision[counter])
        counter = counter + 1


    with open("/home/vboxuser/Desktop/Licencjat/output_"+str(alg_number)+"/output_" + str(file) + ".csv", "w") as plik:
        for item in description:
            plik.write(str(item)+"\t")
        
        plik.write("\n")
        for row in data:
            plik.write(str(row[0]) + "\t")
            plik.write(str(row[1]) + "\t")
            plik.write(str(row[2]) + "\t")
            plik.write(str(row[3]) + "\t")
            plik.write(str(row[4]) + "\n")
            with open("/home/vboxuser/Desktop/Licencjat/output_"+str(alg_number)+"/endfile"+".txt", "a") as plik_end:
                if int(row[4]) == 1 and int(row[0])==21:
                    print("TEST: "+ str(row[4]) + "\n")
                    plik_end.write(str(file)+"\n")
        with open("/home/vboxuser/Desktop/Licencjat/output_"+str(alg_number)+"/srednie"+".txt", "a") as plik_mean:
            plik_mean.write(str(srednia)+"\n")    
    
        plik.write("Odchylenie standardowe dla osobnika: " + str(standardd) + "\n")
        plik.write("Srednia arytmetyczna: "+str(srednia))


        if int(alg_number) == 2:
        # SHOTGUN - Generowanie grup
          #  if srednia > 0.9:
          #      range_tab_1.append(str(file)+".txt")
          #  if srednia <= 0.9 and srednia > 0.6:
          #      range_tab_2.append(str(file)+".txt")
          #  if srednia <= 0.6 and srednia > 0.3:
          #      range_tab_3.append(str(file) + ".txt")
          #  if srednia <= 0.3 :
          #      range_tab_4.append(str(file)+".txt") 


        # CAPTURE - generowanie grup
            if srednia > 1.0:
                range_tab_1.append(str(file)+".txt")
            if srednia <= 1.0 and srednia > 0.5:
                range_tab_2.append(str(file)+".txt")
            if srednia <= 0.5 and srednia > 0.1:
                range_tab_3.append(str(file)+".txt")
            if srednia <= 0.1 :
                range_tab_4.append(str(file)+".txt")  

            print(range_tab_1)
            print(range_tab_2)
            print(range_tab_3)
            print(range_tab_4)
    
           
    print("Plik zostal zapisany")


# Algorytm wywolujacy pozostale funkcje
def alg1(data,filename, alg_number):
    """
    Zmienna column_*  przechowuja dane potrzebne do pozniejszego oznaczenia czy pokrycie danego chromosomu znajduje sie w zakresie
    """
    srednia = 1
    column_3 = [] 
    column_1 = []
    column_3_alg2 = [] #tablice nie biorace pod uwage chromosomow 13,18,21
    column_1_alg2 = []
    for row in data:
        coverage= round(float(row[2])/float(row[1])*100,3) # Srednie pokrycie
        row.insert(3,coverage) # Dodanie pokrycia do odpowiedniego wiersza z danymi
        row.pop(4)
        print(row)
        
        column_3.append(row[3]) 
        column_1.append(row[0])
        
        if int(alg_number) == 2 and (int(row[0]) != 13 and int(row[0]) != 18 and int(row[0]) != 21):
            column_3_alg2.append(row[3]) 
            column_1_alg2.append(row[0])

    if int(alg_number) == 1:
        srednia = average(column_3)
        standardd= standard_dev(column_3)
    if int(alg_number) == 2: 
        srednia = average(column_3_alg2)
        standardd= standard_dev(column_3_alg2)

    print("Srednia arytmetyczna: " + str(srednia))
    print("Odchylenie standardowe: "+ str(standardd)) #Kontrolne wypisane wyniku w konsoli
    output_file_alg1(alg_number,data,filename, standardd, is_within_range(column_1, column_3, srednia, standardd, data),srednia) # Wywolanie zapisu wyniku do pliku

 
def alg3(data,filename,alg_number):
    total=0
    chr21=0
    chr13=0
    chr18=0
    for row in data:
        if int(alg_number) == 3 and (int(row[0]) != 13 and int(row[0]) != 18 and int(row[0]) != 21):
            total = int(total) + int(row[2])
        if int(row[0]) == 13: 
            chr13 = row[2]
        if int(row[0]) == 18: 
            chr18 = row[2]
        if int(row[0]) == 21: 
            chr21 = row[2]
    
    R21=1.0*float(chr21)/(total)
    SE=math.sqrt((R21*(1.0-R21))/total)
    print("R21: "+str(R21))    
    if float(R21)> 0.02:
        file_path = "/home/vboxuser/Desktop/Licencjat/output_3/R21_output.txt"  # Nazwa pliku do zapisu
        with open(file_path, "a") as file:  # Tryb 'a' oznacza dopisywanie do pliku
            file.write( str(filename)+"\tR21: "+str(R21)+ "\n")

    
# Główna funkcja programu
def main(): 
    """
    Główna funkcja programu, która obsługuje logikę działania skryptu.
    """
    alg_number = input("Numer algorytmu: ")
    # Uruchomienie algorytmu nr.1
    if int(alg_number) == 1 or int(alg_number)==2:
        for f in sys.argv[1:]:
            print(f"Przetwarzam plik: {f}")
            if len(f) > 1:
                file = open_file(f)
                alg1(file,f,alg_number)
                
            else:
                print("Brak podanych argumentów.")
        table_range_write()
    # Algorytm ze wskaznikiem R
    if int(alg_number) == 3:
        for f in sys.argv[1:]:
            print(f"Przetwarzam plik: {f}")
            if len(f) > 1:
                file = open_file(f)
                alg3(file,f,alg_number)
    # Algorytm 4. - srednia trafien odczytu sekwencji danego chromosomu per populacja (all_samples.py)
    if int(alg_number) == 4:  
        for f in sys.argv[1:]:
            print(f"Przetwarzam plik: {f}")
            if len(f) > 1:
                all_samples.create_tables(f)
        all_samples.chromosomes_sort(all_samples.genomes_list)
        all_samples.chr_SD_mean() 
            
        for f in sys.argv[1:]:
            all_samples.decision(f)  

# Sprawdzenie, czy skrypt jest uruchamiany jako główny program
if __name__ == "__main__":
    main()