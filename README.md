# rocnikovy-projekt  
Algoritmus, ktory preveruje hypotezu o magickych stvorcoch.  

Podrobnu dokumentaciu kodu a popis algoritmu najdete v prilozenom PDF.  

Program spustite cez prikazovy riadok prikazom:  
**python rocnikovy_projekt.py [typ vyhladavania: bruteforce/random] [dolna hranica] [horna hranica] --iterations [pocet iteracii v nahodnom vyhladavani - dobrovolne] --cpu [pocet vyuzitych cpu jadier - dobrovolne]**  

Tieto informacie (vratane celkoveho poctu jadier vasho CPU) si zobrazite prikazom:  
**python rocnikovy_projekt.py -h**  

Ak chcem uplne vyhladavanie v intervale od 50 do 100 s vyuzitim 4 jadier, napisem:  
**python rocnikovy_projekt.py bruteforce 50 100 --cpu 4**  

Ak chcem nahodne vyhladavanie v intervale od 1 do 1000 s 5*10^7 pokusmi, napisem:  
**python rocnikovy_projekt.py random 1 1000 --iterations 50000000**  

Ak nezadate parameter *--iterations* pri nahodnom vyhladavani, automaticky sa vykona 10^7 pokusov.  
Ak nezadate parameter *--cpu*, automaticky sa budu vyuzivat vsetky jadra.
