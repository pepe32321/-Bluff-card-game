# DSW-Obiekt-wka-45692
Programowanie obiektowe ćwiczenia gr. 3

Na zajęcia przygotowałem projekt gry karcianej w oszusta.

Gra polega na próbie odgadnięcia najwyższej figury pokerowej na stole.
Każdy z graczy zaczyna z jedną kartą i może zadeklarować wyższą figurę lub sprawdzić poprzedniego gracza.
W przypadku sprawdzenia gracz, który się pomylił zacznie następną rozgrywkę z jedną kartą więcej.
Jeżeli liczba kart gracza zwiększy się do pięciu, odpada on z dalszej gry.
Gra kończy się, gdy zostanie jeden gracz.

Kod napisałem w języku python.
Zdefiniowałem trzy klasy obiektów: karta, talia, gracz.
Napisałem dwie długie metody:
do generowania słownika możliwych deklaracji figur w rosnącej kolejności,
do sprawdzenia prawdziwości aktualnej deklaracji

Planowane kroki projektu:
-czyszczenie, uproszczenie istniejącego kodu
-implementacja wyboru strategii dla graczy (aktualnie decyzje są podejmowane losowo)
