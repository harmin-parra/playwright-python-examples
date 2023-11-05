def get_property(element, prop):
    """ Returns the value of a property of the HTML element """
    func = "elem => elem.$var"
    func = func.replace('$var', prop)
    return element.evaluate(func)


def has_class(element, cls):
    """ Query whether the HTML element has a class """
    func = "elem => $(elem).hasClass('$var')"
    func = func.replace("$var", cls)
    return element.evaluate(func)


def get_values(element):
    """ Returns the value(s) of the HTML element """
    element.evaluate("elem => $(elem).val()")


def invoke(element, func):
    """ Invokes a JQuery function on the HTML element """
    func2 = "elem => $(elem).$var()"
    func2 = func2.replace("$var", func)
    element.evaluate(func2)
