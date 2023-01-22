import random


class mitarbeiter:
    def __init__(self, name, kranfuehrer=False, abwesend=False, qualifikationen=[]):
        self.name = name
        self.kranfuehrer = kranfuehrer
        self.abwesend = abwesend
        self.qualifications = qualifikationen
        self.letzte_schicht = None

    def __str__(self):
        return self.name

    def is_available(self):
        return not self.abwesend

    kalenderwoche = []

    def verteilung_schicht(self, personen, schicht_pro_woche):
        kranführer = [p for p in personen if p.kranfuehrer]
        nicht_kranführer = [p for p in personen if not p.kranfuehrer]
        random.shuffle(kranführer)
        random.shuffle(nicht_kranführer)

        kranführer_index = 0
        nicht_kranführer_index = 0

        for i in range(0, len(personen), 2):
            zugewiesene_mitarbeiter = {'frueh': [kranführer[kranführer_index % len(kranführer)]],
                                       'spaet': [kranführer[(kranführer_index + 1) % len(kranführer)]]}

            kranführer_index += 2
            if kranführer_index >= len(kranführer):
                kranführer_index = 0

            while nicht_kranführer_index < len(nicht_kranführer):
                if nicht_kranführer[nicht_kranführer_index].letzte_schicht != "frueh" and nicht_kranführer[
                    nicht_kranführer_index].letzte_schicht != "spaet":
                    zugewiesene_mitarbeiter['frueh'].append(nicht_kranführer[nicht_kranführer_index])
                    nicht_kranführer[nicht_kranführer_index].letzte_schicht = "frueh"
                    break
                nicht_kranführer_index += 1
            nicht_kranführer_index = 0
            while nicht_kranführer_index < len(nicht_kranführer):
                if nicht_kranführer[nicht_kranführer_index].letzte_schicht != "frueh" and nicht_kranführer[
                    nicht_kranführer_index].letzte_schicht != "spaet":
                    zugewiesene_mitarbeiter['spaet'].append(nicht_kranführer[nicht_kranführer_index])
                    nicht_kranführer[nicht_kranführer_index].letzte_schicht = "spaet"
                    break
                nicht_kranführer_index += 1
            nicht_kranführer_index = 0

            self.kalenderwoche.append(zugewiesene_mitarbeiter)

    # ToDo Korrigieren das alle Mitarbeiter einer Schicht zugewiesen werden und input mit einbauen für manuelle
    #  änderungen einbauen
    def print_output(self):
        for i, woche in enumerate(self.kalenderwoche):
            print(f'Week {i + 1}:')
            print(f'Morning shift: {[str(e) for e in woche["frueh"]]}')
            print(f'Evening shift: {[str(e) for e in woche["spaet"]]}')


# Instanzen der Klasse Employee erstellen
john_doe = mitarbeiter(name="John Doe", kranfuehrer=True)
jane_smith = mitarbeiter(name="Jane Smith", kranfuehrer=False)
bob_johnson = mitarbeiter(name="Bob Johnson", kranfuehrer=True)
mike_brown = mitarbeiter(name="Mike Brown", kranfuehrer=False)
marie_johnson = mitarbeiter(name="Marie Johnson", kranfuehrer=True)
tom_brown = mitarbeiter(name="Tom Brown", kranfuehrer=False)
# eine Liste von Mitarbeiterobjekten erstellen
personen = [john_doe, jane_smith, bob_johnson, mike_brown, marie_johnson, tom_brown]

# Eine Instanz der Klasse Employee erstellen
manager = mitarbeiter(name="Manager")

# Jedem Mitarbeiter eine Schicht zuweisen
num_of_weeks = 5
manager.verteilung_schicht(personen, num_of_weeks)

# Schichtplan ausgeben
manager.print_output()
