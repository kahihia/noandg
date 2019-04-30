from django import template
from django.shortcuts import get_object_or_404

from apps.engineering.forms import ProjectEquipmentForm
from apps.engineering.models import ProjectEquipment

register = template.Library()


@register.filter(name='equipment_form_instance')
def equipment_form_instance(value):
    equipment = get_object_or_404(ProjectEquipment, slug=value)
    return ProjectEquipmentForm(instance=equipment)
