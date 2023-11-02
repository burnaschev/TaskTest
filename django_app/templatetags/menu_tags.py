from typing import Dict, Any, List

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('django_app/menu.html', takes_context=True)
def draw_menu(context: Context, menu: str) -> Dict[str, Any]:
    try:
        items = MenuItem.objects.filter(menu__title=menu)
        items_values = items.values()

        root_item = [item for item in items_values.filter(parent=None)]

        selected_item_id = int(context['request'].GET[menu])
        selected_item = items.get(id=selected_item_id)

        selected_item_id_list = get_selected_item_id_list(selected_item, root_item, selected_item_id)

        for item in root_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)

        result_dict = {'items': root_item}

    except (KeyError, ObjectDoesNotExist):
        result_dict = {
            'items': [
                item for item in MenuItem.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    result_dict['menu'] = menu
    result_dict['other_querystring'] = build_querystring(context, menu)

    return result_dict


def build_querystring(context: Context, menu: str) -> str:
    querystring_args = []

    for key in context['request'].GET:
        if key != menu:
            querystring_args.append(f"{key}={context['request'].GET[key]}")

    querystring = '&'.join(querystring_args)

    return querystring


def get_child_items(items_values, current_item_id, selected_item_id_list):
    item_list = [item for item in items_values.filter(parent_id=current_item_id)]
    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(items_values, item['id'], selected_item_id_list)
    return item_list


def get_selected_item_id_list(parent: MenuItem, primary_item: List[MenuItem], selected_item_id: int) -> List[int]:
    selected_item_id_list = []

    while parent:
        selected_item_id_list.append(parent.id)
        parent = parent.parent
    if not selected_item_id_list:
        for item in primary_item:
            if item.id == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
