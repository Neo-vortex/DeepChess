import chess
import chess.engine
import chess.pgn
import re
import sqlite3
from tqdm import tqdm
import glob

# Function to read the checkpoint file
def read_checkpoint():
    try:
        with open('checkpoint.txt', 'r') as checkpoint_file:
            return int(checkpoint_file.read().strip())
    except FileNotFoundError:
        return 0

# Function to write the checkpoint file
def write_checkpoint(line_number):
    with open('checkpoint.txt', 'w') as checkpoint_file:
        checkpoint_file.write(str(line_number))

# Open a connection to the SQLite database (create if not exists)
conn = sqlite3.connect('chess_evals.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fen TEXT,
        eval INTEGER,
        binary TEXT
    )
''')

# Open the engine
engine = chess.engine.SimpleEngine.popen_uci("/home/neo/Tools/stockfish/stockfish-ubuntu-x86-64-avx2")

# Get a list of all files matching the pattern output*.txt
output_files = glob.glob('output*.txt')

# Iterate over each output file
for output_file in output_files:
    # Read the checkpoint to determine where to start
    start_line = read_checkpoint()

    with open(output_file, 'r') as file:
        # Read all lines into a list
        all_lines = file.readlines()
        all_lines = all_lines[start_line:]
        all_lines = list(set(all_lines))

    # Process and save results to the database
    buffer = []

    for line_number, line in tqdm(enumerate(all_lines, start=start_line), desc=f"Processing lines in {output_file}", unit="line"):
        # Rest of your existing processing code

        # Add the data to the buffer
        buffer.append((fen, eval_value))

        # Check if the buffer is full, and if so, commit to the database and update checkpoint
        if len(buffer) >= 1000:
            cursor.executemany('INSERT INTO evaluations (fen, eval) VALUES (?, ?)', buffer)
            conn.commit()
            # Clear the buffer
            buffer = []
            # Update the checkpoint after processing every 1000 lines
            write_checkpoint(line_number)

    # Commit any remaining items in the buffer to the database
    if buffer:
        cursor.executemany('INSERT INTO evaluations (fen, eval) VALUES (?, ?)', buffer)
        conn.commit()

    # Update the final checkpoint after processing all lines
    write_checkpoint(len(all_lines))

# Close the database connection
conn.close()
