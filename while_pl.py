
(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, SEMI, EOF, 
EQUAL, LESSTHAN, GREATERTHAN, AND, OR, NOT, IF, THEN, ELSE , LBRACE, RBRACE,
WHILE, DO, TRUE, FALSE, SKIP) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN','SEMI', 'EOF',
    'EQUAL', 'LESSTHAN', 'GREATERTHAN', 'AND', 'OR', 'NOT','if','then','else', '{', '}',
    'while', 'do', 'true', 'false', 'skip'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'if': Token('if','if'),
    'then': Token('then','then'),
    'else': Token('else','else'),
    'while': Token('while','while'),
    'do': Token('do','do'),
    'true': Token('true','true'),
    'false': Token('false','false'),
    'skip': Token('skip','skip')
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')

            if self.current_char == '<':
                self.advance()
                return Token(LESSTHAN, '<')

            if self.current_char == '>':
                self.advance()
                return Token(GREATERTHAN, '>')

            if self.current_char == '∧':
                self.advance()
                return Token(AND, '∧')

            if self.current_char == '∨':
                self.advance()
                return Token(OR, '∨')

            if self.current_char == '¬':
                self.advance()
                return Token(NOT, '¬')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass

class If(AST):
    def __init__(self, boolean, if_true, if_false):
        self.boolean = boolean 
        self.if_true = if_true
        self.if_false = if_false

class While(AST):
    def __init__(self, boolean, if_true):
        self.boolean = boolean 
        self.if_true = if_true

class Relation(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right 

class Comparison(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right 

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            #print('worked',self.current_token, token_type)
            self.current_token = self.lexer.get_next_token()            
        else:
            #print(self.current_token, token_type)
            self.error()

    def program(self):
        node = self.compound_statement()
        return node

    def compound_statement(self):

        nodes = self.statement_list()
        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def while_compound(self):
        self.eat(WHILE)
        boolean = self.boolean_relation()
        self.eat(DO)
        if self.current_token.type == LBRACE:
            self.eat(LBRACE)
            if_true = self.compound_statement()
            self.eat(RBRACE)
        else:
            if_true = self.statement()
        # if self.current_token.type == ELSE:

        node = While(boolean, if_true)   

        return node     

    def if_compound(self):
        self.eat(IF)
        boolean = self.boolean_relation()
        self.eat(THEN)
        if self.current_token.type == LBRACE:
            self.eat(LBRACE)
            if_true = self.compound_statement()
            self.eat(RBRACE)
        else:
            if_true = self.statement()
        # if self.current_token.type == ELSE:
        self.eat(ELSE)
        if self.current_token.type == LBRACE:
            self.eat(LBRACE)
            if_false = self.compound_statement()
            self.eat(RBRACE)
        else:
            if_false = self.statement()
        # else:
        node = If(boolean, if_true, if_false)

        return node

    def boolean_relation(self):

        def core():
            token = self.current_token
            if token.type == NOT:
                self.eat(NOT)
                left = self.boolean_comparison()
                node = Relation(left,token,None)
            else:
                left = self.boolean_comparison()
                token = self.current_token
                if token.type == AND:
                    self.eat(AND)
                    right = self.boolean_comparison()
                    node = Relation(left,token,right)
                elif token.type == OR:
                    self.eat(OR)
                    right = self.boolean_comparison()
                    node = Relation(left,token,right)
                else:
                    node = Relation(left,None,None)

            return node 

        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = core()
            self.eat(RPAREN)
        else:
            node = core()

        return node 
    
    def boolean_comparison(self):

        def core():
            if self.current_token.type is TRUE:
                self.eat(TRUE)
                node = Comparison(True,None,None)
            elif self.current_token.type is FALSE:
                self.eat(FALSE)
                node = Comparison(False,None,None)
            else:
                left = self.expr()
                token = self.current_token
                if token.type == EQUAL:
                    self.eat(EQUAL)
                elif token.type == LESSTHAN:
                    self.eat(LESSTHAN)
                elif token.type == GREATERTHAN:
                    self.eat(GREATERTHAN)
                right = self.expr()
                node = Comparison(left,token,right)

            return node 

        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = core()
            self.eat(RPAREN)
        else:
            node = core()

        return node 

    def statement_list(self):
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):

        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_compound()
        elif self.current_token.type == WHILE:
            node = self.while_compound()
        elif self.current_token.type == SKIP:
            self.eat(SKIP)
            node = self.empty()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node

    


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)

        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_While(self,node):
        while self.visit(node.boolean):
            self.visit(node.if_true)


    def visit_If(self,node):
        Bool = self.visit(node.boolean)
        if Bool is True:
            self.visit(node.if_true)
        if Bool is False:
            self.visit(node.if_false)

    def visit_Relation(self,node):
        if node.op is None:
            return self.visit(node.left)
        if node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        if node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        if node.op.type == NOT:
            return not self.visit(node.left)


    def visit_Comparison(self,node):
        if node.op == None:
            return node.left
        if node.op.type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)
        if node.op.type == LESSTHAN:
            return self.visit(node.left) < self.visit(node.right)
        if node.op.type == GREATERTHAN:
            return self.visit(node.left) > self.visit(node.right)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name, 0)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)


def main():
    import sys
    text = input()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    output_string_array = []

    for i in sorted(interpreter.GLOBAL_SCOPE.keys()):
            output_string_array.append(str(i) + ' → ' + str(interpreter.GLOBAL_SCOPE[i]))

    output = ''.join(["{", ", ".join(output_string_array), "}"])
    print(output)

if __name__ == '__main__':
    main()
