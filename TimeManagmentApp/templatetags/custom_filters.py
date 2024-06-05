from django import template

register = template.Library()


@register.filter
def unique_vehicles(workergroups):
    seen_vehicles = set()
    unique_workergroups = []
    for wg in workergroups:
        if wg.vehicle not in seen_vehicles:
            unique_workergroups.append(wg)
            seen_vehicles.add(wg.vehicle)
    return unique_workergroups


@register.filter
def unique_tasks(workertask):
    seen_task = set()
    unique_workertask = []
    for ut in workertask:
        if ut.task not in seen_task:
            unique_workertask.append(ut)
            seen_task.add(ut.task)
    return unique_workertask


@register.filter(name='in_group')
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()