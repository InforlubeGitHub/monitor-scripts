class ScriptError (BaseException):
    def __init__(self, site: str, element: str, message: str, string_search: str):
        self.site = site
        self.element = element
        self.message = message
        self.string_search = string_search

    def __str__(self):
        return f"Site: {self.site}. Elemento: {self.element}. Mensagem: {self.message}. Busca: {self.string_search}"