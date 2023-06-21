#ifndef TOKEN_H_
#define TOKEN_H_

typedef struct TokenStruct {
    enum {
        TOKENID,
        TOKENEQUALS,
        TOKENSTRING,
        TOKENSEMI,
        TOKENLPAREN,
        TOKENRPAREN
    } type;
    char* value;
} Token;

Token* initToken(int type, char* value);
#endif