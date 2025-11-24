from django import template

register = template.Library()

@register.filter
def es_moderador_o_gestor(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name="Moderador").exists() or
            user.groups.filter(name="Gestor").exists()
        )
    )
