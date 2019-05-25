def _execute(__code, gr):
    exec(compile(__code, "", "exec"))

def _executeBlock(__code, gr, block):
    exec(compile(__code, "", "exec"))
