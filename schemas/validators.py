# Check: All citizen_id in batch are unique
def check_citizen_unique(citizen, ctx):
    if citizen.citizen_id in ctx:
        raise ValueError('All citizen_id in batch must be unique')

# Check: Citizen not relative to himself/herself
def check_not_relative_to_self(citizen, ctx):
    if citizen.citizen_id in ctx[citizen.citizen_id]:
        raise ValueError('Citizen relative to himself/herself')

# Check: All relations are symmetric
def check_are_relations_symmetric(ctx):
    for relative in ctx.values():
        if len(relative) != 0:
            raise ValueError('Relationships are not symmetric')
