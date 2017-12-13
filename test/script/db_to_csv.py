import sqlite3

connection = sqlite3.connect("db.sqlite3")

with open("Mahasiswa.csv", "w") as write_file:
    cursor = connection.cursor()
    for row in cursor.execute("SELECT * FROM polls_Mahasiswa"):
        writeRow = ",".join(str(v) for v in row)
        write_file.write(writeRow)
        write_file.write("\n")
