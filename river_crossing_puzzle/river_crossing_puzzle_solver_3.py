import queue
import itertools


def leftover(all_items, remove_items):
    leftover_items = []
    for i in all_items:
        if i not in remove_items:
            leftover_items.append(i)
    return leftover_items


LEFT = 0
RIGHT = 1

characters = sorted(['A', 'a1', 'a2', 'B', 'b1', 'b2', 'C', 'c', 'boat'])
left_side = sorted(['A', 'a1', 'a2', 'B', 'b1', 'b2', 'C', 'c', 'boat'])
# everybody in the left side of rever
right_side = sorted([])
# nobady in the right side of rever
rowers = ['A', 'B', 'C']
# the man only can row the boat
boat_size = 2
ban = [(['A'], ['a1', 'B']), (['A'], ['a2', 'B']),
       (['B'], ['b1', 'A']), (['B'], ['b2', 'A']),
       (['C'], ['c', 'A']), (['C'], ['c', 'a1']), (['C'], ['c', 'a2']),
       (['C'], ['c', 'B']), (['C'], ['c', 'b1']), (['C'], ['c', 'b2']), ]
goal = [[], sorted(['A', 'a1', 'a2', 'B', 'b1', 'b2', 'C', 'c', 'boat'])]
Q = queue.Queue()
past = dict()
Q.put((left_side[:], right_side[:], ['start']))
while not Q.empty():
    q = Q.get()
    if tuple(q[LEFT]) in past:
        continue
    else:
        past.update({tuple(q[LEFT]): q[2]})
    if q[LEFT] == goal[LEFT] and q[RIGHT] == goal[RIGHT]:
        path = []
        t = q[LEFT]
        while t != ['start']:
            path.append(t)
            t = past[tuple(t)]
        path.reverse()
        for p in path:
            print(p, leftover(characters, p))
        exit()

    boat = RIGHT
    if 'boat' in q[LEFT]:
        boat = LEFT
    for rower in rowers:
        if rower in q[boat]:
            for passengers in itertools.combinations([''] * (boat_size - 1) + q[boat], boat_size - 1):
                if rower in passengers or 'boat' in passengers:
                    continue
                left = q[LEFT][:]
                right = q[RIGHT][:]
                if boat == LEFT:
                    left.remove('boat')
                    right.append('boat')
                    if rower != '':
                        left.remove(rower)
                        right.append(rower)
                    for passenger in passengers:
                        if passenger != '':
                            left.remove(passenger)
                            right.append(passenger)
                else:
                    right.remove('boat')
                    left.append('boat')
                    if rower != '':
                        right.remove(rower)
                        left.append(rower)
                    for passenger in passengers:
                        if passenger != '':
                            right.remove(passenger)
                            left.append(passenger)
                is_banned = False
                for b in ban:
                    if (all(c in left for c in b[0]) and all(c in right for c in b[1])) or (all(c in left for c in b[1]) and all(c in right for c in b[0])):
                        is_banned = True
                if not is_banned:
                    Q.put((sorted(left[:]),
                           sorted(right[:]), sorted(q[LEFT][:])))
print('no answer')
