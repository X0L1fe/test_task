from django import template

from menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu_items.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    
    menu = Menu.objects.get(name=menu_name)
    menu_items = MenuItem.objects.filter(menu=menu, is_active=True)

    def build_tree(items, parent=None):
        tree=[]
        for item in items:
            if item.parent == parent:
                children = build_tree(items, item)
                tree.append({
                    'item': item,
                    'children': build_tree(items, item)
                })
        return tree

    menu_tree = build_tree(menu_items)

    def is_active(item):
        if item.url == current_url:
            return True
        for child in item.children:
            if is_active(child['item']):
                return True
        return False
    
    return {
        'menu': menu,
        'menu_tree': menu_tree,
        'current_url': current_url,
        'is_active': is_active,
    }