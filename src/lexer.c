#include "lexer.h"
#include "token.h"
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

Lexer* initLexer(char* contents) {
    Lexer* lexer = calloc(1, sizeof(struct LexerStruct));
    lexer->contents = contents;
    lexer->i = 0;
    lexer->c = contents[0];
    return lexer;
}

void lexerAdvance(Lexer* lexer) {
    if (lexer->c != '\0' && lexer->i < strlen(lexer->contents)) {
        lexer->i++;
        lexer->c = lexer->contents[lexer->i];
    }
}

Token* lexerAdvanceWithToken(Lexer* lexer, Token* token) {
    lexerAdvance(lexer);
    return token;
}

Token* lexerCollectId(Lexer* lexer) {
    //lexerAdvance(lexer);

    char* value = calloc(1, sizeof(char));
    value[0] = '\0';

    while (isalnum(lexer->c))
    {
        char* s = lexerGetCurrentCharAsString(lexer);
        value = realloc(value, (strlen(value) + strlen(s) + 1) * sizeof(char));
        strcat(value, s);

        lexerAdvance(lexer);
    }

    return initToken(TOKENID, value);
}

Token* lexerCollectString(Lexer* lexer) {
    lexerAdvance(lexer);

    char* value = calloc(1, sizeof(char));
    value[0] = '\0';

    while (lexer->c != '"')
    {
        char* s = lexerGetCurrentCharAsString(lexer);
        value = realloc(value, (strlen(value) + strlen(s) + 1) * sizeof(char));
        strcat(value, s);

        lexerAdvance(lexer);
    }

    lexerAdvance(lexer);

    return initToken(TOKENSTRING, value);

}

char* lexerGetCurrentCharAsString(Lexer* lexer) {
    char* str = calloc(2, sizeof(char));
    str[0] = lexer->c;
    str[1] = '\0';

    return str;
}

Token* lexerGetNextToken(Lexer* lexer) {
    while (lexer->c != '\0' && lexer-> i < strlen(lexer->contents)) {
        if (lexer->c == ' '){

            lexerSkipWhitespace(lexer);
        }

        if (isalnum(lexer->c)) {
            return lexerCollectId(lexer);

        }

        if (lexer->c == '"') {
            return lexerCollectString(lexer);

        }

        switch (lexer->c) {
            case '=': return lexerAdvanceWithToken(lexer, initToken(TOKENEQUALS, lexerGetCurrentCharAsString(lexer)));
                break;
            case '\n': return lexerAdvanceWithToken(lexer, initToken(TOKENSEMI, lexerGetCurrentCharAsString(lexer)));
                break;
            case '(': return lexerAdvanceWithToken(lexer, initToken(TOKENLPAREN, lexerGetCurrentCharAsString(lexer)));
                break;
            case ')': return lexerAdvanceWithToken(lexer, initToken(TOKENRPAREN, lexerGetCurrentCharAsString(lexer)));
                break;
        }
    }
    return (void*)0;
}

void lexerSkipWhitespace(Lexer* lexer) {
    while (lexer->c == ' ')
        lexerAdvance(lexer);
}