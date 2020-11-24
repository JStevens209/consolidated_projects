package utilities

import (
	"regexp"
	"strings"
)

const (
	T_IGNORE     = "_<IGNORE>"
	T_CURRENCY   = "_<CURRENCY>"
	T_AT         = "_<AT>"
	T_DOT        = "_<DOT>"
	T_DASH       = "_<DASH>"
	T_PAREN      = "_<PAREN>"
	T_COMMA      = "_<COMMA>"
	T_BREAK      = "<BRK>"
	T_NUMBER     = "<NUM>"
	T_NUMBER_1D  = "<NUM_1D>"
	T_NUMBER_3D  = "<NUM_3D>"
	T_NUMBER_4D  = "<NUM_4D>"
	T_NUMBER_5D  = "<NUM_5D>"
	T_WORD       = "<WORD>"
	T_IDENTIFIER = "<WORD_ID>"
)

type Token struct {
	Label   string
	Pattern string
}

var (
	tokens = []Token{

		Token{T_AT, "^[@]$"},
		Token{T_DOT, "^[.]$"},
		Token{T_CURRENCY, "^[\\$]$"},
		Token{T_DASH, "^[-]$"},
		Token{T_COMMA, "^[,]$"},
		Token{T_PAREN, "^[\\(\\)\\[\\]\\{\\}]$"},
		Token{T_BREAK, "^[•¶\\|\\+\\*]$"},

		Token{T_NUMBER_1D, "^(\\d{1})$"},
		Token{T_NUMBER_3D, "^(\\d{3})$"},
		Token{T_NUMBER_4D, "^(\\d{4})$"},
		Token{T_NUMBER_5D, "^(\\d{5})$"},
		Token{T_NUMBER, "^((\\d{1,3},?)+(\\.\\d+)?)$"},

		Token{T_WORD, "^([a-zA-Z]+)$"},
		Token{T_IDENTIFIER, "^\\w+$"},
		Token{T_IGNORE, "^\\W+$"},
	}
)

func Tokenize(text string) string {

	for _, token := range tokens {

		normalized := strings.ToLower(strings.TrimSpace(text))
		label := token.Label
		pattern := token.Pattern
		if Re(pattern, normalized) {
			return label
		}
	}
	return ""
}

func Re(pattern, text string) bool {
	matched, goerr := regexp.MatchString(pattern, strings.ToLower(text))
	if goerr != nil {
		return false
	}
	return matched
}
