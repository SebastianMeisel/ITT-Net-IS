import os
import sys
import subprocess


def bad_function(password):
    # Sicherheitslücke: Nutzung von subprocess mit unsicheren Eingaben
    command = "echo " + password
    os.system(command)


class my_class():
    def __init__(self, value):
        self.value = value

    def add(self, other):
        return self.value + other  # Typisierungsproblem


def unused_function():
    pass  # Diese Funktion wird nicht genutzt


if __name__ == "__main__":
    bad_function("mysecretpassword")  # Hardcodiertes Passwort
    obj = my_class(42)
    print(obj.add("test"))  # Fehlerhafte Typen
