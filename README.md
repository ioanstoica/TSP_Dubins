## Descriere
Proiectul constă în implementarea unui algoritm care să determine traiectoria optimă pentru a parcurge un set de puncte intermediare, folosind primitive Dubins.

Proiectul este pentru materia SPER, anul 3, semestrul 2, 2023-2024.
Am ales tema:
    2.3 Parcurgere de puncte intermediare printr-o traiectorie Dubins
    Pentru o listă de puncte intermediare dată, construiți traiectoria formată din
primitive Dubins astfel încât să minimizați lungimea traiectoriei.
    Se cer următoarele:
    i) Alegeți ordinea de parcurgere a punctelor intermediare astfel încât să mini-
mizați lungimea traiectoriei (de exemplu printr-un algoritm de tipul trave-
ling salesman problem).
    ii) Ilustrați traiectoriile rezultate pentru diverse valori ale valorii de rază de
întoarcere minimă.

# Echipa
Stoica Ioan
Alexandru Andrei

## Resurse folosite
 - https://github.com/fgabbert/dubins_py - pentru a calcula traiectoriile Dubins
 - python_tsp - pentru a calcula traseul optim intr-o lista de puncte

## Cum se ruleaza
 - pip install python-tsp
 - pip install pygad
 - python main.py

## Obs: Daca pentru un punct, se schimba unghiul de plecare, se schimba si lungimea traiectoriei
ex:
 - Wptz = [Waypoint(0,0,0), 
    Waypoint(6000,7000,260), 
    Waypoint(1000,15000,180), 
    Waypoint(-5000,5000,270), 
    Waypoint(0,10000,180)]

 - Wptz = [Waypoint(0,0,0), 
        Waypoint(6000,7000,260), 
        Waypoint(1000,15000,180), 
        Waypoint(-5000,5000,270), 
        Waypoint(0,10000,0)]
    
 - Au traiectorii si distante diferite (45075 metri, respectiv 46979 metri)

## Timp de rulare
 - Pentru 5 puncte x 3 raze, timpul de rulare este de aproximativ 15 secunde
 - Pentru 7 puncte x 3 raze, timpul de rulare este de aproximativ 90 secunde
 - Pentru 8 puncte x 3 raze, timpul de rulare este de aproximativ 115 secunde
 - Pentru 9 puncte x 3 raze, timpul de rulare este de aproximativ 152 secunde
 - Pentru 10 puncte x 3 raze, timpul de rulare este de aproximativ 400 secunde

