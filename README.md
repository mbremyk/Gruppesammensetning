# Gruppesammensetning

Dette er et program for sammensetning av grupper til faget INFT1003 Webteknologi og teamarbeid ved NTNU

## Bruksanvisning
#### 1. Last ned .exe-filen
I mappen ./dist/ finner du [denne filen](./dist/Gruppesammensetning.exe). Trykk på last ned, og lagre den på et fornuftig sted.

#### 2. Generer et Excel-ark med data
For å kunne generere grupper, trenger du et regneark på formatet:

| ID  | Starttidspunkt | Fullføringstidspunkt | E-postadresse      | Navn       | Brukernavn | Programmeringserfaring        | Ønsket arbeidstid | Ønskede samarbeidspartnere |
|-----|----------------|----------------------|--------------------|------------|------------|-------------------------------|-------------------|----------------------------|
| 1   | Tid            | Tid                  | stud1@stud.ntnu.no | student1   | stud1      | Erfaring med JavaScript;      | Dagtid            | student2                   |
| 2   | Tid            | Tid                  | stud2@stud.ntnu.no | student2   | stud2      | Erfaring med andre språk;     | Kveldstid         |                            |
| 3   | Tid            | Tid                  | stud3@stud.ntnu.no | student3   | stud3      | Ingen programmeringserfaring; | Fleksibel         |                            |
| 4   | Tid            | Tid                  | stud4@stud.ntnu.no | student4   | stud4      | Følger JavaScript-kurs;       | Dagtid            |                            | 
| N/A | N/A            | N/A                  | **VIKTIG**         | **VIKTIG** | **VIKTIG** | **VIKTIG**                    | **VIKTIG**        | Frivillig                  |

Den kan genereres ved å la studentene svare på [dette spørreskjemaet](https://forms.office.com/Pages/ShareFormPage.aspx?id=cgahCS-CZ0SluluzdZZ8BVIwJWvqz_9Crtj1AnKbJ95UMDFaVjYwQkxDVzdZVUlYNERJRzZRNjlKSy4u&sharetoken=z0NOzokK5c78FgHYXRT3). For å få tak i en kopi av spørreskjemaet for å sende til studentene, må du:
1. Trykke på linken til [dette spørreskjemaet](https://forms.office.com/Pages/ShareFormPage.aspx?id=cgahCS-CZ0SluluzdZZ8BVIwJWvqz_9Crtj1AnKbJ95UMDFaVjYwQkxDVzdZVUlYNERJRzZRNjlKSy4u&sharetoken=z0NOzokK5c78FgHYXRT3) for å åpne det i en ny fane.
2. Trykk på _Dupliser det_  
Du vil nå få en kopi av skjemaet koblet til din Microsoft-konto
3. Endre navn og beskrivelse på skjemaet om nødvendig.  
**NB - Ikke endre på svaralternativene eller rekkefølgen på spørsmålene. Da vil ikke programmet fungere**
4. Klikk på _Del_, kopiér linken under _Send og samle inn svar_, og send til studentene. Pass på at **<ins>alle</ins>** studentene svarer på undersøkelsen
5. Etter at alle studentene har svart trykker du på _Svar_ og _Åpne i Excel_. Da vil du laste ned en Excel-fil du kan bruke i programmet

#### 3. Åpne programmet
Finn fram til der du lagret [main.exe](./dist/Gruppesammensetning.exe) og dobbeltklikk på filen

#### 4. Importer dataene fra steg 2
Klikk på knappen _Velg fil_  
Naviger til der du lagret Excel-filen med studentenes svar  
Klikk på filen, og deretter _Åpne_, eller dobbeltklikk på filen  
En liste med alle studentenes navn og e-postadresse skal dukke opp på venstre side, og _Antall studenter_ skal reflektere hvor mange studenter det er i lista  

#### 5. Opprett grupper
Klikk på knappen _Opprett grupper_  
En liste med grupper og informasjon om studentene i hver gruppe skal komme nede på høyre side

#### 6. Flytte studenter
Hvis du ikke er fornøyd med gruppene programmet har satt opp, kan du velge en student fra listen til venstre eller i gruppelisten, endre tallet i boksen markert _Gruppe:_, og trykke på _Flytt til gruppe X_

#### 7. Eksportere grupper og gruppemedlemmer
Når du er fornøyd med gruppene, kan du eksportere grupper og gruppemedlemmer ved å trykke på knappene _Eksporter grupper..._ og _Eksporter gruppemedlemmer..._
Siden BlackBoard importerer grupper og gruppemedlemmer separat, må det også eksporteres som to filer.
Velg filplassering og navn på filene (standard er _Grupper.csv_ og _Gruppemedlemmer.csv_)

#### 8. Importér grupper og gruppemedlemmer i BlackBoard
For å importere grupper og gruppemedlemmer går du til fagrommet til faget ditt i BlackBoard.
Under _Emnebehandling_ på venstre side velger du _Brukere og grupper_ og trykker på _Grupper_.  
Trykk på _Importer_  
Under _IMPORTER GRUPPEMEDLEMMER_ trykker du på _Bla gjennom min datamaskin_, navigerer til der du lagret de eksporterte filene, og velger filen som inneholder Gruppemedlemmene, standard navn er _Gruppemedlemmer.csv_  
Under _IMPORTER GRUPPER_ gjør du det samme, men velger filen med gruppene istedenfor, standard navn er _Grupper.csv_  
Velg hvilke verktøy gruppene skal ha tilgang til, og trykk _Send_  
BlackBoard er litt tregt, så om du ikke ser gruppene med én gang skal det bare være å vente litt og så laste inn siden på nytt med F5 eller Ctrl+R  
Hvis du ikke har endret innstillingene dine for mailing i BlackBoard skal du også få en mail når gruppene er importert

Nå skal gruppene være importert i BlackBoard. Sjekk om alle studentene er i en gruppe, og legg inn de som mangler


### Support
Ved eventuelle bugs eller problemer med programmet kan jeg kontaktes på [magbre@stud.ntnu.no](mailto:magbre@stud.ntnu.no?subject=Gruppesammensetning)