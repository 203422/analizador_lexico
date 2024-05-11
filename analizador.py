from flask import Flask, render_template, request
import ply.lex as lex

app = Flask(__name__)

tokens = ('FOR', 'IF', 'DO', 'WHILE', 'ELSE', 'LPAREN', 'RPAREN')

def t_FOR(t):
    r'\bfor\b|\bFOR\b'
    t.type = 'FOR'
    t.reserved = 'Reservada For'
    return t

def t_IF(t):
    r'\bif\b|\bIF\b'
    t.type = 'IF'
    t.reserved = 'Reservada If'
    return t

def t_DO(t):
    r'\bdo\b|\bDO\b'
    t.type = 'DO'
    t.reserved = 'Reservada Do'
    return t

def t_WHILE(t):
    r'\bwhile\b|\bWHILE\b'
    t.type = 'WHILE'
    t.reserved = 'Reservada While'
    return t

def t_ELSE(t):
    r'\belse\b|\bELSE\b'
    t.type = 'ELSE'
    t.reserved = 'Reservada Else'
    return t

def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'
    t.reserved = 'Parentesis de apertura'
    return t

def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'
    t.reserved = 'Parentesis de cierre'
    return t


t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter no valido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/text", methods=['POST'])
def text():
    if request.method == 'POST':
        code = request.form['code']
        lexer.input(code)
        line_counter = 1
        tokens = []
        for token in lexer:
            tokens.append({'type': token.type, 'value': token.value, 'line': line_counter, 'reserved': token.reserved})
            if token.value in ['(', ')']:
                line_counter += 1
            else:
                words = token.value.split()
                line_counter += len(words)
        return render_template('index.html', tokens=tokens)

@app.route("/file", methods=['POST'])
def upload_file():
        
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.txt'):
            code = file.read().decode('utf-8')
            lexer.input(code)
            line_counter = 1
            tokens = []
            for token in lexer:
                tokens.append({'type': token.type, 'value': token.value, 'line': line_counter, 'reserved': token.reserved})
                if token.value in ['(', ')']:
                    line_counter += 1
                else:
                    words = token.value.split()
                    line_counter += len(words)
            return render_template('index.html', tokens=tokens)
        else:
            return "Archivo no soportado"
    else:
        return "No se ha proporcionado el archivo"


if __name__ == '__main__':
    app.run(debug=True)
