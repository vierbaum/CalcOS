#include "token.h"
#include <stdlib.h>


Token* initToken(int type, char* value) {
    Token* token = calloc(1, sizeof(struct TokenStruct));
    token->type = type;
    token->value = value;

    return token;
}