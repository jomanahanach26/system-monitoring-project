"""Tester för session_length.py. Kör med: python test_session_length.py"""

import math

from session_length import ITERATIONS, SECONDS, SessionLength, parse_length, parse_length_type

# parse_length_type: "1" är varv och "2" är sekunder
assert parse_length_type("1") == ITERATIONS
assert parse_length_type("2") == SECONDS
assert parse_length_type(" 2 ") == SECONDS

# parse_length_type: ogiltiga val ger None
assert parse_length_type("3") == None
assert parse_length_type("varv") == None
assert parse_length_type("") == None

# parse_length: heltal från 1 och uppåt är giltiga längder
assert parse_length("1") == 1
assert parse_length("30") == 30
assert parse_length(" 5 ") == 5

# parse_length: "oändligt" eller "o" ger en oändlig längd
assert parse_length("oändligt") == math.inf
assert parse_length("OÄNDLIGT") == math.inf
assert parse_length("o") == math.inf

# parse_length: 0, negativa tal, decimaltal och text är inte giltiga längder
assert parse_length("0") == None
assert parse_length("-5") == None
assert parse_length("2.5") == None
assert parse_length("fem") == None
assert parse_length("") == None

# is_finished för varv: klar när antalet varv har uppnåtts
five_iterations = SessionLength(ITERATIONS, 5)
assert five_iterations.is_finished(4, 100.0) == False
assert five_iterations.is_finished(5, 0.0) == True

# is_finished för sekunder: klar när antalet sekunder har passerat
thirty_seconds = SessionLength(SECONDS, 30)
assert thirty_seconds.is_finished(100, 29.9) == False
assert thirty_seconds.is_finished(0, 30.0) == True

# is_finished för oändlig längd: aldrig klar
infinite_iterations = SessionLength(ITERATIONS, math.inf)
assert infinite_iterations.is_finished(1000000, 1000000.0) == False

# str ger en läsbar beskrivning av längden
assert str(five_iterations) == "5 varv"
assert str(thirty_seconds) == "30 sekunder"
assert str(infinite_iterations) == "oändligt antal varv"
assert str(SessionLength(SECONDS, math.inf)) == "oändligt antal sekunder"

print("Alla tester för session_length gick igenom")
