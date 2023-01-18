import csv
from random import random


class Person:
    def __init__(self, name: str, kranfuehrer: bool):
        self.name = name
        self.kranfuehrer = kranfuehrer


class Schichtplan:
    def __init__(self):
        self.fruehschicht = []
        self.spaetschicht = []
        self.kalenderwoche = []
        self.kranfuehrer_frueh = 0
        self.kranfuehrer_spaet = 0

    def personen_hinzufuegen(self, personen):
        self.personen = personen

    # def verteilung_schicht(self, personen, schicht_pro_woche):
    #     for i in range(schicht_pro_woche):
    #         for j in range(len(personen)):
    #             person = personen[j]
    #             if person.kranfuehrer:
    #                 if self.kranfuehrer_frueh < 1:
    #                     self.fruehschicht.append(person)
    #                     self.kranfuehrer_frueh += 1
    #                 elif self.kranfuehrer_spaet < 1:
    #                     self.spaetschicht.append(person)
    #                     self.kranfuehrer_spaet += 1
    #             else:
    #                 self.fruehschicht.append(person)
    #         self.kalenderwoche.append([self.fruehschicht, self.spaetschicht])
    #         self.fruehschicht.clear()
    #         self.spaetschicht.clear()
    #         self.kranfuehrer_frueh = 0
    #         self.kranfuehrer_spaet = 0

    def verteilung_schicht(self, personen, schicht_pro_woche):
        for i in range(schicht_pro_woche):
            kranfuehrer_frueh_scheduled = False
            kranfuehrer_spaet_scheduled = False
            additional_employee_scheduled = False
            for j in range(len(personen)):
                person = personen[j]
                # Check if employee is a kranfuehrer
                if person.kranfuehrer:
                    if not kranfuehrer_frueh_scheduled:
                        self.fruehschicht.append(person)
                        kranfuehrer_frueh_scheduled = True
                    elif not kranfuehrer_spaet_scheduled:
                        self.spaetschicht.append(person)
                        kranfuehrer_spaet_scheduled = True
                    else:
                        # check if the employee has been scheduled for the same shift in the previous week
                        if i > 0:
                            if person not in self.kalenderwoche[i-1][0] and person not in self.kalenderwoche[i-1][1]:
                                self.fruehschicht.append(person)
                                additional_employee_scheduled = True
                                break
                        else:
                            self.fruehschicht.append(person)
                            additional_employee_scheduled = True
                            break
                # check if a kranfuehrer and an additional employee have been scheduled for the morning and evening shift
                elif not kranfuehrer_frueh_scheduled or not kranfuehrer_spaet_scheduled or not additional_employee_scheduled:
                    if not kranfuehrer_frueh_scheduled:
                        self.fruehschicht.append(person)
                        additional_employee_scheduled = True
                    elif not kranfuehrer_spaet_scheduled:
                        self.spaetschicht.append(person)
                        additional_employee_scheduled = True
                    else:
                        # check if the employee has been scheduled for the same shift in the previous week
                        if i > 0:
                            if person not in self.kalenderwoche[i-1][0] and person not in self.kalenderwoche[i-1][1]:
                                self.fruehschicht.append(person)
                                additional_employee_scheduled =                                 self.fruehschicht.append(person)
                                additional_employee_scheduled = True
                                break
                        else:
                            self.fruehschicht.append(person)
                            additional_employee_scheduled = True
                            break
            self.kalenderwoche.append([self.fruehschicht, self.spaetschicht])
            self.fruehschicht.clear()
            self.spaetschicht.clear()
            kranfuehrer_frueh_scheduled = False
            kranfuehrer_spaet_scheduled = False
            additional_employee_scheduled = False

            #Manual input for absences and replacements
            for person in self.fruehschicht:
                if person.absent:
                    replacement_employee = self.find_replacement(person)
                    if replacement_employee:
                        self.fruehschicht.remove(person)
                        self.fruehschicht.append(replacement_employee)
                    else:
                        print("No replacement found for {}. Please contact supervisor.".format(person.name))
            for person in self.spaetschicht:
                if person.absent:
                    replacement_employee = self.find_replacement(person)
                    if replacement_employee:
                        self.spaetschicht.remove(person)
                        self.spaetschicht.append(replacement_employee)
                    else:
                        print("No replacement found for {}. Please contact supervisor.".format(person.name))





    def plan_erstellen(self, kalenderwochen):
        for i in range(kalenderwochen):
            self.verteilung_schicht(self.personen, 1)
            fruehschicht = [person.name for person in self.kalenderwoche[-1][0]]
            spaetschicht = [person.name for person in self.kalenderwoche[-1][1]]
            print("Kalenderwoche {}: Frühschicht - {} | Spätschicht - {}".format(i + 1,fruehschicht, spaetschicht))


        # Prüfe auf ausgefallene Personen und suche Ersatz
        # Prüfe auf ausgewogene Pausen zwischen den Schichten und angepasste Schichten
            # Prüfe ob jede Person nicht mehr als 2 Wochen hintereinander die gleiche Schicht hat
            for i in range(len(self.kalenderwoche) - 1):
                for j in range(len(self.kalenderwoche[i])):
                    for person in self.kalenderwoche[i][j]:
                        if person in self.kalenderwoche[i + 1][j]:
                            # find a replacement employee and add them to the schedule
                            replacement_employee = random.choice([x for x in self.personen if
                                                                  x not in self.kalenderwoche[i][j] and x not in
                                                                  self.kalenderwoche[i + 1][j]])
                            index = self.kalenderwoche[i + 1][j].index(person)
                            self.kalenderwoche[i + 1][j][index] = replacement_employee

            # Überprüfe, ob der Plan die Urlaubstage aller Personen berücksichtigt und fair verteilt
            for i in range(len(self.kalenderwoche)):
                for j in range(len(self.kalenderwoche[i])):
                    for person in self.kalenderwoche[i][j]:
                        # check if the employee has any remaining vacation days
                        if person.vacation_days > 0:
                            # find a replacement employee and add them to the schedule
                            replacement_employee = random.choice(
                                [x for x in self.personen if x not in self.kalenderwoche[i][j]])
                            index = self.kalenderwoche[i][j].index(person)
                            self.kalenderwoche[i][j][index] = replacement_employee
                            person.vacation_days -= 1

    # passenden Anpassungen hier vorzunehmen

