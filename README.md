# Gruppesammensetning

Dette er et program for sammensetning av grupper til faget INFT1003 Webteknologi og teamarbeid ved NTNU

## Bruksanvisning
#### 1. Last ned .exe-filen
I mappen ./dist/ finner du [denne filen](./dist/main.exe). Trykk på last ned, og lagre den på et fornuftig sted.

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
Finn fram til der du lagret [main.exe](./dist/main.exe) og dobbeltklikk på filen

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
