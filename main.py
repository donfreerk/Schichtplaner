import random


class Employee:
    def __init__(self, name, kranfuehrer=False, absent=False, qualifications=[]):
        self.name = name
        self.kranfuehrer = kranfuehrer
        self.absent = absent
        self.qualifications = qualifications
        self.last_shift = None

    def __str__(self):
        return self.name

    def is_available(self):
        return not self.absent

    kalenderwoche = []

    def verteilung_schicht(self, personen, schicht_pro_woche):
        crane_operators = [p for p in personen if p.kranfuehrer]
        non_crane_operators = [p for p in personen if not p.kranfuehrer]
        random.shuffle(crane_operators)
        random.shuffle(non_crane_operators)
        for i in range(schicht_pro_woche):
            zugewiesene_mitarbeiter = {'frueh': [crane_operators[i % len(crane_operators)]],
                                       'spaet': [crane_operators[(i + 1) % len(crane_operators)]]}

            for j in range(len(non_crane_operators)):
                if non_crane_operators[j].last_shift != "frueh" and non_crane_operators[j].last_shift != "spaet":
                    zugewiesene_mitarbeiter['frueh'].append(non_crane_operators[j])
                    non_crane_operators[j].last_shift = "frueh"
                    break
            for j in range(len(non_crane_operators)):
                if non_crane_operators[j].last_shift != "frueh" and non_crane_operators[j].last_shift != "spaet":
                    zugewiesene_mitarbeiter['spaet'].append(non_crane_operators[j])
                    non_crane_operators[j].last_shift = "spaet"
                    break

            self.kalenderwoche.append(zugewiesene_mitarbeiter)

    def mitarbeiter_einer_schicht_zuordnen(self, person, zugewiesene_mitarbeiter):
        if person.kranfuehrer:
            if not zugewiesene_mitarbeiter['frueh']:
                zugewiesene_mitarbeiter['frueh'].append(person)
            else:
                zugewiesene_mitarbeiter['spaet'].append(person)
        else:
            if not zugewiesene_mitarbeiter['frueh']:
                zugewiesene_mitarbeiter['frueh'].append(person)
            else:
                zugewiesene_mitarbeiter['spaet'].append(person)

    def check_vorige_woche(self, person, i):
        return person in self.kalenderwoche[i]['frueh'] or person in self.kalenderwoche[i]['spaet']

    def ersatz_finden(self, person):
        for ersatz_kandidat in personen:
            if ersatz_kandidat.kranfuehrer == person.kranfuehrer and ersatz_kandidat.is_available():
                return ersatz_kandidat
                return None

    def print_output(self):
        for i, week in enumerate(self.kalenderwoche):
            print(f'Week {i + 1}:')
            print(f'Morning shift: {[str(e) for e in week["frueh"]]}')
            print(f'Evening shift: {[str(e) for e in week["spaet"]]}')


# Create instances of the Employee class
john_doe = Employee(name="John Doe", kranfuehrer=True)
jane_smith = Employee(name="Jane Smith", kranfuehrer=False)
bob_johnson = Employee(name="Bob Johnson", kranfuehrer=True)
mike_brown = Employee(name="Mike Brown", kranfuehrer=False)
marie_johnson = Employee(name="Marie Johnson", kranfuehrer=True)
tom_brown = Employee(name="Tom Brown", kranfuehrer=False)
# create a list of employee objects
personen = [john_doe, jane_smith, bob_johnson, mike_brown, marie_johnson, tom_brown]

# Create an instance of the Employee class
manager = Employee(name="Manager")

# Assign shifts to each employee
num_of_weeks = 12
manager.verteilung_schicht(personen, num_of_weeks)

# Print the shift schedule
manager.print_output()