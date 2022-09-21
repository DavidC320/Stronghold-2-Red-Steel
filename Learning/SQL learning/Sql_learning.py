# Beta Ally Storage Unit or A.S.U
# David Cruz
# 9/14/2022
# version Alpha 0.1.1

import sqlite3
# code based off of Kite's Sqlite3 Python Tutorial

database = sqlite3.connect("Learning/SQL learning/data_file.db")
cursor = database.cursor()

create_ally_roster = """
CREATE TABLE IF NOT EXISTS
allies(
    member_id INTEGER PRIMARY KEY,
    name TEXT,
    race TEXT,
    attack_preference TEXT,
    dead BOOL
    )
"""
cursor.execute(create_ally_roster)
# Create table if not exists is really helpful.

create_party_list = """
CREATE TABLE IF NOT EXISTS
parties(
    party_id INTEGER PRIMARY KEY,
    name TEXT,
    party_m_1 Integer,
    party_m_2 Integer,
    party_m_3 Integer,
    party_m_4 Integer,
    FOREIGN KEY(party_m_1) REFERENCES allies(member_id),
    FOREIGN KEY(party_m_2) REFERENCES allies(member_id),
    FOREIGN KEY(party_m_3) REFERENCES allies(member_id),
    FOREIGN KEY(party_m_4) REFERENCES allies(member_id)
    )"""
cursor.execute(create_party_list)

class Ally:
    def __init__(self, name, race, attack_pref, dead):
        self.name = name[:14]
        self.race = race[:14]
        self.attack_pref = attack_pref[:14]
        self.dead = dead

    def add_ally(self):
        command = f"""INSERT INTO allies (name, race, attack_preference, dead)
        VALUES ('{self.name}','{self.race}','{self.attack_pref}',{self.dead})"""
        cursor.execute(command)
        database.commit()

class Party:
    def __init__(self, name,  member_1, member_2, member_3, member_4):
        self.name = name[:19]
        self.member_1 = member_1
        self.member_2 = member_2
        self.member_3 = member_3
        self.member_4 = member_4
    
    def add_ally(self):
        qes = (self.member_1, self.member_2, self.member_3, self.member_4).count("?")
        list_of_none = []
        for _ in range(qes):
            list_of_none.append(None)

        command = f"""INSERT INTO parties (name, party_m_1, party_m_2, party_m_3, party_m_4)
        VALUES ('{self.name}', {self.member_1}, {self.member_2}, {self.member_3}, {self.member_4})"""
        cursor.execute(command, list_of_none)
        database.commit()

class Ally_storage_unit:
    def __init__(self):
        self.operate = True
        self.bool_dict = {
            "YES" : 1,
            "Y" : 1,
            "1" : 1,
            "TRUE" : 1,
            "T" : 1,
            "NO" : 0,
            "N" : 0,
            "0" : 0,
            "FALSE" : 0,
            "F" : 0
        }
    
    def asu(self):
        print("\nWelcome to the Ally Storage Unit or ASU\nVersion 0.1.1 A\n")
        while self.operate:
            print("""Action list:
            print allies - view all allies within the system
            print parties - view all parties within the system
            create ally - create an ally into the system
            create party - create a party into the system""")

            action = self.user_input()

            if action == "PRINT ALLIES":
                self.print_data("allies")

            elif action == "PRINT PARTIES":
                self.print_data("parties")

            elif action == "CREATE ALLY":
                self.create_ally()

            elif action == "CREATE PARTY":
                self.create_party()

            else:
                print("Sorry that's not a command")
    
    def user_input(self, true_text = False):
        if true_text:
            return input(": ")
        else:
            return input(": ").upper()

    def print_data(self, table):
        if table == "allies":
            command = f"SELECT * FROM {table}"
        else:
            command = f"""
            SELECT parties.party_id, parties.name, p1.name, p2.name, p3.name, p4.name
            From parties
            LEFT JOIN allies AS p1 ON parties.party_m_1 = p1.member_id
            LEFT JOIN allies AS p2 ON parties.party_m_2 = p2.member_id
            LEFT JOIN allies AS p3 ON parties.party_m_3 = p3.member_id
            LEFT JOIN allies AS p4 ON parties.party_m_4 = p4.member_id"""
        cursor.execute(command)
        data = cursor.fetchall()

        if len(data) == 0:
            table_dict = {
                "parties" : "a party",
                "allies" : "an ally"
            }
            print(f"Seems you don't have any {table}.\nCreate {table_dict.get(table)}")

        else:
            for record in data:
                print(record)

            print(f"Here is all of the {table}")

        print("Press enter to go back.")
        
        while True:
            action = self.user_input()
            if action or action == "":
                break

    def create_ally(self):
        op = True

        print("\nTo Create an ally you must enter a name, race, attack prefrence, and if there dead.\nIf you want to stop at any time enter stop.")
        while op:
            print("enter a name.\n")

            name = self.user_input(True)
            if name.upper() == "STOP":
                break

            print("enter a race.\n")

            race = self.user_input(True)
            if race.upper() == "STOP":
                break

            print("enter a attack prefrence.\n")

            attack = self.user_input(True)
            if attack.upper() == "STOP":
                break
            
            print("Are they dead?.\nY or N?\n")

            while True:
                dead = self.user_input()
                print(dead)
                print(self.bool_dict.keys())
                if dead in self.bool_dict.keys():
                    dead = self.bool_dict.get(dead)
                    break

                if dead  == "STOP":
                    op = False
                    break

                else:
                    print("This is not an action.\n Yes or No")
            
            if op == False:
                break
            else:
                ally = Ally(name, race, attack, dead)
                ally.add_ally()
                print("added ally to the unit.")
                break

    def create_party(self):
        print("\nTo create a party you must have at least one ally in the system.")
        
        command = f"SELECT * FROM allies"
        cursor.execute(command)
        data = cursor.fetchall()

        if len(data) == 0:
            print("Sorry but you don't have any allies in the system.\nYou will need to create one.\n")

        else:
            op = True
            print("You are able to create a party!")
            while op:
                print("You will need to enter a name for the party.\nIf you want to stop at anytime type in STOP")
                name = self.user_input(False)
                if name.upper() == "Stop":
                    break

                print("This is where you will be adding allies to the party.\nYou can't use the same party member.\nIf you use all of your allies, the party will be filled with Spaces")
                cursor.execute("SELECT allies.member_id, allies.name FROM allies")
                data = cursor.fetchall()
                a = {}
                for ally in data:
                    a.update({ ally[1].upper() : ally[0] })
                    print(ally)

                ally_numbers = len(data)
                names = a.keys()
                ids = a.values()

                party = []
                for _ in range(4):
                    if ally_numbers > len(party):
                        while True:
                            print("enter a party member. you can insert id or name\n")
                            member = self.user_input()

                            if member.isdigit():
                                if int(member) in ids:
                                    if int(member) not in party:
                                        print("Adding to the party.\n")
                                        party.append(int(member))
                                        break
                                    else:
                                        print("You already have this ally.\n")
                                else:
                                    print("This ally doesn't exist.\n")
                            else:
                                if member in names or member == "?":
                                    if member != "?":
                                        member = a.get(member)
                    
                                        if int(member) not in party:
                                            print("Adding to the party.\n")
                                            party.append(int(member))
                                            break
                                        else:
                                            print("You already have this ally.\n")
                                    else:
                                        print("Adding to the party.\n")
                                        party.append("?")
                                        break
                                else:
                                    print("This ally doesn't exist.\n")
                    else:
                        print("You have used all your allies.\n")
                        party.append("?")
                party = Party(name, party[0], party[1], party[2],party[3])
                party.add_ally()
                print("Party has been added to the system.\n")
                break




operator = Ally_storage_unit()
if __name__ == "__main__":
    operator.asu()
