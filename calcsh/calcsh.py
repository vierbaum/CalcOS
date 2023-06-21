import string
TT_INT        = "INT"
TT_FLOAT      = "FLOAT"
TT_PLUS       = "PLUS"
TT_MINUS      = "MINUS"
TT_MUL        = "MUL"
TT_DIV        = "DIV"
TT_LPAREN     = "LPAREN"
TT_RPAREN     = "RPAREN"
TT_EOF        = "EOF"
TT_POWER      = "POWER"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD    = "KEYWORD"
TT_EQ         = "EQ"

LETTERS = string.ascii_letters
LETTERSDIGITS = LETTERS + "0123456789"
KEYWORDS = ["var"]

class Token:
    def __init__(self, t, v=None, posStart=None, posEnd=None):
        self.type = t
        self.value = v
        if posStart:
            self.posStart = posStart.copy()
            self.posEnd = self.posStart
            self.posEnd.advance()

        if posEnd:
            self.posEnd = posEnd.copy()

    def __repr__(self):
        if self.value:
            return "%s:%s"%(self.type, self.value)
        return self.type

    def matches(self, type_, value):
        return self.type == type_ and self.value == value


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, currentChar=None):
        self.idx += 1
        self.col += 1

        if currentChar == "\n":
            self.ln += 1
            self.col = 0

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def makeTokens(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in " \t": # skipping white space
                self.advance()
            elif self.currentChar in "0123456789":
                tokens.append(self.makeNumber())
            elif self.currentChar in LETTERS:
                tokens.append(self.makeIdentifier())
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS, posStart=self.pos))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_MINUS, posStart=self.pos))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL, posStart=self.pos))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV, posStart=self.pos))
                self.advance()
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN, posStart=self.pos))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN, posStart=self.pos))
                self.advance()
            elif self.currentChar == '^':
                tokens.append(Token(TT_POWER, posStart=self.pos))
                self.advance()
            elif self.currentChar == '=':
                tokens.append(Token(TT_EQ, posStart=self.pos))
                self.advance()
            else:
                posStart = self.pos.copy()
                char = self.currentChar
                self.advance
                return [], IllegalCharError(posStart, self.pos, char)

        tokens.append(Token(TT_EOF, posStart=self.pos))
        return tokens, None

    def makeNumber(self):
        numStr = ""
        dotCount = 0
        posStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in "0123456789.":
            if self.currentChar == ".":
                if dotCount >= 1:
                    break
                dotCount += 1
                numStr += "."
            else:
                numStr += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(numStr), posStart, self.pos)
        else:
            return Token(TT_FLOAT, float(numStr), posStart, self.pos)

    def makeIdentifier(self):
        idStr = ""
        posStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in LETTERSDIGITS + "_":
            idStr += self.currentChar
            self.advance()

        tokType = TT_KEYWORD if idStr in KEYWORDS else TT_IDENTIFIER
        return Token(tokType, idStr, posStart, self.pos)


class Error:
    def __init__(self, posStart, posEnd, errorName, details):
        self.posStart = posStart
        self.posEnd = posEnd
        self.errorName = errorName
        self.details = details

    def asString(self):
        result  = f'{self.errorName}: {self.details}\n'
        result += f'File {self.posStart.fn}, line {self.posStart.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Illegal Character', details)

class IllegalSyntaxError(Error):
    def __init__(self, posStart, posEnd, details):
        super().__init__(posStart, posEnd, 'Invalid Syntax', details)

class RunTimeError(Error):
    def __init__(self, posStart, posEnd, details, context):
        super().__init__(posStart, posEnd, 'Runtime Error', details)
        self.context = context

    def asString(self):
        result = self.generateTraceBack()
        result += f'{self.errorName}: {self.details}\n'
        return result

    def generateTraceBack(self):
        result = ""
        pos = self.posStart
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.displayName}\n' + result
            pos = ctx.parentEntryPos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.posStart = self.tok.posStart
        self.posEnd = self.tok.posEnd

    def __repr__(self):
        #return "%s"%(self.tok)
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, leftNode, opTok, rightNode):
        self.leftNode = leftNode
        self.opTok = opTok
        self.rightNode = rightNode
        self.posStart = self.leftNode.posStart
        self.posEnd = self.rightNode.posEnd

    def __repr__(self):
        return f'({self.leftNode}, {self.opTok}, {self.rightNode})'
        #return "%s, %s, %s"%(self.leftNode, self.opTok, self.rightNode)
    
class UnaryOpNode:
    def __init__(self, opTok, node):
        self.opTok = opTok
        self.node = node
        self.posStart = self.opTok.posStart
        self.posEnd = self.node.posEnd
    
    def __repr__(self):
        return "%s, %s"%(self.opTok, self.node)


class VarAccesNode:
    def __init__(self, varNameTok):
        self.varNameTok = varNameTok
        self.posStart = self.varNameTok.posStart
        self.posEnd = self.varNameTok.posEnd

class VarAssignNode:
    def __init__(self, varNameTok, valueNode):
        self.varNameTok = varNameTok
        self.valueNode = valueNode
        self.posStart = self.valueNode.posStart
        self.posEnd = self.valueNode.posEnd


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class RuntimeResult():
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokIdx = -1
        self.advance()

    def advance(self):
        self.tokIdx += 1
        if self.tokIdx < len(self.tokens):
            self.currentTok = self.tokens[self.tokIdx]
        return self.currentTok

    def parse(self):
        res = self.expr()
        if not res.error and self.currentTok.type != TT_EOF:
            return res.failure(IllegalSyntaxError(self.currentTok.posStart, self.currentTok.posEnd, "Expected +, -, *, /"))
        return res

    def atom(self):
        res = ParseResult()
        tok = self.currentTok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccesNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.currentTok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(IllegalSyntaxError(self.currentTok.posStart, self.currentTok.posEnd, "Missing )"))
        
        return res.failure(IllegalSyntaxError(tok.posStart, tok.posEnd, "Expected int, float, +, -, ()"))

    def power(self):
        return self.binOp(self.atom, (TT_POWER, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.currentTok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()
        #return res.failure(IllegalSyntaxError(tok.posStart, tok.posEnd, "Expexted float / int"))

    def term(self):
        return self.binOp(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()
        if self.currentTok.matches(TT_KEYWORD, "var"):
            res.register(self.advance())

            if self.currentTok.type != TT_IDENTIFIER:
                return res.failure(IllegalSyntaxError(self.currentTok.posStart, self.currentTok.posEnd, "Expected identifier"))

            varName = self.currentTok
            res.register(self.advance())

            if self.currentTok.type != TT_EQ:
                return res.failure(IllegalSyntaxError(self.currentTok.posStart, self.currentTok.posEnd, "Expected ="))

            res.register(self.advance())

            expr = res.register(self.expr())
            if res.error:
                return res

            return res.success(VarAssignNode(varName, expr))

        return self.binOp(self.term, (TT_PLUS, TT_MINUS))

    def binOp(self, func, ops, func2=None):
        if func2 == None:
            func2 = func
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.currentTok.type in ops:
            opTok = self.currentTok
            res.register(self.advance())
            right = res.register(func2())
            if res.error:
                return res
            left = BinOpNode(left, opTok, right)

        return res.success(left)


class Number:
    def __init__(self, value):
        self.value = value
        self.setPos()
        self.setContext()

    def setPos(self, posStart=None, posEnd=None):
        self.posStart = posStart
        self.posEnd = posEnd
        return self

    def setContext(self, context=None):
        self.context = context
        return self

    def addedTo(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).setContext(self.context), None

    def subtractedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).setContext(self.context), None

    def divBy(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.posStart, other.posEnd, "Division by zero", self.context)
            return Number(self.value / other.value).setContext(self.context), None

    def mulBy(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).setContext(self.context), None

    def powerOf(self, other):
        if isinstance(other, Number):
            if self.value == 0 and other.value == 0:
                return None, RunTimeError(other.posStart, other.posEnd, "Recieved undefined 0^0", self.context)
            return Number(self.value ** other.value).setContext(self.context), None


    def __repr__(self):
        return str(self.value)


class Context:
    def __init__(self, displayName, parent=None, parentEntryPos=None):
        self.displayName = displayName
        self.parent = parent
        self.parentEntryPos = parentEntryPos
        self.SymbolTable = None

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.set[name]

class Interpreter:
    def __init__(self):
        pass

    def visitVarAccesNode(self, node, context):
        res = RuntimeResult()
        varName = node.varNameTok.value
        value = context.SymbolTable.get(varName)

        if not value:
            return res.failure(RunTimeError(node.posStart, node.posEnd, "%s not defined"%(varName), context))
        
        return res.success(value)
    
    def visitVarAssignNode(self, node, context):
        res = RuntimeResult()
        varName = node.varNameTok.value
        value = res.register(self.visit(node.valueNode, context))

        if res.error:
            return res

        context.SymbolTable.set(varName, value)
        return res.success(value)

    def visit(self, node, context):
        methodName = "visit%s"%(type(node).__name__)
        method = getattr(self, methodName, self.noVisitMethod)
        return method(node, context)

    def noVisitMethod(self, node, context):
        raise Exception("No visit Method defined %s"%("visit%s"%(type(node).__name__)))

    def visitNumberNode(self, node, context):
        return RuntimeResult().success(Number(node.tok.value).setContext(context).setPos(node.posStart, node.posEnd))

    def visitBinOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.leftNode, context))
        if res.error:
            return res
        right = res.register(self.visit(node.rightNode, context))
        if res.error:
            return res

        error = None
        if node.opTok.type == TT_PLUS:
            result, error = left.addedTo(right)
        elif node.opTok.type == TT_MINUS:
            result, error = left.subtractedBy(right)
        elif node.opTok.type == TT_MUL:
            result, error = left.mulBy(right)
        elif node.opTok.type == TT_DIV:
            result, error = left.divBy(right)
        elif node.opTok.type == TT_POWER:
            result, error = left.powerOf(right)

        if error:
            return res.failure(error)
        return res.success(result.setPos(node.posStart, node.posEnd))

    def visitUnaryOpNode(self, node, context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None
        if node.opTok.type == TT_MINUS:
            number, error = number.mulBy(Number(-1))

        if error:
            return res.failure(error)
        return res.success(number.setPos(node.posStart, node.posEnd))

golbalSymbolTable = SymbolTable()
golbalSymbolTable.set("pi", "3.1415")
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()

    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.SymbolTable = golbalSymbolTable
    result = interpreter.visit(ast.node, context)

    return result.value, result.error