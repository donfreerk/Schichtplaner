import csv
import random


class Person:
    def __init__(self, name: str, kranfuehrer: bool, absent: bool, urlaubstage: int):
        self.name = name
        self.kranfuehrer = kranfuehrer
        self.urlaubstage = urlaubstage
        self.absent = absent


class Schichtplan:
    def __init__(self):
        self.fruehschicht = []
        self.spaetschicht = []
        self.kalenderwoche = []
        self.kranfuehrer_frueh = 0
        self.kranfuehrer_spaet = 0
        self.frueh_personen = []
        self.spaet_personen = []

    # def init(self):
    #     self.fruehschicht = []
    #     self.spaetschicht = []
    #     self.kalenderwoche = []
    #     self.kranfuehrer_frueh = 0
    #     self.kranfuehrer_spaet = 0

    def personen_hinzufuegen(self, personen):
        self.personen = personen
        print(self.personen)

    def find_replacement(self, person):
        for employee in self.personen:
            if employee.name != person.name and not employee.kranfuehrer and not employee.absent:
                return employee
        return None

    def verteilung_schicht(self, personen, schicht_pro_woche):
        for i in range(schicht_pro_woche):
            kranfuehrer_frueh_geplant = False
            kranfuehrer_spaet_geplant = False
            zusätzlicher_mitarbeiter_geplant = False
            for j in range(len(personen)):
                person = personen[j]
                # Prüfen, ob der Mitarbeiter ein Kranführer ist
                if person.kranfuehrer:
                    if not kranfuehrer_frueh_geplant:
                        self.fruehschicht.append(person)
                        kranfuehrer_frueh_geplant = True
                    elif not kranfuehrer_spaet_geplant:
                        self.spaetschicht.append(person)
                        kranfuehrer_spaet_geplant = True
                    else:
                        # prüfen, ob der Arbeitnehmer in der Vorwoche für dieselbe Schicht eingeplant war
                        if i > 0:
                            if person not in self.kalenderwoche[i - 1][0] and person not in self.kalenderwoche[i - 1][
                                1]:
                                self.fruehschicht.append(person)
                                zusätzlicher_mitarbeiter_geplant = True
                                break
                        else:
                            self.fruehschicht.append(person)
                            zusätzlicher_mitarbeiter_geplant = True
                            break
                # prüfen, ob ein Kranführer und ein zusätzlicher Mitarbeiter für die Früh- und Spätschicht eingeplant
                # worden sind

                elif not kranfuehrer_frueh_geplant or not kranfuehrer_spaet_geplant or not zusätzlicher_mitarbeiter_geplant:
                    if not kranfuehrer_frueh_geplant:
                        self.fruehschicht.append(person)
                        zusätzlicher_mitarbeiter_geplant = True
                    elif not kranfuehrer_spaet_geplant:
                        self.spaetschicht.append(person)
                        zusätzlicher_mitarbeiter_geplant = True
                    else:
                        # prüfen, ob der Arbeitnehmer in der Vorwoche für dieselbe Schicht eingeplant war
                        if i > 0:
                            if person not in self.kalenderwoche[i - 1][0] and person not in self.kalenderwoche[i - 1][
                                1]:
                                self.fruehschicht.append(person)
                                zusätzlicher_mitarbeiter_geplant = self.fruehschicht.append(person)
                                zusätzlicher_mitarbeiter_geplant = True
                                break
                        else:
                            self.fruehschicht.append(person)
                            zusätzlicher_mitarbeiter_geplant = True
                            break
            self.kalenderwoche.append([self.fruehschicht, self.spaetschicht])

            kranfuehrer_frueh_geplant = False
            kranfuehrer_spaet_geplant = False
            zusätzlicher_mitarbeiter_geplant = False

            # Manuelle Eingabe für Abwesenheiten und Vertretungen
            for person in self.fruehschicht:
                if person.absent:
                    ersatz_mitarbeiter = self.find_replacement(person)
                    if ersatz_mitarbeiter:
                        self.fruehschicht.remove(person)
                        self.fruehschicht.append(ersatz_mitarbeiter)
                    else:
                        print("Kein Ersatz für {} gefunden. Bitte kontaktieren Sie Ihren Vorgesetzten.".format(
                            person.name))
            for person in self.spaetschicht:
                if person.absent:
                    ersatz_mitarbeiter = self.find_replacement(person)
                    if ersatz_mitarbeiter:
                        self.spaetschicht.remove(person)
                        self.spaetschicht.append(ersatz_mitarbeiter)
                    else:
                        print("Kein Ersatz für {} gefunden. Bitte kontaktieren Sie Ihren Vorgesetzten.".format(
                            person.name))

    def plan_erstellen(self, kalenderwochen):
        for i in range(kalenderwochen):
            self.verteilung_schicht(self.personen, 1)
            fruehschicht = [person.name for person in self.kalenderwoche[-1][0]]
            spaetschicht = [person.name for person in self.kalenderwoche[-1][1]]
            print("Kalenderwoche {}: Frühschicht - {} | Spätschicht - {}".format(i + 1, fruehschicht, spaetschicht))

            # Prüfe auf ausgefallene Personen und suche Ersatz
            # Prüfe auf ausgewogene Pausen zwischen den Schichten und angepasste Schichten
            #Prüfe, ob jede Person nicht mehr als 2 Wochen hintereinander die gleiche Schicht hat
            # for i in range(len(self.kalenderwoche) - 1):
            #     for j in range(len(self.kalenderwoche[i])):
            #         for person in self.kalenderwoche[i][j]:
            #             if person in self.kalenderwoche[i + 1][j]:
            #                 # # einen Ersatzmitarbeiter zu finden und ihn in den Zeitplan aufzunehmen
            #                 # ersatz_mitarbeiter = random.choice([x for x in self.personen if
            #                 #                                       x not in self.kalenderwoche[i][j] and x not in
            #                 #                                       self.kalenderwoche[i + 1][j]])
            #                 # index = self.kalenderwoche[i + 1][j].index(person)
            #                 # self.kalenderwoche[i + 1][j][index] = ersatz_mitarbeiter
            #                 # Prüfe auf ausgefallene Personen und suche Ersatz
            #                 ersatz_mitarbeiter = [x for x in self.personen if
            #                                       x not in self.kalenderwoche[i - 1][0] and x not in
            #                                       self.kalenderwoche[i - 1][1] and x.urlaubstage == 0]
            #                 if len(ersatz_mitarbeiter) > 0:
            #                     replacement_employee = random.choice(ersatz_mitarbeiter)
            #                 else:
            #                     pass
                                #print("kein Ersatz möglich")
                                # oder sende eine Meldung an Vorgesetzten

            #Überprüfe, ob der Plan die Urlaubstage aller Personen berücksichtigt und fair verteilt
            for i in range(len(self.kalenderwoche)):
                for j in range(len(self.kalenderwoche[i])):
                    for person in self.kalenderwoche[i][j]:
                        # prüfen, ob der Arbeitnehmer noch Urlaubstage hat
                        if person.urlaubstage > 0:
                            # einen Ersatzmitarbeiter zu finden und ihn in den Zeitplan aufzunehmen
                            ersatz_mitarbeiter = random.choice(
                                [x for x in self.personen if x not in self.kalenderwoche[i][j]])
                            index = self.kalenderwoche[i][j].index(person)
                            self.kalenderwoche[i][j][index] = ersatz_mitarbeiter
                            person.urlaubstage -= 1

    # passenden Anpassungen hier vorzunehmen


if __name__ == "__main__":
    # Beispieldaten für Personen
    personen = [
        Person("Max Mustermann", False, absent=False, urlaubstage=0),
        Person("Erika Mustermann", False, absent=False, urlaubstage=0),
        Person("John Doe", True, absent=False, urlaubstage=0),
        Person("Jane Doe", False, absent=False, urlaubstage=0),
        Person("Bob Smith", False, absent=True, urlaubstage=0),
        Person("Alice Johnson", True, absent=False, urlaubstage=0)
    ]

    schichtplan = Schichtplan()
    schichtplan.personen_hinzufuegen(personen)
    schichtplan.plan_erstellen(4)
