def tokenize(text):
    whitespaces = {" ", "\t", "\n"}
    tokens = []
    token = ""
    for c in text:
        if c not in whitespaces:
            token += c
        else:
            if token:
                tokens.append(token)
            token = ""
    if token:
        tokens.append(token)
    return tokens
