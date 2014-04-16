from django import template
from membership.models import Member

register = template.Library()

@register.filter
def can_view(goal, user):
    return goal.member.user.id == user.id or (goal.who_can_view == "Restricted" and Member.objects.get(user=user) in goal.member.auth.all()) or goal.who_can_view == "Everyone"
