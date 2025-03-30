
from debug import *
from tokens import *

"""
OPERATORS:
    # - Stringize
    ## - Token Pasting
DIRECTIVES:
    define
    undef
    include
    ifdef
    ifndef
    if
    else
    elif
    endif
CONDITIONALS:
    defined()
    +, -, *, /, %,
    ==, !=, <, >, <=, >=,
    &&, ||, !,
    &, |, ^, ~, <<, >>
PREDEFINED:
    __DATE__
    __TIME__
    __FILE__
    __LINE__
    __STDC__
"""

class FunctionMacro:
    def __init__(self, args:Tokens, definition, is_variadic=False):
        self.args = args
        self.is_variadic = is_variadic
        self.definition = definition

    def get_replacement(self, args:Tokens):
        dbg(f"Getting replacement for {args}")
        result = Tokens([])

        # throw error if not enough args supplied
        if self.is_variadic:
            if len(args) < len(self.args)-1:
                self.definition[0].fatal_error("Too few args supplied to Macro")
        else:
            if len(args) > len(self.args):
                self.definition[0].fatal_error("Too many args supplied to Macro")
            elif len(args) < len(self.args):
                self.definition[0].fatal_error("Too few args supplied to Macro")

        for x in self.definition:
            result.append(x)

        # put the passed values into the definition
        i = 0
        n = len(result)
        while i < n:
            if result[i] == "__VA_ARGS__":
                if not self.is_variadic:
                    result[i].fatal_error("Cannot use __VA_ARGS__ in non-variadic function")
                insertion = []
                for j in range(len(self.args)-1, len(args)):
                    insertion += args[j]
                    if j < len(args)-1:
                        new_tok = string_to_token(",")
                        insertion.append(new_tok)
                print(result[i])
                del result[i]
                result.insert_all(i, insertion)
                i += len(insertion)
                n = len(result)
                continue
            elif result[i] in self.args:
                ind = self.args.index(result[i])
                del result[i]
                result.insert_all(i, args[ind])
                i += len(args[ind])
                n = len(result)
                continue
            i += 1

        # perform stringizing
        i = 0
        n = len(result)
        while i < n:
            if result[i] == "#":
                # next toke becomes string literal
                if i + 1 >= n:
                    result[i].fatal_error("Expected token to stringize after this")
                del result[i]
                n -= 1
                result[i].token = f'"{result[i].token}"'
            i += 1

        # perform token pasting
        i = 0
        n = len(result)
        while i < n:
            if result[i] == "##":
                del result[i]
                i -= 1
                n -= 1
                if i + 1 >= n:
                    result[i].fatal_error("Expected token to paste with after")
                result[i].token += result[i+1].token
                del result[i+1]
                n -= 1
            i += 1

        return result


DEFINITIONS = {}
CONDITIONS = []
DELETING = False

def preprocess(toks:Tokens):
    """
    iterate through the file and handle a directive at a time
    """
    dbg("Handling Directives...")
    toks = handle_directives(toks)

    dbg("Finshed Preprocessing!")
    dbg(toks)
    return toks


def handle_directives(toks:Tokens):
    i = 0
    n = len(toks)

    while i < n:
        if toks[i] == "#":
            directive = toks.splice_until(i, "#END_DIRECTIVE")
            directive = Tokens(directive)
            directive = replace_with_defined(directive)
            dbg(f"Found directive:")
            dbg(directive)
            handle_directive(directive)
            n = len(toks)
            i -= 1
        elif DELETING:
            del toks[i]
            i -= 1
            n -= 1
        elif toks[i] in DEFINITIONS:
            # replace with the definition
            toks = replace_index_with_defined(toks, i)
            new_n = len(toks)
            i += new_n - n
            n = new_n
        i += 1

    return toks


def replace_index_with_defined(toks:Tokens, index:int):
    """
    Use the definitions to replace tokens at specific index
    """
    # see if this should be function-like or normal
    if toks[index] not in DEFINITIONS:
        return toks

    the_definition = DEFINITIONS[toks[index]]

    if issubclass(type(the_definition), FunctionMacro):
        dbg("Should be replaced with function macro")
        if index + 1 >= len(toks) or toks[index+1] != "(":
            return toks
        arg_values = toks.get_match_content(index+1, ")")
        if arg_values is None:
            toks[index+1].fatal_error("Unmatched (")
        arg_values = arg_values[1:-1]
        arg_values = Tokens(arg_values).split_at(",")
        dbg(f"Function args values: {arg_values}")
        replacement = the_definition.get_replacement(arg_values)
        dbg(f"Replacement = {replacement}")

        del toks[index]
        toks.insert_all(index, replacement)

    else:
        dbg("Should be replaced normally")
        del toks[index]
        toks.insert_all(index, the_definition)

    return toks


def replace_with_defined(toks:Tokens):
    """
    Use the definitions to replace tokens
    """
    i = 0
    n = len(toks)
    while i < n:
        if toks[i] in DEFINITIONS:
            toks = replace_index_with_defined(toks, index)
            new_n = len(toks)
            i += new_n - n
            n = new_n
        i += 1
    return toks


def get_directive_type(directive):
    if len(directive) <= 1:
        directive[0].fatal_error("Expected content in directive")
    valid_types = set(["define", "undef", "include", "ifdef", "ifndef", "if", "else", "elif", "endif"])

    i = 1
    while i < len(directive):
        if directive[i] not in valid_types:
            if directive[i] != "#DEFINE_SPACE":
                directive[i].fatal_error("Invalid directive")
        else:
            return directive[i]
        i += 1


def handle_directive(directive):
    directive_type = get_directive_type(directive)
    match (directive_type):
        case "define":
            if not DELETING:
                handle_define(directive)
        case "undef":
            if not DELETING:
                handle_undef(directive)
        case "include":
            if not DELETING:
                handle_include(directive)
        case "ifdef":
            handle_ifdef(directive)
        case "ifndef":
            handle_ifndef(directive)
        case "if":
            handle_if(directive)
        case "else":
            handle_else(directive)
        case "elif":
            handle_elif(directive)
        case "endif":
            handle_endif(directive)


def handle_define(directive):
    dbg("Handling define...")
    if len(directive) > 0 and directive[-1] == "#END_DIRECTIVE":
        del directive[-1]

    # figure out if a normal or function-like macro
    # first, get first thing after the define and DEFINE_SPACE
    while len(directive) > 0:
        if directive[0] != "define":
            del directive[0]
        else:
            define_token = directive[0]
            del directive[0]
            del directive[0]
            break
    # we should now be at the definition name
    if len(directive) == 0:
        define_token.fatal_error("Expected definition after define")

    the_definition = directive[0]
    if len(directive) < 2:
        directive[0].fatal_error("Expected definiton after define")
    dbg(f"DefName = {the_definition}")

    if directive[1] == "(":
        definition_type = "function"
    else:
        definition_type = "normal"

    dbg(f"Definiton type is {definition_type}")
    if definition_type == "normal":
        # if normal, add to definitions
        del directive[0]
        del directive[0]
        handle_normal_define(the_definition, directive)
    else:
        # if function-like, handle separately
        del directive[0]
        directive = Tokens(directive)
        args = directive.get_match_content(0, ")")
        if args is None:
            directive[0].fatal_error("Unmatched (")
        args = args[1:-1]

        if len(directive) == 0 or directive[0] != "#DEFINE_SPACE":
            the_definition.fatal_error("No definition")

        del directive[0]

        handle_function_define(the_definition, args, directive)


def handle_normal_define(the_definition, directive):
    dbg("Handling normal define:")
    dbg(f"\tdefinition: {the_definition}")
    dbg(f"\tdirective: {directive}")
    if the_definition in DEFINITIONS:
        the_definition.fatal_error(f"Redefinition of {the_definition}")
    directive = [x for x in directive if x != "#DEFINE_SPACE"]
    DEFINITIONS[the_definition] = Tokens(directive)


def handle_function_define(the_definition, args, directive):
    dbg("Handling function define:")
    dbg(f"\tdefinition: {the_definition}")
    dbg(f"\targs: {args}")
    dbg(f"\tdirective: {directive}")
    if the_definition in DEFINITIONS:
        the_definition.fatal_error(f"Redefinition of {the_definition}")
    directive = Tokens([x for x in directive if x != "#DEFINE_SPACE"])

    args = Tokens(args)
    args.combine_all([".", ".", "."])
    args.remove_all("#DEFINE_SPACE")
    args = args.split_at(",")
    # combine ...
    # combine ##
    directive.combine_all(["#", "#"])

    # throw error if ... exists and is not last arg
    is_variadic = False
    for i in range(len(args)):
        if len(args[i]) == 0:
            the_definition.fatal_error("Cannot define function-like macro with empty argument")
        args[i] = args[i][0]
        if args[i] == "...":
            if i != len(args)-1:
                args[i].fatal_error("... must be last argument")
            is_variadic = True

    # create FunctionMacro object
    result = FunctionMacro(args, directive, is_variadic=is_variadic)

    DEFINITIONS[the_definition] = result


def handle_undef(directive):
    dbg("Handling undef...")
    directive.remove_all("#DEFINE_SPACE")
    directive.remove_all("#END_DIRECTIVE")
    if len(directive) < 3:
        directive[1].fatal_error("Expected a definition after undef")
    definition = directive[2]
    if definition in DEFINITIONS:
        DEFINITIONS.pop(definition)
        dbg(f"Removed definition of {definition}")


def handle_include(directive):
    dbg("Handling include...")
    # TODO
    # figure out if it is a local or library include


def handle_ifdef(directive:Tokens):
    dbg("Handling ifdef...")
    directive.remove_all("#DEFINE_SPACE")
    directive.remove_all("#END_DIRECTIVE")
    if len(directive) < 3:
        directive[1].fatal_error("Invalid ifdef syntax")
    definition = directive[2]
    if definition in DEFINITIONS:
        CONDITIONS.append(True)
        dbg("ifdef = True")
    else:
        CONDITIONS.append(False)
        dbg("ifdef = False")
    should_delete()

def handle_ifndef(directive):
    dbg("Handling ifndef...")
    directive.remove_all("#DEFINE_SPACE")
    directive.remove_all("#END_DIRECTIVE")
    if len(directive) < 3:
        directive[1].fatal_error("Invalid ifndef syntax")
    definition = directive[2]
    if definition in DEFINITIONS:
        CONDITIONS.append(False)
        dbg("ifndef = False")
    else:
        CONDITIONS.append(True)
        dbg("ifndef = True")
    should_delete()

def handle_if(directive):
    dbg("Handling if...")
    directive.remove_all("#DEFINE_SPACE")
    directive.remove_all("#END_DIRECTIVE")
    condition = directive[2:]
    result = check_condition(condition)
    CONDITIONS.append(result)
    should_delete()


def handle_else(directive):
    dbg("Handling else...")
    # if condition was true, change to None
    if len(CONDITIONS) == 0:
        directive[1].fatal_error("No conditional opened")
    if CONDITIONS[-1] == True:
        CONDITIONS[-1] = None
        dbg("Closed previous conditional")
    elif CONDITIONS[-1] == False:
        CONDITIONS[-1] = True
        dbg("else = True")
    should_delete()


def handle_elif(directive):
    dbg("Handling elif...")
    if len(CONDITIONS) == 0:
        directive[1].fatal_error("No conditional opened")
    if CONDITIONS[-1] == True:
        CONDITIONS[-1] = None
        dbg("Closed previous conditional")
    elif CONDITIONS[-1] == False:
        # check the condition
        directive.remove_all("#DEFINE_SPACE")
        directive.remove_all("#END_DIRECTIVE")
        condition = directive[2:]
        result = check_condition(condition)
        CONDITIONS[-1] = result
        dbg(f"elif = {result}")
    should_delete()


def handle_endif(directive):
    dbg("Handling endif...")
    if len(CONDITIONS) == 0:
        directive[1].fatal_error("Unmatched endif")
    CONDITIONS.pop()
    dbg("Closed conditional")
    should_delete()


def check_condition(condition):
    dbg(f"Checking condition:")
    dbg(condition)
    # TODO
    return True


def should_delete():
    global DELETING
    DELETING = False
    for x in CONDITIONS:
        if x == False:
            DELETING = True
    return DELETING

