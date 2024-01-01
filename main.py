import chess
import chess.engine
import re

def extract_numerical_score(stockfish_output):
    # Define a regex pattern to match numbers
    pattern = r"[-+]?\d+"
    
    # Use re.findall to extract all numbers from the string
    numbers = re.findall(pattern, stockfish_output)
    
    return numbers[0] if numbers else None


board = chess.Board("rnbqkbnr/pppp1p1p/8/4p3/P3P1p1/5N2/1PPP1PPP/RNBQKB1R b KQkq - 0 4")

stockfish_path = r"Z:\Tools\stockfish-windows-x86-64-avx2.exe"

# Open the Stockfish engine
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
            # Analyze the position using Stockfish for 0.1 seconds
analysis = engine.analyse(board, chess.engine.Limit(time=5.0))

            # Extract numerical score from Stockfish output
numerical_score = extract_numerical_score(str(analysis["score"]))
print(numerical_score)