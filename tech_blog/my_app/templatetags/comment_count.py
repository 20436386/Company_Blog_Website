from django import template

register = template.Library()
#Custom template filters
@register.filter()
def comment_count(value):
    '''
    Template filter to fetch all values from a list that correspond to the value arg
    '''

    print(value)
    approved_count = 0
    for object in value:
        if (object.status == True):
            approved_count += 1
    return str(approved_count)
    
