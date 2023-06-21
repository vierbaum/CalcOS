#ifndef LEXER_H_
#define LEXER_H_
#include "token.h"

typedef struct LexerStruct {
    char c;
    unsigned int i;
    char* contents;
} Lexer;

Lexer* initLexer(char* contents);

void lexerAdvance(Lexer* lexer);

Token* lexerAdvanceWithToken(Lexer* lexer, Token* token);

Token* lexerCollectId(Lexer* lexer);

Token* lexerCollectString(Lexer* lexer);

char* lexerGetCurrentCharAsString(Lexer* lexer);

Token* lexerGetNextToken(Lexer* lexer);

void lexerSkipWhitespace(Lexer* lexer);

#endif