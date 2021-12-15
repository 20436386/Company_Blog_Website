from django import template

register = template.Library()
#Custom template filters
@register.filter()
def comment_count(value):
    '''
    Template filter that returns sum of approved comments
    '''

    print(value)
    approved_count = 0
    for object in value:
        if (object.status == True):
            approved_count += 1
    return str(approved_count)
    
