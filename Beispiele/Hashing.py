#!/bin/env python3
import sys
# Bibliothek die Hashingalgorithmen implementiert
import hashlib

# Das Argument wird mit sys.argv[1] eingelesen (in Anführungszeichen oder ohne Leerzeichen)
# hashlib.sha256 übernimmt das Argument, dass mit .encode in Binary umgewandelt wird.
# .hexdigest() wandelt das Ergebnis in einen Hexadezimalstring um.
inputHash:str = hashlib.sha256(sys.argv[1].encode()).hexdigest()

# Das Passwort ist gehash hinterlegt.
# Dafür habe ich die Ausgabe von  print(hashlib.sha256(b"geheim").hexdigest()) kopiert.
passHash: str = "addb0f5e7826c857d7376d1bd9bc33c0c544790a2eac96144a8af22b1298c940"

# Eingabe Hash und Passworthash werden verglichen und die Antwort erfolgt.
if ( inputHash == passHash ):
    print("Login erfolgreich!")
else:
    print("Passwort ist falsch!")
