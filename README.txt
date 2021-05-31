# lil_wizard
Searching problem using ucs, a* and ida* alghorithms

Context
Un mic vrajitor a pornit la drum sa gaseasca o piatra magica. Numai ca piatra magica se gaseste intr-o pestera la fel de magica. Pestera e de forma dreptunghiulara impartita in parcele patratice, fiecare de o anumita culoare. La intrarea in pestera un batran vrajitor ii ofera o pereche de cizme de culoarea parcelei care se afla la intrarea in pestera, si il povatuieste sa nu calce niciodata cu o pereche de cizme de o culoare pe o parcela de alta culoare fiindca in mod sigur va muri. Micul vrajitor mai poate sa poarte in desaga o pereche in plus de cizme (o pereche de cizme de rezerva). Batranul de asemenea il atentioneaza ca din cauza energiei terenului vrajit, cizmele se strica dupa 3 parcele parcurse, iar daca nu le schimba pana se strica de tot, va ramane descult in urmatoarea parcela si iar va muri. Unele parcele pot contine o pereche de cizme. Micutul vrajitor poate lua acea pereche de cizme si sa o puna in desaga ori sa-si schimbe cizmele curente pentru intrarea intr-o noua parcela de alta culoare (la schimbarea cizmelor, daca are desaga goala le va pune pe cele vechi in desaga, altfel are de ales intre a le arunca pe acestea ori a le arunca pe cele din desaga si a le pune pe acestea in locul lor). Se considera ca schimbarea cizmelor se face dupa parasirea parcelei curente dar imediat inainte de intrarea intr-o noua parcela (deci sa zicem, intermediar, pe granita - dar nu e nevoie sa considerati granita ca o stare aparte; pasul si scimbarea cizmelor vor fi vazute ca o tranzitie unitara). Micul vrajitor atunci cand are desaga goala va lua intotdeauna cizmele din parcela sa le puna in desaga; de asemenea nu va arunca cizmele din desaga daca nu are altele pe care sa le puna in loc (fie cele incaltate, fie cele gasite in parcela). Insa daca cizmele din desaga sunt de aceeasi culoare cu cele din parcela si sunt nepurtate (numarul de purtari e 0) atunci nu le schimba (nu are de ce, ajunge la 2 stari succesoare posibile identice).



Se considera ca daca au fost luate cizmele dintr-o parcela, dupa plecarea vrajitorului, prin magie apare o noua pereche de aceeasi culoare in acelasi loc (deci daca a luat o pereche de acolo, dar dupa niste pasi a ajuns tot in acea parcela ar gasi o pereche de cizme la fel cu cele luate anterior, si le-ar putea folosi). Nu poate lua insa mai mult de o pereche de cizme dintr-o parcela (adica nu poate sa schimbe si cizmele din desaga si pe cele pe care le avea incaltate cu cele gasite in parcela). Cizmele gasite intr-o parcela sunt intotdeauna noi.

Vrajitorasul tinde spre reinnoirea cizmelor. Daca are in desaga cizme de culoarea celor gasite in parcela, sau poarta cizme de culoarea celor gasite in parcela le va reinnoi daca acestea nu sunt noi deja.

Pentru a nu obtine 2 succesori identici pentru anumite stari, luati in vedere faptul ca nu are sens sa-si schimbe cizmele din desaga cu cele incaltate daca sunt de aceeasi culoare si au acelasi numar de purtari.

La intrarea in pestera se considera ca s-a facut un pas, deci cizmele in starea initiala au numarul de purtari egal cu 1.

Atentie scopul nu e doar sa ajunga la piatra ci si sa iasa cu ea din pestera (intoarcerea la nodul initial). Dupa cum se vede micul vrajitor e supus la grea incercare si numai voi il puteti ajuta sa gaseasca drumul catre piatra magica.
Stări și tranziții. Cost
O stare e dată atât de poziția vrăjitorului cât și de elementele rămase pe hartă. Vrajitorul se poate misca doar pe linie si coloana, nu si pe diagonala. Fiecare deplasare pe un tip de relief are costul său (se adună costul celulei pe care ajunge, nu de pe care pleacă). În plus, se mai poate aduna costul unei schimbări de cizme care este 1.

Fisierul de intrare
Aveti un pic mai jos un exemplu de fisier de intrare. Primele linii conțin costurile pentru deplasarea pe fiecare formă de relief. Urmează un despărțitor și hărțile care sunt doua matrici separate printr-o linie goala. Liniile unei matrici sunt fiecare pe cate un rand nou. Elementele pe linie se separa prin spatii (se poate considera ca fiecare element al matricii e de un singur caracter). Prima matrice reprezinta harta efectiva cu culorile parcelelor. A doua matrice este cea care arata ce obiecte se gasesc in parcelele respective. Tot in a doua matrice e marcat locul de pornire cu un caracter * si locul unde se gaseste pitra cu un @. In parcela de pornire si in cea cu piatra nu aveti si cizme. Daca o parcela nu contine nimic, in matricea a doua va avea alocat un 0 pe pozitia corespunzatoare ei. De exemplu:

v 2
r 1
a 3
----
v r r r
v v a v
v a a a

0 r a *
0 0 0 0
0 0 @ v

Pentru acest exemplu de fisier de intrare se considera ca se porneste de la coordonatele 0,3 de pe o parcela de culoare r. Piatra se afla la coordonatele 2,2 pe o parcela de culoare a. Parcela de la coordonatele 0,0 este de culoare v si nu contine nimic. Parcela de la coordonatele 0,2 e de culoare r si contine cizme de culoare a.
Desi programul cunoaste harta, se considera ca vrajitorul nu stie cum arata terenul pana nu il descopera singur, mergand prin pestera.

Fișierul de ieșire va urma modelul de mai jos.

De exemplu pentru fisierul de intrare:

v 2
r 1
a 3
g 2
----
g r v v v v
a r r r r a
a v a r r a
v v a r r a
g g a r r a
v r r g v v
r r a a a a

0 * 0 0 0 0
g a 0 0 0 0
0 r 0 0 0 r
0 0 g 0 0 0
v 0 @ 0 0 0
0 0 0 0 0 g
0 0 0 0 0 0

O solutie posibila e cea de mai jos: (acesta ar fi si continutul fisierului de iesire)

Pas 0). Incepe drumul cu cizme de culoare r din locatia(0,1). Incaltat: r (purtari: 1). Desaga: nimic. Fara piatra.

Pas 1).Paseste din (0,1) in (1,1). Incaltat: r (purtari: 2). Desaga: nimic. Fara piatra.

Pas 2).A gasit cizme a. Schimba cizmele din desaga cu cele din patratel si porneste la drum. Paseste din (1,1) in (1,2). Incaltat: r (purtari: 3). Desaga: a (purtari: 0). Fara piatra.

Pas 3).I s-au tocit cizmele r. Incalta cizmele din desaga si porneste la drum. Paseste din (1,2) in (2,2). Incaltat: a (purtari: 1). Desaga: nimic. Fara piatra.

Pas 4).Paseste din (2,2) in (3,2). Incaltat: a (purtari: 2). Desaga: nimic. Fara piatra.

Pas 5).A gasit cizme g. Schimba cizmele din desaga cu cele din patratel si porneste la drum. Paseste din (3,2) in (4,2). Incaltat: a (purtari: 3). Desaga: g (purtari: 0). Fara piatra.

Pas 6).I s-au tocit cizmele a. Incalta cizmele din desaga  ia piatra si porneste la drum. Paseste din (4,2) in (4,1). Incaltat: g (purtari: 1). Desaga: nimic. Cu piatra.

Pas 7).Paseste din (4,1) in (4,0). Incaltat: g (purtari: 2). Desaga: nimic. Cu piatra.

Pas 8).A gasit cizme v. Muta cizmele incaltate in desaga si le incalta pe cele din patratel si porneste la drum. Paseste din (4,0) in (3,0). Incaltat: v (purtari: 1). Desaga: g (purtari: 2). Cu piatra.

Pas 9).Paseste din (3,0) in (3,1). Incaltat: v (purtari: 2). Desaga: g (purtari: 2). Cu piatra.

Pas 10).Paseste din (3,1) in (2,1). Incaltat: v (purtari: 3). Desaga: g (purtari: 2). Cu piatra.

Pas 11).I s-au tocit cizmele v. A gasit cizme r. Incalta aceste cizme si porneste la drum. Paseste din (2,1) in (1,1). Incaltat: r (purtari: 1). Desaga: g (purtari: 2). Cu piatra.

Pas 12).Paseste din (1,1) in (0,1). Incaltat: r (purtari: 2). Desaga: g (purtari: 2). Cu piatra.

A iesit din pestera.
