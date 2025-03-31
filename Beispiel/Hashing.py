#!/bin/env python3
import sys
import hashlib

inputHash:str = hashlib.sha256(sys.argv[1].encode()).hexdigest()
passHash: str = hashlib.sha256(b"geheim").hexdigest()

if ( inputHash == passHash ):
    print("Login erfolgreich!")
else:
    print("Passwort ist falsch!")
