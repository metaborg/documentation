# Lexing and Parsing
IntelliJ relies on a lexer and parser.

## Lexer
The lexer shall extend the `com.intellij.lexer.Lexer` class (usually through
the `com.intellij.lexer.LexerBase` class). IntelliJ will call its `start`
method, providing it with a character buffer and range that need to be lexed,
and the lexer state at the start of the region. Then the lexer will lex forward
on each call to `advance`, providing information about the current token's type
and offset, and the lexer state at that point.

Note that the lexer may not know which file is being lexed, and it needs to be
able to start at any arbitrary point in the input. Also, it needs to return
_every_ token, including layout, even invalid ones.

## Parser
The parser is fed the lexer tokens, and turns them into AST nodes. A single AST
node can consist of multiple tokens. Again, the parser must be able to parse
from within a file.
