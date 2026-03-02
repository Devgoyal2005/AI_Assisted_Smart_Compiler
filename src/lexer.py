"""
Lexical Analyzer (Lexer) for TinyLang
Converts source code text into a stream of tokens
"""

from typing import List, Optional
from src.tokens import Token, TokenType, lookup_identifier


class Lexer:
    """
    Tokenizes source code into a list of tokens
    
    The lexer scans through the source code character by character,
    identifying and creating tokens for each meaningful element.
    """
    
    def __init__(self, source_code: str):
        """
        Initialize the lexer with source code
        
        Args:
            source_code: The complete source code to tokenize
        """
        self.source = source_code
        self.position = 0  # Current position in source
        self.line = 1      # Current line number
        self.column = 1    # Current column number
        self.tokens: List[Token] = []
        
    def current_char(self) -> Optional[str]:
        """Get the current character without advancing"""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at the next character(s) without advancing"""
        peek_pos = self.position + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self) -> Optional[str]:
        """Move to the next character and return current"""
        if self.position >= len(self.source):
            return None
        
        char = self.source[self.position]
        self.position += 1
        self.column += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
            
        return char
    
    def skip_whitespace(self):
        """Skip over whitespace characters"""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments (// comment)"""
        if self.current_char() == '/' and self.peek_char() == '/':
            # Skip until end of line
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        """
        Read a number token (integer or float)
        Examples: 123, 45.67, 0.5
        """
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        # Read digits before decimal point
        while self.current_char() and self.current_char().isdigit():
            num_str += self.current_char()
            self.advance()
        
        # Check for decimal point
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            num_str += self.current_char()  # Add '.'
            self.advance()
            
            # Read digits after decimal point
            while self.current_char() and self.current_char().isdigit():
                num_str += self.current_char()
                self.advance()
        
        # Convert to appropriate type
        value = float(num_str) if '.' in num_str else int(num_str)
        
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword
        Examples: x, myVar, if, print
        """
        start_line = self.line
        start_col = self.column
        identifier = ''
        
        # First character must be letter or underscore
        # Following characters can be letters, digits, or underscores
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        # Check if it's a keyword or regular identifier
        token_type = lookup_identifier(identifier)
        
        return Token(token_type, identifier, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """
        Main tokenization method
        Converts entire source code into list of tokens
        
        Returns:
            List of Token objects
        """
        while self.current_char() is not None:
            # Skip whitespace
            if self.current_char().isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Single and double character operators
            char = self.current_char()
            line = self.line
            col = self.column
            
            # Two-character operators (==, !=, >=, <=)
            if char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', line, col))
            elif char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, col))
            elif char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQ, '>=', line, col))
            elif char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQ, '<=', line, col))
            
            # Single character tokens
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', line, col))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', line, col))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER, '>', line, col))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS, '<', line, col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', line, col))
                self.advance()
            else:
                # Unknown character - report error but continue
                print(f"Warning: Unknown character '{char}' at {line}:{col}")
                self.advance()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        
        return self.tokens


# Main entry point for testing
if __name__ == '__main__':
    # Test the lexer with sample code
    test_code = """
    x = 5;
    y = x + 3;
    if (y > 5) {
        z = 1;
        print(z);
    }
    """
    
    print("=" * 50)
    print("LEXER TEST")
    print("=" * 50)
    print("\nSource Code:")
    print(test_code)
    print("\nTokens:")
    print("-" * 50)
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)
    
    print("\n" + "=" * 50)
    print(f"Total tokens: {len(tokens)}")
