import math
from typing import Any, Generator, Optional, Text, Union
from .utils import TokenType, LexException, all_syms, symbols, key_words


__all__ = ['Token', 'Lex']


class Token:
    def __init__(self, row: int, col: int,
                 tk_type: TokenType, value: Optional[Any]=None) -> None:
        self.row = row
        self.col = col
        self.tk_type = tk_type
        self.value = value

    def __str__(self) -> str:
        if self.tk_type == TokenType.tk_Integer:
            tk_str = f'{self.value:d}'
        elif self.tk_type == TokenType.tk_Ident:
            tk_str = f'{self.value:s}'
        elif self.tk_type == TokenType.tk_String:
            tk_str = f'"{self.value:s}"'
        else:
            tk_str = None
        symbol = all_syms[self.tk_type.value]

        if tk_str is None:
            return f'{self.row:d} {self.col:d} {symbol:s}'
        else:
            return f'{self.row:d} {self.col:d} {symbol:s} {tk_str}'


class Lex:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.fp = None
        self.the_ch = None
        self.curr_row = 1
        self.curr_col = 0

    def __enter__(self) -> object:
        self.fp = open(self.file_name, 'r')
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.fp.close()

    def char_trans(self) -> str:
        curr_row = self.curr_row
        curr_col = self.curr_col
        char = self.next_ch()
        ord_char = ord(char)

        if char == '\'':
            LexException('Empty char', self.curr_row, self.curr_col)
        elif char == '\\':
            char = self.next_ch()
            if char == 'n':
                ord_char = ord('\n')
            elif char == '\\':
                ord_char = ord('\\')
            else:
                LexException('Unrecognized escape',
                             self.curr_row, self.curr_col)
        if self.next_ch() != '\'':
            LexException('Multiple char found.',
                         self.curr_row, self.curr_col)

        self.next_ch()
        return Token(curr_row, curr_col, TokenType.tk_Integer, ord_char)


    def string_trans(self, start: str) -> Token:
        string = ''
        curr_row = self.curr_row
        curr_col = self.curr_col

        while self.next_ch() != start:
            if len(self.the_ch) == 0:
                raise LexException('EOF while scanning string literal',
                                   self.curr_row, self.curr_col)
            if self.the_ch == '\n':
                raise LexException('EOL while scanning string literal',
                                   self.curr_row, self.curr_col)
            string += self.the_ch

        self.next_ch()
        return Token(curr_row, curr_col, TokenType.tk_String, string)

    def look_ahead(self, expected_ch: str, if_meet: TokenType,
                   not_meet: TokenType) -> Token:
        curr_row = self.curr_row
        curr_col = self.curr_col
        
        if self.next_ch() == expected_ch:
            token = Token(curr_row, curr_col, if_meet)
        else:
            token = Token(curr_row, curr_col, not_meet)
        
        self.next_ch()
        return token

    def div_or_comment(self) -> Token:
        string = ''
        curr_col = self.curr_col
        curr_row = self.curr_row

        if self.next_ch() != '*':
            return Token(curr_row, curr_col, TokenType.tk_Div)
        
        # comment found
        # self.the_ch == '*'
        while True:
            self.next_ch()
            pre_ch = self.the_ch
            if self.the_ch == '*':
                self.next_ch()
                if self.the_ch == '/':
                    # comment token
                    token = Token(curr_row, curr_col,
                                 TokenType.tk_Comment, string)
                    break
                else:
                    string += pre_ch
            string += self.the_ch
            if len(self.the_ch) == 0:
                raise LexException('EOF in comment.',
                                   self.curr_row, self.curr_col)
        
        self.next_ch()
        return token

    def ident_or_int(self) -> Token:
        curr_row = self.curr_row
        curr_col = self.curr_col
        is_number = False
        string = ''

        while self.the_ch.isalnum() or self.the_ch == '_':
            string += self.the_ch
            if self.the_ch.isdigit():
                is_number = True
            self.next_ch()

        if len(string) == 0:
            raise LexException('Empty string.', self.curr_row, self.curr_col)

        if is_number:
            token = Token(curr_row, curr_col,
                         TokenType.tk_Integer, int(string))
        else:
            if string[0].isdigit():
                raise LexException()
            else:
                if string in key_words:
                    token_key_word = key_words[string]
                    token = Token(curr_row, curr_col, token_key_word)
                else:
                    token = Token(curr_row, curr_col,
                                 TokenType.tk_Ident, string)
        
        return token

    def next_ch(self) -> str:
        self.the_ch = self.fp.read(1)
        self.curr_col += 1

        if self.the_ch == '\n':
            self.curr_row += 1
            self.curr_col = 0

        return self.the_ch

    def next_token(self) -> Generator:
        self.next_ch()
        while True:
            while self.the_ch.isspace():
                self.next_ch()
                continue

            the_row = self.curr_row
            the_col = self.curr_col

            if len(self.the_ch) == 0:
                yield Token(the_row, the_col, TokenType.tk_EOI)
                break
            elif self.the_ch == '/':
                yield self.div_or_comment()
            elif self.the_ch == '\'':
                yield self.char_trans()
            elif self.the_ch == '<':
                yield self.look_ahead('=', TokenType.tk_Leq, TokenType.tk_Lss)
            elif self.the_ch == '>':
                yield self.look_ahead('=', TokenType.tk_Geq, TokenType.tk_Gtr)
            elif self.the_ch == '=':
                yield self.look_ahead('=', TokenType.tk_Eq, TokenType.tk_Assign)
            elif self.the_ch == '!':
                yield self.look_ahead('=', TokenType.tk_Neq, TokenType.tk_Not)
            elif self.the_ch == '&':
                yield self.look_ahead('&', TokenType.tk_And, TokenType.tk_EOI)
            elif self.the_ch == '|':
                yield self.look_ahead('|', TokenType.tk_Or, TokenType.tk_EOI)
            elif self.the_ch == '"':
                yield self.string_trans(start='"')
            elif self.the_ch in symbols:
                tk_type = symbols[self.the_ch]
                sym = all_syms[tk_type.value]
                token = Token(self.curr_row, self.curr_col, tk_type, sym)
                self.next_ch()
                yield token
            else:
                # identity or int
                yield self.ident_or_int()

    @classmethod
    def generate(cls, in_file: str, out_file: str) -> None:
        with cls(in_file) as lex:
            with open(out_file, 'w') as f:
                for token in lex.next_token():
                    # skip comment
                    if token.tk_type == TokenType.tk_Comment:
                        continue
                    f.write(str(token) + '\n')
