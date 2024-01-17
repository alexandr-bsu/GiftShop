def extract_citizen_birth_date_to_dict(citizens):
    citizens = citizens.citizens
    return {citizen.citizen_id: citizen.birth_date for citizen in citizens}

# If relations are symmetric, all sets of citizens relatives will be empty
def difference_relatives(citizen, ctx):
    exclude_relatives = set()
    for relative in ctx[citizen.citizen_id]:
        symmetry_relatives = ctx.get(relative, None)

        if symmetry_relatives is not None:
            ctx[relative].remove(citizen.citizen_id)
            exclude_relatives.add(relative)

    ctx[citizen.citizen_id].difference_update(exclude_relatives)
