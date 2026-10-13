import ast

try:
  with open("database.py", "r", encoding="utf-8") as f:
    source_code = f.read()

  # Tenta di analizzare l'albero sintattico del database
  ast.parse(source_code)
  print("✅ Sintassi di database.py perfetta! Nessun errore trovato.")

except SyntaxError as e:
  print("❌ TROVATO UN ERRORE DI SINTASSI!")
  print(f"----------------------------------------")
  print(f"📄 File: {e.filename}")
  print(f"🔢 Riga esatta: {e.lineno}")
  print(f"📌 Colonna: {e.offset}")
  print(f"💬 Descrizione: {e.msg}")
  print(f"🔍 Codice incriminato:\n{e.text}")
