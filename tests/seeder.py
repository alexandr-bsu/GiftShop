from random import randint, shuffle
import time
from schemas.ImportCitizens import ImportCitizens
from schemas.Citizen import Citizen


def random_seq_exclude(a, b, ex=-1):
    result = set()
    i = 0
    while i != max(a, b) - min(a, b) + (0 if ex != -1 else 1):
        temp = randint(a, b)
        if temp not in result and temp != ex:
            result.add(temp)
            i += 1

    return result


def gen_correct_full_linked_data(max_citizens=1000):
    start = time.time()
    citizens = random_seq_exclude(1, max_citizens)
    result = [{'citizen_id': citizen, 'relatives': random_seq_exclude(1, max_citizens, citizen)} for citizen in
              citizens]
    end = time.time()
    print("The time of execution of above program is :",
          (end - start) * 10 ** 3, "ms")

    return result

def gen_symmetric_relations(citizen, relative, citizen_relatives):
    citizen_relatives[citizen].add(relative)
    citizen_relatives[relative].add(citizen)


def gen_randomized_data(max_citizen=10000, max_relatives=1000):
    citizen_relatives = {citizen_id: set() for citizen_id in range(1, max_citizen)}
    for i in range(max_relatives):
        citizen = randint(1, max_citizen)
        while citizen == max_citizen:
            citizen = randint(1, max_citizen)

        relative = randint(1, max_citizen)
        while relative == max_citizen or relative == citizen:
            citizen = randint(1, max_citizen)

        gen_symmetric_relations(citizen, relative, citizen_relatives)

    keys = list(citizen_relatives.keys())
    shuffle(keys)

    return [{'citizen_id': citizen_id, 'relatives': list(citizen_relatives[citizen_id]), 'town': 'Улан-Удэ',
             'street':'Юного коммунара', 'building': '4', 'apartment': 7, 'name': 'Родионов Алексндр Сергеевич',
             'birth_date': '25.04.2002', 'gender': 'male'}
            for citizen_id in keys]



# print(gen_randomized_data(10000,1000))


def validator(data):
    start = time.time()
    citizens = data
    citizens_relatives = {}

    for citizen in citizens:
        # Check: All citizen_id in batch are unique
        if citizen['citizen_id'] in citizens_relatives:
            raise ValueError('All citizen_id in batch must be unique')

        # Add sets of relatives to dict for fast access
        citizens_relatives[citizen['citizen_id']] = set(citizen['relatives'])

        # Check: Citizen not relative to himself/herself
        if citizen['citizen_id'] in citizens_relatives[citizen['citizen_id']]:
            raise ValueError('Citizen relative to himself/herself')

        # Check: All relatives has symmetry
        exclude_relatives = set()
        for relative in citizens_relatives[citizen['citizen_id']]:
            symmetry_relatives = citizens_relatives.get(relative, None)

            # Relative haven't been scanned
            # if symmetry_relatives is None:
            #     break

            if symmetry_relatives is not None:
                citizens_relatives[relative].remove(citizen['citizen_id'])
                exclude_relatives.add(relative)

        citizens_relatives[citizen['citizen_id']].difference_update(exclude_relatives)

    # Check: All relations are symmetric
    for relative in citizens_relatives.values():
        if len(relative) != 0:
            raise ValueError('Relationships are not symmetric')

    end = time.time()

    # print the difference between start
    # and end time in milli. secs
    print("The time of execution of above program is 2:",
          (end - start) * 10 ** 3, "ms")

    return data

#
# c = gen_correct_full_linked_data(4000)
# start2 = time.time()
# ImportCitizens(citizens=c)
# end2 = time.time()
# print("The time of execution of above program is 3:",
#           (end2-start2) * 10 ** 3, "ms")

# c = gen_randomized_data(100000,60000)
# c = gen_correct_full_linked_data(1000)
# print('r')

# start2 = time.time()
# ImportCitizens(citizens=c)
# end2 = time.time()
#
# print("The time of execution of above program is 3:",
#       (end2 - start2) * 10 ** 3, "ms")

# validator(c)
