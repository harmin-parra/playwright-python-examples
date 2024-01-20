def get_property(element, prop):
    """ Returns the value of a property of the HTML element """
    func = "(elem, prop) => elem[prop]"
    return element.evaluate(func, prop)


def has_class(element, cls):
    """ Query whether the HTML element has a class """
    func = "(elem, cls) => $(elem).hasClass(cls)"
    return element.evaluate(func, cls)


def get_values(element):
    """ Returns the value(s) of the HTML element """
    return element.evaluate("elem => $(elem).val()")


def invoke(element, func):
    """ Invokes a JQuery function on the HTML element """
    #func2 = "elem => $(elem).$var()"
    #func2 = func2.replace("$var", func)
    func2 = "(elem, func) => $(elem)[func]()"
    return element.evaluate(func2, func)
