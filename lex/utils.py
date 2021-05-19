from enum import Enum


__all__ = ['TokenType', 'all_syms', 'symbols', 'key_words', 'LexException']


class TokenType(Enum):
    tk_EOI = 0
    tk_Mul = 1
    tk_Div = 2
    tk_Mod = 3
    tk_Add = 4
    tk_Sub = 5
    tk_Negate = 6
    tk_Not = 7
    tk_Lss = 8
    tk_Leq = 9
    tk_Gtr = 10
    tk_Geq = 11
    tk_Eq = 12
    tk_Neq = 13
    tk_Assign = 14
    tk_And = 15
    tk_Or = 16
    tk_If = 17
    tk_Else = 18
    tk_While = 19
    tk_Print = 20
    tk_Putc = 21
    tk_Lparen = 22
    tk_Rparen = 23
    tk_Lbrace = 24
    tk_Rbrace = 25
    tk_Semi = 26
    tk_Comma = 27
    tk_Ident = 28
    tk_Integer = 29
    tk_String = 30
    tk_Comment = 31


all_syms = ["End_of_input", "Op_multiply", "Op_divide", "Op_mod",
            "Op_add", "Op_subtract", "Op_negate", "Op_not", "Op_less",
            "Op_lessequal", "Op_greater", "Op_greaterequal", "Op_equal",
            "Op_notequal", "Op_assign", "Op_and", "Op_or", "Keyword_if",
            "Keyword_else", "Keyword_while", "Keyword_print", "Keyword_putc",
            "LeftParen", "RightParen", "LeftBrace", "RightBrace", "Semicolon",
            "Comma", "Identifier", "Integer", "String", "Comment"]


# single character only symbols
symbols = { '{': TokenType.tk_Lbrace,
            '}': TokenType.tk_Rbrace,
            '(': TokenType.tk_Lparen,
            ')': TokenType.tk_Rparen,
            '+': TokenType.tk_Add,
            '-': TokenType.tk_Sub,
            '*': TokenType.tk_Mul,
            '%': TokenType.tk_Mod,
            ';': TokenType.tk_Semi,
            ',': TokenType.tk_Comma}


 # keywords
key_words = {'if': TokenType.tk_If,
             'else': TokenType.tk_Else,
             'print': TokenType.tk_Print,
             'putc': TokenType.tk_Putc,
             'while': TokenType.tk_While}


class LexException(Exception):
    def __init__(self, msg: str, row: int, col: int) -> None:
        msg = f'{msg}, row {row} col {col}.'
        super().__init__(msg)
