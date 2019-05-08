from django import template
import re

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter(names='getUsername')
def getUsername(arg1):
    """get username from url path"""
    try:
        usernm = re.search("\/users\/(\w+?)\/", arg1).group(1)
    except AttributeError:
        usernm = ""
    return str(usernm)
