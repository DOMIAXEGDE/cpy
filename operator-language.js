/**
 * Operator Language System
 * A Turing-complete programming language with graphical interface for the Operator System
 */

class OperatorLanguage {
    constructor(canvasId, consoleId) {
        // Language state
        this.variables = new Map(); // Variable store
        this.functions = new Map(); // Function store
        this.callStack = []; // Function call stack
        this.programCounter = 0; // Current instruction pointer
        this.program = []; // Current program
        this.running = false; // Is program running
        this.waitingForInput = false; // Is waiting for input
        this.breakpoints = new Set(); // Set of instruction numbers
        
        // Runtime configuration
        this.maxIterations = 100000; // Safety against infinite loops
        this.executionDelay = 0; // Delay between statements (ms)
        this.executionMode = 'normal'; // 'normal', 'step', 'fast'
        
        // Graphics context
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.graphicsStack = []; // For saved states
        
        // Console output
        this.consoleElement = document.getElementById(consoleId);
        this.consoleHistory = [];
        this.maxConsoleHistory = 100;
        
        // Initialize standard library
        this.initializeStandardLibrary();
    }
    
    /**
     * Initialize the standard library of functions
     */
    initializeStandardLibrary() {
        // Math operations
        this.registerNativeFunction('add', (a, b) => a + b);
        this.registerNativeFunction('sub', (a, b) => a - b);
        this.registerNativeFunction('mul', (a, b) => a * b);
        this.registerNativeFunction('div', (a, b) => a / b);
        this.registerNativeFunction('mod', (a, b) => a % b);
        this.registerNativeFunction('pow', (a, b) => Math.pow(a, b));
        this.registerNativeFunction('sqrt', (a) => Math.sqrt(a));
        this.registerNativeFunction('sin', (a) => Math.sin(a));
        this.registerNativeFunction('cos', (a) => Math.cos(a));
        this.registerNativeFunction('tan', (a) => Math.tan(a));
        this.registerNativeFunction('floor', (a) => Math.floor(a));
        this.registerNativeFunction('ceil', (a) => Math.ceil(a));
        this.registerNativeFunction('round', (a) => Math.round(a));
        this.registerNativeFunction('abs', (a) => Math.abs(a));
        this.registerNativeFunction('random', (min, max) => min + Math.random() * (max - min));
        
        // Comparison operations
        this.registerNativeFunction('eq', (a, b) => a === b);
        this.registerNativeFunction('neq', (a, b) => a !== b);
        this.registerNativeFunction('lt', (a, b) => a < b);
        this.registerNativeFunction('gt', (a, b) => a > b);
        this.registerNativeFunction('lte', (a, b) => a <= b);
        this.registerNativeFunction('gte', (a, b) => a >= b);
        this.registerNativeFunction('and', (a, b) => a && b);
        this.registerNativeFunction('or', (a, b) => a || b);
        this.registerNativeFunction('not', (a) => !a);
        
        // String operations
        this.registerNativeFunction('concat', (a, b) => String(a) + String(b));
        this.registerNativeFunction('substr', (str, start, length) => String(str).substring(start, start + length));
        this.registerNativeFunction('length', (str) => {
            if (Array.isArray(str)) {
                return str.length;
            } else if (typeof str === 'string') {
                return str.length;
            }
            return 0;
        });
        this.registerNativeFunction('tostring', (a) => String(a));
        this.registerNativeFunction('tonumber', (a) => Number(a));
        
        // Array operations
        this.registerNativeFunction('array', (...args) => args);
        this.registerNativeFunction('get', (arr, index) => {
            if (!Array.isArray(arr)) {
                throw new Error(`Expected an array, got ${typeof arr}`);
            }
            return arr[index];
        });
        this.registerNativeFunction('set', (arr, index, value) => { 
            if (!Array.isArray(arr)) {
                throw new Error(`Expected an array, got ${typeof arr}`);
            }
            const result = [...arr]; 
            result[index] = value; 
            return result; 
        });
        this.registerNativeFunction('push', (arr, value) => {
            if (!Array.isArray(arr)) {
                return [value]; // If arr is not an array, create a new array with the value
            }
            return [...arr, value];
        });
        this.registerNativeFunction('pop', (arr) => {
            if (!Array.isArray(arr) || arr.length === 0) {
                return [];
            }
            const result = [...arr];
            result.pop();
            return result;
        });
        this.registerNativeFunction('join', (arr, separator) => {
            if (!Array.isArray(arr)) {
                return String(arr);
            }
            return arr.join(separator || '');
        });
        this.registerNativeFunction('split', (str, separator) => {
            return String(str).split(separator || '');
        });
        
        // I/O operations
        this.registerNativeFunction('print', (...args) => {
            this.writeToConsole(args.join(' '));
            return args[args.length - 1];
        });
        this.registerNativeFunction('clear', () => {
            this.clearConsole();
            return null;
        });
        
        // Graphics operations
        this.registerNativeFunction('clearCanvas', (color = '#ffffff') => {
            this.ctx.fillStyle = color;
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            return null;
        });
        this.registerNativeFunction('setFillColor', (color) => {
            this.ctx.fillStyle = color;
            return color;
        });
        this.registerNativeFunction('setStrokeColor', (color) => {
            this.ctx.strokeStyle = color;
            return color;
        });
        this.registerNativeFunction('setLineWidth', (width) => {
            this.ctx.lineWidth = width;
            return width;
        });
        this.registerNativeFunction('drawRect', (x, y, width, height, fill = true) => {
            if (fill) {
                this.ctx.fillRect(x, y, width, height);
            } else {
                this.ctx.strokeRect(x, y, width, height);
            }
            return null;
        });
        this.registerNativeFunction('drawCircle', (x, y, radius, fill = true) => {
            this.ctx.beginPath();
            this.ctx.arc(x, y, radius, 0, Math.PI * 2);
            if (fill) {
                this.ctx.fill();
            } else {
                this.ctx.stroke();
            }
            return null;
        });
        this.registerNativeFunction('drawLine', (x1, y1, x2, y2) => {
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
            return null;
        });
        this.registerNativeFunction('drawText', (text, x, y, maxWidth) => {
            if (maxWidth) {
                this.ctx.fillText(text, x, y, maxWidth);
            } else {
                this.ctx.fillText(text, x, y);
            }
            return null;
        });
        this.registerNativeFunction('setFont', (font) => {
            this.ctx.font = font;
            return font;
        });
        this.registerNativeFunction('saveGraphicsState', () => {
            this.ctx.save();
            return null;
        });
        this.registerNativeFunction('restoreGraphicsState', () => {
            this.ctx.restore();
            return null;
        });
        this.registerNativeFunction('translate', (x, y) => {
            this.ctx.translate(x, y);
            return null;
        });
        this.registerNativeFunction('rotate', (angle) => {
            this.ctx.rotate(angle);
            return null;
        });
        this.registerNativeFunction('scale', (x, y) => {
            this.ctx.scale(x, y);
            return null;
        });
        
        // Time operations
        this.registerNativeFunction('delay', (ms) => {
            return new Promise(resolve => setTimeout(resolve, ms));
        });
        this.registerNativeFunction('now', () => Date.now());
        
        // System operations
        this.registerNativeFunction('getVariable', (name) => this.getVariable(name));
        this.registerNativeFunction('setVariable', (name, value) => this.setVariable(name, value));
        
        // Type checking
        this.registerNativeFunction('isNumber', (value) => typeof value === 'number');
        this.registerNativeFunction('isString', (value) => typeof value === 'string');
        this.registerNativeFunction('isArray', (value) => Array.isArray(value));
        this.registerNativeFunction('isBoolean', (value) => typeof value === 'boolean');
        this.registerNativeFunction('isNull', (value) => value === null);
        this.registerNativeFunction('isUndefined', (value) => value === undefined);
    }
    
    /**
     * Register a native JavaScript function in the language
     */
    registerNativeFunction(name, func) {
        this.functions.set(name, {
            type: 'native',
            func: func
        });
    }
    
    /**
     * Register a user-defined function
     */
    defineFunction(name, params, body) {
        this.functions.set(name, {
            type: 'user',
            params: params,
            body: body
        });
    }
    
    /**
     * Get a variable value
     */
    getVariable(name) {
        if (this.variables.has(name)) {
            return this.variables.get(name);
        }
        return null;
    }
    
    /**
     * Set a variable value
     */
    setVariable(name, value) {
        this.variables.set(name, value);
        return value;
    }
    
    /**
     * Write text to the console
     */
    writeToConsole(text) {
        if (this.consoleElement) {
            const line = document.createElement('div');
            line.className = 'console-line';
            line.textContent = text;
            this.consoleElement.appendChild(line);
            this.consoleElement.scrollTop = this.consoleElement.scrollHeight;
            
            // Limit console history
            this.consoleHistory.push(text);
            if (this.consoleHistory.length > this.maxConsoleHistory) {
                this.consoleHistory.shift();
                if (this.consoleElement.childNodes.length > this.maxConsoleHistory) {
                    this.consoleElement.removeChild(this.consoleElement.childNodes[0]);
                }
            }
        }
    }
    
    /**
     * Clear the console
     */
    clearConsole() {
        if (this.consoleElement) {
            this.consoleElement.innerHTML = '';
            this.consoleHistory = [];
        }
    }
    
    /**
     * Parse a string into a program
     * This is the main entry point for the parser
     */
    parseProgram(code) {
        const parser = new OperatorLangParser(code, this);
        return parser.parse();
    }
    
    /**
     * Load a program from a string
     */
    loadProgram(code) {
        this.program = this.parseProgram(code);
        this.programCounter = 0;
        this.running = false;
        this.callStack = [];
        return this.program;
    }
    
    /**
     * Set a breakpoint at a specific line
     */
    setBreakpoint(line) {
        this.breakpoints.add(line);
    }
    
    /**
     * Clear a breakpoint at a specific line
     */
    clearBreakpoint(line) {
        this.breakpoints.delete(line);
    }
    
    /**
     * Clear all breakpoints
     */
    clearAllBreakpoints() {
        this.breakpoints.clear();
    }
    
    /**
     * Start program execution
     */
    async run() {
        if (this.running) {
            return;
        }
        
        this.running = true;
        this.programCounter = 0;
        this.callStack = [];
        
        return this.executeProgram();
    }
    
    /**
     * Stop program execution
     */
    stop() {
        this.running = false;
    }
    
    /**
     * Execute the current program
     */
    async executeProgram() {
        let iterations = 0;
        
        while (this.running && this.programCounter < this.program.length) {
            // Check for breakpoints
            if (this.breakpoints.has(this.programCounter)) {
                this.writeToConsole(`Breakpoint hit at instruction ${this.programCounter}`);
                this.running = false;
                return;
            }
            
            // Execute the current instruction
            const instruction = this.program[this.programCounter];
            this.programCounter++;
            
            try {
                await this.executeInstruction(instruction);
            } catch (e) {
                this.writeToConsole(`Runtime error: ${e.message}`);
                this.running = false;
                return;
            }
            
            // Safety check against infinite loops
            iterations++;
            if (iterations > this.maxIterations) {
                this.writeToConsole('Program exceeded maximum iterations - stopping execution');
                this.running = false;
                return;
            }
            
            // Add delay between statements if needed
            if (this.executionDelay > 0) {
                await new Promise(resolve => setTimeout(resolve, this.executionDelay));
            }
            
            // Step mode - pause after each instruction
            if (this.executionMode === 'step') {
                this.running = false;
                return;
            }
        }
        
        if (this.programCounter >= this.program.length) {
            this.writeToConsole('Program execution completed');
            this.running = false;
        }
    }
    
    /**
     * Execute the next step of the program
     */
    async step() {
        if (this.programCounter >= this.program.length) {
            this.writeToConsole('Program execution completed');
            return;
        }
        
        this.running = true;
        const instruction = this.program[this.programCounter];
        this.programCounter++;
        
        try {
            await this.executeInstruction(instruction);
        } catch (e) {
            this.writeToConsole(`Runtime error: ${e.message}`);
        }
        
        this.running = false;
    }
    
    /**
     * Execute a single instruction
     */
    async executeInstruction(instruction) {
        switch (instruction.type) {
            case 'assign':
                const value = await this.evaluateExpression(instruction.expression);
                this.setVariable(instruction.variable, value);
                return value;
                
            case 'if':
                const condition = await this.evaluateExpression(instruction.condition);
                if (condition) {
                    // Execute the if body
                    for (const stmt of instruction.body) {
                        await this.executeInstruction(stmt);
                        if (!this.running) return;
                    }
                } else if (instruction.elseBody) {
                    // Execute the else body
                    for (const stmt of instruction.elseBody) {
                        await this.executeInstruction(stmt);
                        if (!this.running) return;
                    }
                }
                return null;
                
            case 'while':
                while (this.running) {
                    const condition = await this.evaluateExpression(instruction.condition);
                    if (!condition) break;
                    
                    for (const stmt of instruction.body) {
                        await this.executeInstruction(stmt);
                        if (!this.running) return;
                    }
                }
                return null;
                
            case 'for':
                const start = await this.evaluateExpression(instruction.start);
                const end = await this.evaluateExpression(instruction.end);
                
                for (let i = start; i < end && this.running; i++) {
                    this.setVariable(instruction.variable, i);
                    
                    for (const stmt of instruction.body) {
                        await this.executeInstruction(stmt);
                        if (!this.running) return;
                    }
                }
                return null;
                
            case 'return':
                const returnValue = await this.evaluateExpression(instruction.expression);
                return returnValue;
                
            case 'expression':
                return await this.evaluateExpression(instruction.expression);
                
            case 'end':
            case 'else':
                // These instruction types should be handled during parsing
                // They should not appear as standalone instructions during execution
                return null;
                
            default:
                throw new Error(`Unknown instruction type: ${instruction.type}`);
        }
    }
    
    /**
     * Evaluate an expression to a value
     */
    async evaluateExpression(expression) {
        switch (expression.type) {
            case 'value':
                return expression.value;
                
            case 'variable':
                return this.getVariable(expression.name);
                
            case 'call':
                const func = this.functions.get(expression.function);
                if (!func) {
                    throw new Error(`Function not found: ${expression.function}`);
                }
                
                // Evaluate all arguments
                const args = [];
                for (const arg of expression.arguments) {
                    args.push(await this.evaluateExpression(arg));
                }
                
                // Call the function
                if (func.type === 'native') {
                    return await func.func(...args);
                } else if (func.type === 'user') {
                    // Create new scope for function
                    this.callStack.push({
                        variables: new Map(this.variables),
                        programCounter: this.programCounter
                    });
                    
                    // Set up parameters
                    for (let i = 0; i < func.params.length; i++) {
                        this.setVariable(func.params[i], args[i]);
                    }
                    
                    // Execute function body
                    let result = null;
                    for (const stmt of func.body) {
                        result = await this.executeInstruction(stmt);
                        if (!this.running) break;
                        if (stmt.type === 'return') break;
                    }
                    
                    // Restore original scope
                    const callFrame = this.callStack.pop();
                    this.variables = callFrame.variables;
                    this.programCounter = callFrame.programCounter;
                    
                    return result;
                }
                break;
                
            case 'binary':
                const left = await this.evaluateExpression(expression.left);
                const right = await this.evaluateExpression(expression.right);
                
                switch (expression.operator) {
                    case '+': return left + right;
                    case '-': return left - right;
                    case '*': return left * right;
                    case '/': return left / right;
                    case '%': return left % right;
                    case '==': return left === right;
                    case '!=': return left !== right;
                    case '<': return left < right;
                    case '>': return left > right;
                    case '<=': return left <= right;
                    case '>=': return left >= right;
                    case '&&': return left && right;
                    case '||': return left || right;
                    default:
                        throw new Error(`Unknown binary operator: ${expression.operator}`);
                }
                
            case 'unary':
                const value = await this.evaluateExpression(expression.expression);
                
                switch (expression.operator) {
                    case '!': return !value;
                    case '-': return -value;
                    default:
                        throw new Error(`Unknown unary operator: ${expression.operator}`);
                }
                
            case 'array':
                const elements = [];
                for (const element of expression.elements) {
                    elements.push(await this.evaluateExpression(element));
                }
                return elements;
                
            case 'object':
                const obj = {};
                for (const key in expression.properties) {
                    obj[key] = await this.evaluateExpression(expression.properties[key]);
                }
                return obj;
                
            default:
                throw new Error(`Unknown expression type: ${expression.type}`);
        }
    }
    
    /**
     * Save the program as JSON
     */
    exportToJSON() {
        return JSON.stringify({
            program: this.program,
            variables: Array.from(this.variables.entries()),
            functions: Array.from(this.functions.entries())
                .filter(([_, func]) => func.type === 'user')
                .map(([name, func]) => ({
                    name,
                    params: func.params,
                    body: func.body
                })),
            breakpoints: Array.from(this.breakpoints),
            version: '1.0'
        }, null, 2);
    }
    
    /**
     * Load a program from JSON
     */
    importFromJSON(json) {
        try {
            const data = JSON.parse(json);
            
            // Check version
            if (!data.version || data.version !== '1.0') {
                throw new Error('Incompatible program version');
            }
            
            // Load program
            this.program = data.program;
            
            // Load variables
            this.variables = new Map(data.variables);
            
            // Load user-defined functions
            for (const func of data.functions) {
                this.defineFunction(func.name, func.params, func.body);
            }
            
            // Load breakpoints
            this.breakpoints = new Set(data.breakpoints);
            
            // Reset state
            this.programCounter = 0;
            this.running = false;
            this.callStack = [];
            
            return true;
        } catch (e) {
            this.writeToConsole(`Error importing program: ${e.message}`);
            return false;
        }
    }
}

/**
 * TokenType enum for the lexer
 */
const TokenType = {
    // Literals
    NUMBER: 'NUMBER',
    STRING: 'STRING',
    IDENTIFIER: 'IDENTIFIER',
    TRUE: 'TRUE',
    FALSE: 'FALSE',
    NULL: 'NULL',
    
    // Keywords
    IF: 'IF',
    ELSE: 'ELSE',
    WHILE: 'WHILE',
    FOR: 'FOR',
    IN: 'IN',
    RANGE: 'RANGE',
    FUNC: 'FUNC',
    RETURN: 'RETURN',
    LET: 'LET',
    CONTINUE: 'CONTINUE',
    BREAK: 'BREAK',
    
    // Operators
    PLUS: 'PLUS',
    MINUS: 'MINUS',
    TIMES: 'TIMES',
    DIVIDE: 'DIVIDE',
    MODULO: 'MODULO',
    POWER: 'POWER',
    
    // Comparison operators
    EQUAL: 'EQUAL',
    NOT_EQUAL: 'NOT_EQUAL',
    LESS: 'LESS',
    GREATER: 'GREATER',
    LESS_EQUAL: 'LESS_EQUAL',
    GREATER_EQUAL: 'GREATER_EQUAL',
    
    // Logical operators
    AND: 'AND',
    OR: 'OR',
    NOT: 'NOT',
    
    // Assignment
    ASSIGN: 'ASSIGN',
    
    // Delimiters
    LPAREN: 'LPAREN',
    RPAREN: 'RPAREN',
    LBRACE: 'LBRACE',
    RBRACE: 'RBRACE',
    LBRACKET: 'LBRACKET',
    RBRACKET: 'RBRACKET',
    COMMA: 'COMMA',
    DOT: 'DOT',
    COLON: 'COLON',
    SEMICOLON: 'SEMICOLON',
    
    // End of file
    EOF: 'EOF'
};

/**
 * Token class for the lexer
 */
class Token {
    constructor(type, value, line, column) {
        this.type = type;
        this.value = value;
        this.line = line;
        this.column = column;
    }
    
    toString() {
        return `Token(${this.type}, ${this.value})`;
    }
}

/**
 * Lexer class for tokenizing the input code
 */
class Lexer {
    constructor(source) {
        this.source = source;
        this.position = 0;
        this.line = 1;
        this.column = 1;
        this.tokens = [];
        
        this.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'range': TokenType.RANGE,
            'func': TokenType.FUNC,
            'return': TokenType.RETURN,
            'let': TokenType.LET,
            'continue': TokenType.CONTINUE,
            'break': TokenType.BREAK,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'null': TokenType.NULL
        };
    }
    
    /**
     * Get the current character
     */
    currentChar() {
        if (this.position >= this.source.length) {
            return null;
        }
        return this.source[this.position];
    }
    
    /**
     * Look ahead at the next character without advancing the position
     */
    peekChar() {
        if (this.position + 1 >= this.source.length) {
            return null;
        }
        return this.source[this.position + 1];
    }
    
    /**
     * Advance to the next character
     */
    advance() {
        if (this.currentChar() === '\n') {
            this.line++;
            this.column = 1;
        } else {
            this.column++;
        }
        this.position++;
    }
    
    /**
     * Skip whitespace
     */
    skipWhitespace() {
        while (this.currentChar() && /\s/.test(this.currentChar())) {
            this.advance();
        }
    }
    
    /**
     * Skip a comment (everything from # to the end of the line)
     */
    skipComment() {
        while (this.currentChar() && this.currentChar() !== '\n') {
            this.advance();
        }
        if (this.currentChar() === '\n') {
            this.advance();
        }
    }
    
    /**
     * Tokenize a number
     */
    tokenizeNumber() {
        let start = this.position;
        let startColumn = this.column;
        let hasDot = false;
        
        while (this.currentChar() && /[0-9.]/.test(this.currentChar())) {
            if (this.currentChar() === '.') {
                if (hasDot) {
                    break;
                }
                hasDot = true;
            }
            this.advance();
        }
        
        let value = this.source.substring(start, this.position);
        return new Token(TokenType.NUMBER, parseFloat(value), this.line, startColumn);
    }
    
    /**
     * Tokenize a string
     */
    tokenizeString(quoteChar) {
        let start = this.position;
        let startColumn = this.column;
        let value = '';
        
        // Skip the opening quote
        this.advance();
        
        while (this.currentChar() && this.currentChar() !== quoteChar) {
            // Handle escape sequences
            if (this.currentChar() === '\\') {
                this.advance();
                if (this.currentChar() === 'n') {
                    value += '\n';
                } else if (this.currentChar() === 't') {
                    value += '\t';
                } else if (this.currentChar() === 'r') {
                    value += '\r';
                } else if (this.currentChar() === quoteChar) {
                    value += quoteChar;
                } else if (this.currentChar() === '\\') {
                    value += '\\';
                } else {
                    value += this.currentChar();
                }
            } else {
                value += this.currentChar();
            }
            this.advance();
        }
        
        // Skip the closing quote
        if (this.currentChar() === quoteChar) {
            this.advance();
        }
        
        return new Token(TokenType.STRING, value, this.line, startColumn);
    }
    
    /**
     * Tokenize an identifier or keyword
     */
    tokenizeIdentifier() {
        let start = this.position;
        let startColumn = this.column;
        
        while (this.currentChar() && /[A-Za-z0-9_]/.test(this.currentChar())) {
            this.advance();
        }
        
        let value = this.source.substring(start, this.position);
        
        // Check if it's a keyword
        let tokenType = this.keywords[value] || TokenType.IDENTIFIER;
        
        return new Token(tokenType, value, this.line, startColumn);
    }
    
    /**
     * Tokenize the input code
     */
    tokenize() {
        while (this.position < this.source.length) {
            // Skip whitespace
            if (/\s/.test(this.currentChar())) {
                this.skipWhitespace();
                continue;
            }
            
            // Skip comments
            if (this.currentChar() === '#') {
                this.skipComment();
                continue;
            }
            
            // Numbers
            if (/[0-9]/.test(this.currentChar())) {
                this.tokens.push(this.tokenizeNumber());
                continue;
            }
            
            // Strings
            if (this.currentChar() === '"' || this.currentChar() === "'") {
                this.tokens.push(this.tokenizeString(this.currentChar()));
                continue;
            }
            
            // Identifiers and keywords
            if (/[A-Za-z_]/.test(this.currentChar())) {
                this.tokens.push(this.tokenizeIdentifier());
                continue;
            }
            
            // Operators and punctuation
            switch (this.currentChar()) {
                case '+':
                    this.tokens.push(new Token(TokenType.PLUS, '+', this.line, this.column));
                    this.advance();
                    break;
                case '-':
                    this.tokens.push(new Token(TokenType.MINUS, '-', this.line, this.column));
                    this.advance();
                    break;
                case '*':
                    this.tokens.push(new Token(TokenType.TIMES, '*', this.line, this.column));
                    this.advance();
                    break;
                case '/':
                    this.tokens.push(new Token(TokenType.DIVIDE, '/', this.line, this.column));
                    this.advance();
                    break;
                case '%':
                    this.tokens.push(new Token(TokenType.MODULO, '%', this.line, this.column));
                    this.advance();
                    break;
                case '=':
                    if (this.peekChar() === '=') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.EQUAL, '==', this.line, this.column - 2));
                    } else {
                        this.advance();
                        this.tokens.push(new Token(TokenType.ASSIGN, '=', this.line, this.column - 1));
                    }
                    break;
                case '!':
                    if (this.peekChar() === '=') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.NOT_EQUAL, '!=', this.line, this.column - 2));
                    } else {
                        this.advance();
                        this.tokens.push(new Token(TokenType.NOT, '!', this.line, this.column - 1));
                    }
                    break;
                case '<':
                    if (this.peekChar() === '=') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.LESS_EQUAL, '<=', this.line, this.column - 2));
                    } else {
                        this.advance();
                        this.tokens.push(new Token(TokenType.LESS, '<', this.line, this.column - 1));
                    }
                    break;
                case '>':
                    if (this.peekChar() === '=') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.GREATER_EQUAL, '>=', this.line, this.column - 2));
                    } else {
                        this.advance();
                        this.tokens.push(new Token(TokenType.GREATER, '>', this.line, this.column - 1));
                    }
                    break;
                case '&':
                    if (this.peekChar() === '&') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.AND, '&&', this.line, this.column - 2));
                    } else {
                        throw new Error(`Unexpected character '&' at line ${this.line}, column ${this.column}`);
                    }
                    break;
                case '|':
                    if (this.peekChar() === '|') {
                        this.advance();
                        this.advance();
                        this.tokens.push(new Token(TokenType.OR, '||', this.line, this.column - 2));
                    } else {
                        throw new Error(`Unexpected character '|' at line ${this.line}, column ${this.column}`);
                    }
                    break;
                case '(':
                    this.tokens.push(new Token(TokenType.LPAREN, '(', this.line, this.column));
                    this.advance();
                    break;
                case ')':
                    this.tokens.push(new Token(TokenType.RPAREN, ')', this.line, this.column));
                    this.advance();
                    break;
                case '{':
                    this.tokens.push(new Token(TokenType.LBRACE, '{', this.line, this.column));
                    this.advance();
                    break;
                case '}':
                    this.tokens.push(new Token(TokenType.RBRACE, '}', this.line, this.column));
                    this.advance();
                    break;
                case '[':
                    this.tokens.push(new Token(TokenType.LBRACKET, '[', this.line, this.column));
                    this.advance();
                    break;
                case ']':
                    this.tokens.push(new Token(TokenType.RBRACKET, ']', this.line, this.column));
                    this.advance();
                    break;
                case ',':
                    this.tokens.push(new Token(TokenType.COMMA, ',', this.line, this.column));
                    this.advance();
                    break;
                case '.':
                    this.tokens.push(new Token(TokenType.DOT, '.', this.line, this.column));
                    this.advance();
                    break;
                case ':':
                    this.tokens.push(new Token(TokenType.COLON, ':', this.line, this.column));
                    this.advance();
                    break;
                case ';':
                    this.tokens.push(new Token(TokenType.SEMICOLON, ';', this.line, this.column));
                    this.advance();
                    break;
                default:
                    throw new Error(`Unexpected character '${this.currentChar()}' at line ${this.line}, column ${this.column}`);
            }
        }
        
        // End of file
        this.tokens.push(new Token(TokenType.EOF, null, this.line, this.column));
        
        return this.tokens;
    }
}

/**
 * Parser class for parsing tokens into an AST
 */
class Parser {
    constructor(tokens) {
        this.tokens = tokens;
        this.position = 0;
    }
    
    /**
     * Get the current token
     */
    currentToken() {
        if (this.position >= this.tokens.length) {
            return this.tokens[this.tokens.length - 1]; // Return EOF token
        }
        return this.tokens[this.position];
    }
    
    /**
     * Look ahead at the next token without advancing the position
     */
    peekToken() {
        if (this.position + 1 >= this.tokens.length) {
            return this.tokens[this.tokens.length - 1]; // Return EOF token
        }
        return this.tokens[this.position + 1];
    }
    
    /**
     * Advance to the next token
     */
    advance() {
        this.position++;
    }
    
    /**
     * Check if the current token is of the given type
     */
    check(type) {
        return this.currentToken().type === type;
    }
    
    /**
     * Consume a token of the given type and advance
     */
    consume(type, errorMessage) {
        if (this.check(type)) {
            const token = this.currentToken();
            this.advance();
            return token;
        }
        
        throw new Error(`${errorMessage} at line ${this.currentToken().line}, column ${this.currentToken().column}`);
    }
    
    /**
     * Parse the program
     */
    parse() {
        const statements = [];
        
        while (!this.check(TokenType.EOF)) {
            statements.push(this.parseStatement());
        }
        
        return statements;
    }
    
    /**
     * Parse a statement
     */
    parseStatement() {
        // Variable declaration with 'let'
        if (this.check(TokenType.LET)) {
            return this.parseVariableDeclaration();
        }
        
        // If statement
        if (this.check(TokenType.IF)) {
            return this.parseIfStatement();
        }
        
        // While loop
        if (this.check(TokenType.WHILE)) {
            return this.parseWhileLoop();
        }
        
        // For loop
        if (this.check(TokenType.FOR)) {
            return this.parseForLoop();
        }
        
        // Function declaration
        if (this.check(TokenType.FUNC)) {
            return this.parseFunctionDeclaration();
        }
        
        // Return statement
        if (this.check(TokenType.RETURN)) {
            return this.parseReturnStatement();
        }
        
        // Assignment (variable = expression)
        if (this.check(TokenType.IDENTIFIER) && this.peekToken().type === TokenType.ASSIGN) {
            return this.parseAssignment();
        }
        
        // Expression statement
        return this.parseExpressionStatement();
    }
    
    /**
     * Parse a variable declaration (let x = expr)
     */
    parseVariableDeclaration() {
        this.consume(TokenType.LET, "Expected 'let'");
        const name = this.consume(TokenType.IDENTIFIER, "Expected variable name").value;
        this.consume(TokenType.ASSIGN, "Expected '=' after variable name");
        const expression = this.parseExpression();
        
        return {
            type: 'assign',
            variable: name,
            expression: expression
        };
    }
    
    /**
     * Parse an assignment (x = expr)
     */
    parseAssignment() {
        const name = this.consume(TokenType.IDENTIFIER, "Expected variable name").value;
        this.consume(TokenType.ASSIGN, "Expected '=' after variable name");
        const expression = this.parseExpression();
        
        return {
            type: 'assign',
            variable: name,
            expression: expression
        };
    }
    
    /**
     * Parse an if statement (if expr { ... } else { ... })
     */
    parseIfStatement() {
        this.consume(TokenType.IF, "Expected 'if'");
        const condition = this.parseExpression();
        
        this.consume(TokenType.LBRACE, "Expected '{' after if condition");
        const body = this.parseBlock();
        
        let elseBody = null;
        
        // Check for else block
        if (this.check(TokenType.ELSE)) {
            this.advance();
            this.consume(TokenType.LBRACE, "Expected '{' after 'else'");
            elseBody = this.parseBlock();
        }
        
        return {
            type: 'if',
            condition: condition,
            body: body,
            elseBody: elseBody
        };
    }
    
    /**
     * Parse a while loop (while expr { ... })
     */
    parseWhileLoop() {
        this.consume(TokenType.WHILE, "Expected 'while'");
        const condition = this.parseExpression();
        
        this.consume(TokenType.LBRACE, "Expected '{' after while condition");
        const body = this.parseBlock();
        
        return {
            type: 'while',
            condition: condition,
            body: body
        };
    }
    
    /**
     * Parse a for loop (for i in range(start, end) { ... })
     */
    parseForLoop() {
        this.consume(TokenType.FOR, "Expected 'for'");
        const variable = this.consume(TokenType.IDENTIFIER, "Expected variable name").value;
        
        this.consume(TokenType.IN, "Expected 'in'");
        this.consume(TokenType.RANGE, "Expected 'range'");
        this.consume(TokenType.LPAREN, "Expected '(' after 'range'");
        
        const start = this.parseExpression();
        this.consume(TokenType.COMMA, "Expected ',' between range values");
        const end = this.parseExpression();
        
        this.consume(TokenType.RPAREN, "Expected ')' after range values");
        this.consume(TokenType.LBRACE, "Expected '{' after for loop header");
        
        const body = this.parseBlock();
        
        return {
            type: 'for',
            variable: variable,
            start: start,
            end: end,
            body: body
        };
    }
    
    /**
     * Parse a function declaration (func name(params) { ... })
     */
    parseFunctionDeclaration() {
        this.consume(TokenType.FUNC, "Expected 'func'");
        const name = this.consume(TokenType.IDENTIFIER, "Expected function name").value;
        
        this.consume(TokenType.LPAREN, "Expected '(' after function name");
        const params = this.parseParameters();
        this.consume(TokenType.RPAREN, "Expected ')' after parameters");
        
        this.consume(TokenType.LBRACE, "Expected '{' after function parameters");
        const body = this.parseBlock();
        
        return {
            type: 'function',
            name: name,
            params: params,
            body: body
        };
    }
    
    /**
     * Parse function parameters
     */
    parseParameters() {
        const params = [];
        
        // Empty parameter list
        if (this.check(TokenType.RPAREN)) {
            return params;
        }
        
        // Parse first parameter
        params.push(this.consume(TokenType.IDENTIFIER, "Expected parameter name").value);
        
        // Parse remaining parameters
        while (this.check(TokenType.COMMA)) {
            this.advance();
            params.push(this.consume(TokenType.IDENTIFIER, "Expected parameter name").value);
        }
        
        return params;
    }
    
    /**
     * Parse a block of statements
     */
    parseBlock() {
        const statements = [];
        
        while (!this.check(TokenType.RBRACE) && !this.check(TokenType.EOF)) {
            statements.push(this.parseStatement());
        }
        
        this.consume(TokenType.RBRACE, "Expected '}'");
        
        return statements;
    }
    
    /**
     * Parse a return statement
     */
    parseReturnStatement() {
        this.consume(TokenType.RETURN, "Expected 'return'");
        const expression = this.parseExpression();
        
        return {
            type: 'return',
            expression: expression
        };
    }
    
    /**
     * Parse an expression statement
     */
    parseExpressionStatement() {
        const expression = this.parseExpression();
        
        return {
            type: 'expression',
            expression: expression
        };
    }
    
    /**
     * Parse an expression
     */
    parseExpression() {
        return this.parseLogicalOr();
    }
    
    /**
     * Parse logical OR expressions
     */
    parseLogicalOr() {
        let expr = this.parseLogicalAnd();
        
        while (this.check(TokenType.OR)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseLogicalAnd();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse logical AND expressions
     */
    parseLogicalAnd() {
        let expr = this.parseEquality();
        
        while (this.check(TokenType.AND)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseEquality();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse equality expressions (==, !=)
     */
    parseEquality() {
        let expr = this.parseComparison();
        
        while (this.check(TokenType.EQUAL) || this.check(TokenType.NOT_EQUAL)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseComparison();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse comparison expressions (<, >, <=, >=)
     */
    parseComparison() {
        let expr = this.parseAddition();
        
        while (
            this.check(TokenType.LESS) || 
            this.check(TokenType.GREATER) || 
            this.check(TokenType.LESS_EQUAL) || 
            this.check(TokenType.GREATER_EQUAL)
        ) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseAddition();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse addition and subtraction
     */
    parseAddition() {
        let expr = this.parseMultiplication();
        
        while (this.check(TokenType.PLUS) || this.check(TokenType.MINUS)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseMultiplication();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse multiplication, division, and modulo
     */
    parseMultiplication() {
        let expr = this.parseUnary();
        
        while (
            this.check(TokenType.TIMES) || 
            this.check(TokenType.DIVIDE) || 
            this.check(TokenType.MODULO)
        ) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseUnary();
            
            expr = {
                type: 'binary',
                operator: operator,
                left: expr,
                right: right
            };
        }
        
        return expr;
    }
    
    /**
     * Parse unary expressions (!, -)
     */
    parseUnary() {
        if (this.check(TokenType.NOT) || this.check(TokenType.MINUS)) {
            const operator = this.currentToken().value;
            this.advance();
            const right = this.parseUnary();
            
            return {
                type: 'unary',
                operator: operator,
                expression: right
            };
        }
        
        return this.parseCallOrPrimary();
    }
    
    /**
     * Parse function calls or primary expressions
     */
    parseCallOrPrimary() {
        // Parse the primary expression first
        let expr = this.parsePrimary();
        
        // If followed by '(', it's a function call
        while (this.check(TokenType.LPAREN)) {
            expr = this.parseCall(expr);
        }
        
        return expr;
    }
    
    /**
     * Parse function call
     */
    parseCall(callee) {
        // Function name must be an identifier
        if (callee.type !== 'variable') {
            throw new Error("Expected function name");
        }
        
        this.consume(TokenType.LPAREN, "Expected '(' after function name");
        const args = this.parseArguments();
        this.consume(TokenType.RPAREN, "Expected ')' after arguments");
        
        return {
            type: 'call',
            function: callee.name,
            arguments: args
        };
    }
    
    /**
     * Parse function call arguments
     */
    parseArguments() {
        const args = [];
        
        // Empty argument list
        if (this.check(TokenType.RPAREN)) {
            return args;
        }
        
        // Parse first argument
        args.push(this.parseExpression());
        
        // Parse remaining arguments
        while (this.check(TokenType.COMMA)) {
            this.advance();
            args.push(this.parseExpression());
        }
        
        return args;
    }
    
    /**
     * Parse primary expressions (literals, identifiers, parenthesized expressions)
     */
    parsePrimary() {
        // Number literal
        if (this.check(TokenType.NUMBER)) {
            const value = this.currentToken().value;
            this.advance();
            return {
                type: 'value',
                value: value
            };
        }
        
        // String literal
        if (this.check(TokenType.STRING)) {
            const value = this.currentToken().value;
            this.advance();
            return {
                type: 'value',
                value: value
            };
        }
        
        // Boolean literals
        if (this.check(TokenType.TRUE)) {
            this.advance();
            return {
                type: 'value',
                value: true
            };
        }
        
        if (this.check(TokenType.FALSE)) {
            this.advance();
            return {
                type: 'value',
                value: false
            };
        }
        
        // Null literal
        if (this.check(TokenType.NULL)) {
            this.advance();
            return {
                type: 'value',
                value: null
            };
        }
        
        // Identifier
        if (this.check(TokenType.IDENTIFIER)) {
            const name = this.currentToken().value;
            this.advance();
            return {
                type: 'variable',
                name: name
            };
        }
        
        // Array literal
        if (this.check(TokenType.LBRACKET)) {
            return this.parseArrayLiteral();
        }
        
        // Parenthesized expression
        if (this.check(TokenType.LPAREN)) {
            this.advance();
            const expr = this.parseExpression();
            this.consume(TokenType.RPAREN, "Expected ')' after expression");
            return expr;
        }
        
        throw new Error(`Unexpected token ${this.currentToken().type} at line ${this.currentToken().line}, column ${this.currentToken().column}`);
    }
    
    /**
     * Parse array literal
     */
    parseArrayLiteral() {
        this.consume(TokenType.LBRACKET, "Expected '['");
        const elements = [];
        
        // Empty array
        if (this.check(TokenType.RBRACKET)) {
            this.advance();
            return {
                type: 'array',
                elements: elements
            };
        }
        
        // Parse first element
        elements.push(this.parseExpression());
        
        // Parse remaining elements
        while (this.check(TokenType.COMMA)) {
            this.advance();
            elements.push(this.parseExpression());
        }
        
        this.consume(TokenType.RBRACKET, "Expected ']'");
        
        return {
            type: 'array',
            elements: elements
        };
    }
}

/**
 * Main parser class for OperatorLang
 */
class OperatorLangParser {
    constructor(code, context) {
        this.code = code;
        this.context = context;
    }
    
    /**
     * Parse the code into a program
     */
    parse() {
        try {
            // Tokenize the input
            const lexer = new Lexer(this.code);
            const tokens = lexer.tokenize();
            
            // Parse the tokens into an AST
            const parser = new Parser(tokens);
            const program = parser.parse();
            
            // Process function declarations
            this.processFunctionDeclarations(program);
            
            // Return the program without function declarations
            return program.filter(statement => statement.type !== 'function');
        } catch (e) {
            this.context.writeToConsole(`Parse error: ${e.message}`);
            throw e;
        }
    }
    
    /**
     * Process function declarations
     */
    processFunctionDeclarations(program) {
        for (const statement of program) {
            if (statement.type === 'function') {
                this.context.defineFunction(statement.name, statement.params, statement.body);
            }
        }
    }
}

// Example programs
const EXAMPLE_PROGRAMS = {
    helloWorld: `# Hello world program
print("Hello, world!")
`,

    drawingDemo: `# Graphics demo program
clearCanvas("#f0f0f0")

# Draw a colorful pattern
let size = 20
let colors = array("#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff")

for i in range(0, 10) {
    for j in range(0, 10) {
        let x = i * 30 + 50
        let y = j * 30 + 50
        let colorIndex = (i + j) % 6
        setFillColor(get(colors, colorIndex))
        drawRect(x, y, size, size)
    }
}

# Draw a rainbow arc
setLineWidth(5)
let cx = 200
let cy = 200
let radius = 100
let colors2 = array("#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#9400d3")

for i in range(0, 7) {
    let r = radius - i * 10
    setStrokeColor(get(colors2, i))
    drawCircle(cx, cy, r, false)
}

# Draw some text
setFillColor("#000000")
setFont("20px Arial")
drawText("Operator Graphics Demo", 120, 350)
`,

    fibonacci: `# Calculate Fibonacci sequence
# Iterative implementation to avoid recursion issues

print("Fibonacci Sequence:")

# Initialize first two Fibonacci numbers
let a = 0
let b = 1

# Calculate and display the first 10 Fibonacci numbers
for i in range(0, 10) {
    # Use separate if statements instead of else if
    if i == 0 {
        print("fibonacci(0) = 0")
    }
    
    if i == 1 {
        print("fibonacci(1) = 1") 
    }
    
    if i > 1 {
        # Calculate the next Fibonacci number
        let c = a + b
        
        # Update a and b for the next iteration
        a = b
        b = c
        
        # Print the result
        print("fibonacci(" + i + ") = " + c)
    }
}

print("Fibonacci sequence completed")
`,

    gameOfLife: `# Conway's Game of Life - Simplified Version
# This implementation uses a flat 1D array instead of nested arrays

# Grid dimensions
let width = 20
let height = 15
let cellSize = 15

# Debug output
func debug(message) {
    print("DEBUG: " + message)
}

# Convert 2D coordinates to 1D index
func coordToIndex(x, y) {
    return y * width + x
}

# Initialize a random grid
func createGrid() {
    debug("Creating grid...")
    
    # Create a flat array for the grid
    let grid = array()
    
    # Fill with random cells
    for i in range(0, width * height) {
        let state = 0
        if random(0, 1) < 0.3 {
            state = 1
        }
        grid = push(grid, state)
    }
    
    debug("Grid created with " + length(grid) + " cells")
    return grid
}

# Get cell state
func getCell(grid, x, y) {
    # Check bounds
    if x < 0 {
        return 0
    }
    
    if x >= width {
        return 0
    }
    
    if y < 0 {
        return 0
    }
    
    if y >= height {
        return 0
    }
    
    # Get index
    let index = coordToIndex(x, y)
    
    # Check if grid and index are valid
    if grid == null {
        return 0
    }
    
    # Get the cell value
    let cell = get(grid, index)
    
    # Return 0 if cell is not defined
    if cell == null {
        return 0
    }
    
    return cell
}

# Count neighbors
func countNeighbors(grid, x, y) {
    let count = 0
    
    # Check all 8 surrounding cells
    for dy in range(-1, 2) {
        for dx in range(-1, 2) {
            # Skip the cell itself (when dx=0 and dy=0)
            # We'll handle this with an if statement instead of continue
            if dx != 0 || dy != 0 {
                # Add to count if neighbor is alive
                let nx = x + dx
                let ny = y + dy
                
                if getCell(grid, nx, ny) == 1 {
                    count = count + 1
                }
            }
        }
    }
    
    return count
}

# Compute next generation
func nextGeneration(grid) {
    debug("Computing next generation...")
    
    # Create new grid
    let newGrid = array()
    
    # Initialize with all dead cells
    for i in range(0, width * height) {
        newGrid = push(newGrid, 0)
    }
    
    # Apply rules to each cell
    for y in range(0, height) {
        for x in range(0, width) {
            # Get current state
            let state = getCell(grid, x, y)
            
            # Count neighbors
            let neighbors = countNeighbors(grid, x, y)
            
            # Index in the flat array
            let index = coordToIndex(x, y)
            
            # Apply Conway's rules
            let newState = 0
            
            # Rule 1: Live cell with 2-3 neighbors survives
            if state == 1 {
                if neighbors == 2 {
                    newState = 1
                }
                
                if neighbors == 3 {
                    newState = 1
                }
            }
            
            # Rule 2: Dead cell with 3 neighbors becomes alive
            if state == 0 {
                if neighbors == 3 {
                    newState = 1
                }
            }
            
            # Update the new grid
            newGrid = set(newGrid, index, newState)
        }
    }
    
    debug("Next generation computed")
    return newGrid
}

# Draw the grid
func drawGrid(grid) {
    debug("Drawing grid...")
    
    # Clear the canvas
    clearCanvas("#f0f0f0")
    
    # Draw each cell
    for y in range(0, height) {
        for x in range(0, width) {
            # Get cell state
            let state = getCell(grid, x, y)
            
            # Set color based on state
            if state == 1 {
                setFillColor("#000000")  # Black for alive
            } else {
                setFillColor("#ffffff")  # White for dead
            }
            
            # Draw the cell
            drawRect(x * cellSize + 1, y * cellSize + 1, 
                    cellSize - 2, cellSize - 2)
        }
    }
    
    # Draw grid lines
    setStrokeColor("#cccccc")
    setLineWidth(1)
    
    # Vertical lines
    for x in range(0, width + 1) {
        drawLine(x * cellSize, 0, x * cellSize, height * cellSize)
    }
    
    # Horizontal lines
    for y in range(0, height + 1) {
        drawLine(0, y * cellSize, width * cellSize, y * cellSize)
    }
    
    debug("Grid drawn")
}

# Start simulation
print("Conway's Game of Life")
print("Initializing...")

# Create and draw initial grid
let grid = createGrid()
drawGrid(grid)

print("Simulation running...")
print("Press 'Run' again to stop")

# Animation loop
while true {
    # Update grid
    grid = nextGeneration(grid)
    
    # Draw updated grid
    drawGrid(grid)
    
    # Delay for animation
    delay(200)
}
`
};

// Set up the OperatorLanguage UI with the Operator System
document.addEventListener('DOMContentLoaded', function() {
    // Add the programming language section to the main UI
    const mainElement = document.querySelector('main');
    
    if (!mainElement) {
        console.error('Main element not found in the document');
        return;
    }
    
    // Create programming language section
    const programmingSection = document.createElement('section');
    programmingSection.id = 'programming-section';
    programmingSection.className = 'operation-section';
    programmingSection.innerHTML = `
        <h2>Programmable Interface</h2>
        <div class="operation-container">
            <div class="operation-controls">
                <h3>OperatorLang Code</h3>
                <textarea id="code-editor" spellcheck="false"></textarea>
                <div class="editor-toolbar">
                    <button id="run-program" class="button">Run</button>
                    <button id="stop-program" class="button button-secondary">Stop</button>
                    <button id="step-program" class="button">Step</button>
                    <button id="clear-program" class="button button-secondary">Clear</button>
                    <select id="example-programs">
                        <option value="">Load Example...</option>
                        <option value="helloWorld">Hello World</option>
                        <option value="drawingDemo">Drawing Demo</option>
                        <option value="fibonacci">Fibonacci Sequence</option>
                        <option value="gameOfLife">Game of Life</option>
                    </select>
                </div>
                <div class="language-console-container">
                    <h3>Console Output</h3>
                    <div id="language-console" class="language-console"></div>
                </div>
            </div>
            <div class="operation-result">
                <h3>Graphics Output</h3>
                <canvas id="language-canvas" width="400" height="400"></canvas>
                <div class="program-controls">
                    <button id="save-program" class="button">Save Program</button>
                    <button id="load-program" class="button">Load Program</button>
                    <button id="download-canvas" class="button">Download Image</button>
                </div>
            </div>
        </div>
    `;
    
    // Add programming section to the main UI
    mainElement.appendChild(programmingSection);
    
    // Add it to navigation
    const navSection = document.querySelector('#main-nav');
    if (navSection) {
        const programmingNav = document.createElement('div');
        programmingNav.className = 'nav-section';
        programmingNav.innerHTML = `
            <h3>Programming</h3>
            <button data-section="programming-section">OperatorLang</button>
        `;
        navSection.appendChild(programmingNav);
    }
    
    // Add the styles
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        #code-editor {
            width: 100%;
            height: 300px;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            padding: 10px;
            border: 1px solid var(--secondary-color);
            resize: vertical;
            tab-size: 4;
            white-space: pre;
            overflow-wrap: normal;
            overflow-x: auto;
        }
        
        .editor-toolbar {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .language-console {
            background-color: var(--terminal-bg);
            color: var(--terminal-text);
            height: 150px;
            overflow-y: auto;
            padding: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
            margin-top: 10px;
            border: 1px solid var(--secondary-color);
        }
        
        .language-console-container {
            margin-top: 15px;
        }
        
        #language-canvas {
            border: 1px solid var(--secondary-color);
            background-color: white;
            width: 100%;
            height: 400px;
            max-width: 400px;
        }
        
        .program-controls {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .console-line {
            margin-bottom: 5px;
            word-wrap: break-word;
        }
    `;
    document.head.appendChild(styleElement);
    
    // Initialize the language
    const lang = new OperatorLanguage('language-canvas', 'language-console');
    window.operatorLang = lang; // Make it globally accessible
    
    // Set up event listeners
    const codeEditor = document.getElementById('code-editor');
    const runButton = document.getElementById('run-program');
    const stopButton = document.getElementById('stop-program');
    const stepButton = document.getElementById('step-program');
    const clearButton = document.getElementById('clear-program');
    const exampleSelect = document.getElementById('example-programs');
    const saveButton = document.getElementById('save-program');
    const loadButton = document.getElementById('load-program');
    const downloadButton = document.getElementById('download-canvas');
    
    if (!codeEditor || !runButton || !stopButton || !stepButton || !clearButton || 
        !exampleSelect || !saveButton || !loadButton || !downloadButton) {
        console.error('One or more UI elements not found');
        return;
    }
    
    // Run program
    runButton.addEventListener('click', function() {
        if (lang.running) {
            lang.stop();
            runButton.textContent = 'Run';
        } else {
            const code = codeEditor.value;
            try {
                lang.loadProgram(code);
                lang.run();
                runButton.textContent = 'Pause';
            } catch (error) {
                lang.writeToConsole(`Error loading program: ${error.message}`);
            }
        }
    });
    
    // Stop program
    stopButton.addEventListener('click', function() {
        lang.stop();
        runButton.textContent = 'Run';
    });
    
    // Step program
    stepButton.addEventListener('click', function() {
        const code = codeEditor.value;
        if (lang.program.length === 0) {
            try {
                lang.loadProgram(code);
            } catch (error) {
                lang.writeToConsole(`Error loading program: ${error.message}`);
                return;
            }
        }
        lang.step();
    });
    
    // Clear program
    clearButton.addEventListener('click', function() {
        if (confirm('Clear the code editor?')) {
            codeEditor.value = '';
            lang.clearConsole();
        }
    });
    
    // Load example
    exampleSelect.addEventListener('change', function() {
        const example = exampleSelect.value;
        if (example && EXAMPLE_PROGRAMS[example]) {
            if (codeEditor.value.trim() !== '' && 
                !confirm('Replace current code with example?')) {
                exampleSelect.value = '';
                return;
            }
            codeEditor.value = EXAMPLE_PROGRAMS[example];
            lang.clearConsole();
            exampleSelect.value = '';
        }
    });
    
    // Save program
    saveButton.addEventListener('click', function() {
        try {
            // Create the program data
            const programData = {
                code: codeEditor.value,
                timestamp: new Date().toISOString(),
                version: '1.0'
            };
            
            // Save to localStorage
            localStorage.setItem('operatorLangProgram', JSON.stringify(programData));
            
            // Create download file
            const blob = new Blob([JSON.stringify(programData, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'operator_program.json';
            a.click();
            URL.revokeObjectURL(url);
            
            lang.writeToConsole('Program saved successfully');
        } catch (e) {
            lang.writeToConsole(`Error saving program: ${e.message}`);
        }
    });
    
    // Load program
    loadButton.addEventListener('click', function() {
        // Create file input for loading JSON
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.json';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);
        
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    // Validate the data
                    if (!data.code || !data.version) {
                        throw new Error('Invalid program file format');
                    }
                    
                    if (data.version !== '1.0') {
                        throw new Error(`Unsupported program version: ${data.version}`);
                    }
                    
                    // Set the code
                    codeEditor.value = data.code;
                    
                    // Save to localStorage
                    localStorage.setItem('operatorLangProgram', JSON.stringify(data));
                    
                    lang.writeToConsole(`Program loaded from file (${new Date(data.timestamp).toLocaleString()})`);
                } catch (e) {
                    lang.writeToConsole(`Error loading program: ${e.message}`);
                }
            };
            reader.onerror = function() {
                lang.writeToConsole('Error reading file');
            };
            reader.readAsText(file);
            
            document.body.removeChild(fileInput);
        });
        
        // Check if we have a saved program in localStorage
        const savedProgram = localStorage.getItem('operatorLangProgram');
        if (savedProgram) {
            try {
                const data = JSON.parse(savedProgram);
                
                // Validate the data
                if (!data.code || !data.version) {
                    throw new Error('Invalid saved program format');
                }
                
                if (data.version !== '1.0') {
                    throw new Error(`Unsupported program version: ${data.version}`);
                }
                
                // Prompt to load the saved program
                if (confirm(`Load saved program from ${new Date(data.timestamp).toLocaleString()}?`)) {
                    codeEditor.value = data.code;
                    lang.writeToConsole(`Program loaded from local storage (${new Date(data.timestamp).toLocaleString()})`);
                    return;
                }
            } catch (e) {
                lang.writeToConsole(`Error loading saved program: ${e.message}`);
            }
        }
        
        // If no saved program or user declined, show file dialog
        fileInput.click();
    });
    
    // Download canvas as image
    downloadButton.addEventListener('click', function() {
        const canvas = document.getElementById('language-canvas');
        const url = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = url;
        a.download = 'operator_canvas.png';
        a.click();
    });
    
    // Load any saved program on startup
    const savedProgram = localStorage.getItem('operatorLangProgram');
    if (savedProgram) {
        try {
            const data = JSON.parse(savedProgram);
            if (data.code && data.version === '1.0') {
                codeEditor.value = data.code;
            }
        } catch (e) {
            console.error('Error loading saved program:', e);
        }
    } else {
        // Load a default program if no saved program exists
        codeEditor.value = EXAMPLE_PROGRAMS.helloWorld;
    }
    
    // Handle key shortcuts in the editor
    codeEditor.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            
            // Insert a tab at the cursor position
            const start = this.selectionStart;
            const end = this.selectionEnd;
            
            // If multiple lines are selected, indent all of them
            if (start !== end) {
                const lines = this.value.split('\n');
                let startLine = this.value.substr(0, start).split('\n').length - 1;
                let endLine = this.value.substr(0, end).split('\n').length - 1;
                
                let newStart = start;
                let newEnd = end;
                
                if (e.shiftKey) {
                    // Unindent
                    for (let i = startLine; i <= endLine; i++) {
                        if (lines[i].startsWith('\t')) {
                            lines[i] = lines[i].substring(1);
                            if (i === startLine) {
                                newStart--;
                            }
                            newEnd--;
                        }
                    }
                } else {
                    // Indent
                    for (let i = startLine; i <= endLine; i++) {
                        lines[i] = '\t' + lines[i];
                        if (i === startLine) {
                            newStart++;
                        }
                        newEnd++;
                    }
                }
                
                this.value = lines.join('\n');
                this.selectionStart = newStart;
                this.selectionEnd = newEnd;
            } else {
                // Just insert a tab at cursor position
                this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
                this.selectionStart = this.selectionEnd = start + 1;
            }
        }
    });
});