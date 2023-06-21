#include "lexer.h"
#include "token.h"
#include <stdio.h>

int main() {
    Lexer* lexer = initLexer("var name = \"test\"\nprint(name)\n");
    Token* token = (void*)0;
    while ((token = lexerGetNextToken(lexer)) != (void*)0) {
        printf("TOKEN '%d', '%s',\n", token->type, token->value);
    }
    return 1;
}