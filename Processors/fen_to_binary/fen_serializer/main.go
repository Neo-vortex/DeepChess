package main

import (
	"C"
	"encoding/base64"

	"github.com/notnil/chess"
)
import (
	"fmt"
)

//export UnMarshalBinary
func UnMarshalBinary(bin *C.char) *C.char {
	game := chess.NewGame()

	// Convert C string to Go string
	goString := C.GoString(bin)

	// Convert Go string to byte array
	data := []byte(goString)

	game.Position().UnmarshalBinary(data)
	fen := game.FEN()

	// Convert Go string result back to C string
	return C.CString(fen)
}

//export MarshalBinary
func MarshalBinary(fen *C.char) *C.char {
	pos, err := chess.FEN(C.GoString(fen))
	if err != nil {
		return C.CString("")
	}

	game := chess.NewGame(pos)
	data, err := game.Position().MarshalBinary()
	if err != nil {
		return C.CString("")
	}

	base64String := base64.StdEncoding.EncodeToString(data)
	return C.CString(base64String)
}

func main() {
	var pos, _ = chess.FEN("r1bq1rk1/1pp3b1/3p1nn1/4pppp/1PP1P3/2NP2P1/2NB1PBP/1R1Q1RK1 w - - 1 16")
	game := chess.NewGame(pos)
	var data, _ = game.Position().MarshalBinary()
	base64String := base64.StdEncoding.EncodeToString(data)
	fmt.Println(base64String)
}
