import os
import fnmatch

# Nome do próprio script (para esconder)
SELF_FILE = "hierarquia-de-pastas.py"

# Regras tipo .gitignore
IGNORE_RULES = [
    "logs",
    "*.log",
    "npm-debug.log*",
    "yarn-debug.log*",
    "yarn-error.log*",
    "pnpm-debug.log*",
    "lerna-debug.log*",
    "node_modules",
    "dist",
    "dist-ssr",
    "*.local",
    ".vscode/*",
    "!.vscode/extensions.json",
    ".idea",
    ".DS_Store",
    "*.suo",
    "*.ntvs*",
    "*.njsproj",
    "*.sln",
    "*.sw?"
]


def match_rule(path, rule):
    return fnmatch.fnmatch(path, rule)


def should_ignore(path):
    ignored = False

    for rule in IGNORE_RULES:
        if rule.startswith("!"):
            if match_rule(path, rule[1:]):
                ignored = False
        else:
            if match_rule(path, rule):
                ignored = True

    return ignored


def should_ignore_contents(path):
    for rule in IGNORE_RULES:
        if rule.endswith("/*"):
            base = rule[:-2]
            if path == base or path.startswith(base + os.sep):
                return True

        if not any(c in rule for c in "*?") and not rule.startswith("!"):
            if os.path.basename(path) == rule:
                return True

    return False


def mostrar_arvore(diretorio, prefixo="", raiz=None):
    if raiz is None:
        raiz = diretorio

    try:
        itens = sorted(os.listdir(diretorio))
    except PermissionError:
        print(prefixo + "└── [SEM PERMISSÃO]")
        return

    itens_visiveis = []
    for item in itens:
        if item == SELF_FILE:
            continue

        caminho = os.path.join(diretorio, item)
        rel_path = os.path.relpath(caminho, raiz)

        if not should_ignore(rel_path):
            itens_visiveis.append((item, caminho, rel_path))

    for i, (item, caminho, rel_path) in enumerate(itens_visiveis):
        ultimo = i == len(itens_visiveis) - 1

        if ultimo:
            conector = "└── "
            novo_prefixo = prefixo + "    "
        else:
            conector = "├── "
            novo_prefixo = prefixo + "│   "

        print(prefixo + conector + item)

        if os.path.isdir(caminho):
            if not should_ignore_contents(rel_path):
                mostrar_arvore(caminho, novo_prefixo, raiz)
            else:
                print(novo_prefixo + "└── ...")


if __name__ == "__main__":
    caminho = input("Digite o caminho da pasta (ENTER = pasta atual): ").strip()

    if caminho == "":
        caminho = os.getcwd()

    if not os.path.exists(caminho):
        print("❌ Caminho inválido!")
        exit()

    nome_projeto = os.path.basename(os.path.abspath(caminho))

    print("\n📁", nome_projeto)
    mostrar_arvore(caminho)
