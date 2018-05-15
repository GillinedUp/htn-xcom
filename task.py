from pyhop import *
from math import *

act_ap = {'shoot': 5, 'throw_grenade': 5}
dmg = {'shoot': 5, 'throw_grenade': 10}
assault_weapon = {'shoot': 'rifle', 'throw_grenade': 'grenade'}
weapon_range = {'rifle': 10, 'grenade': 5, 'knife': 1}
map_size = 20
ap_dist_mul = 1


def ap_to_dist(ap):
    return floor(ap * ap_dist_mul)


def dist_to_ap(dist):
    return ceil(dist / ap_dist_mul)


def distance(oldpos, newpos):
    oldx, oldy = oldpos
    newx, newy = newpos
    return floor(sqrt(oldx * newx + oldy * newy))


def shoot(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['shoot']
    state.hp[t] = state.hp[t] - dmg['shoot']
    return state


def throw_grenade(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['throw_grenade']
    state.hp[t] = state.hp[t] - dmg['throw_grenade']
    state.weapons[a].remove('grenade')
    return state


def walk(state, a, oldpos, newpos):
    dist = distance(oldpos, newpos)
    state.ap[a] = state.ap[a] - dist_to_ap(dist)
    state.position[a] = newpos
    return state


declare_operators(shoot, throw_grenade)


def is_done(state, goal):
    if state.hp['enemy'] == goal.hp['enemy']:
        return True
    return False


def assault(state, a, t, assault_type, goal):
    if is_done(state, goal):
        return []
    while state.ap[a] >= act_ap[assault_type] \
            and assault_weapon[assault_type] in state.weapons[a]:
        return [(assault_type, a, t), ('act', a, t, goal)]
    return False


def rifle_assault(state, a, t, goal):
    return assault(state, a, t, 'shoot', goal)


def grenade_assault(state, a, t, goal):
    return assault(state, a, t, 'throw_grenade', goal)


def move_gen(oldpos, newpos):
    def move(state, a, t, goal):
        dist = distance(oldpos, newpos)
        if state.position[a] == oldpos and state.ap[a] >= dist_to_ap(dist):
            return [('walk', a, oldpos, newpos), ('act', a, t, goal)]
        return False

    return move


move_list = [move_gen((x1, y1), (x2, y2)) for x1 in range(map_size) for y1 in range(map_size)
             for x2 in range(map_size) for y2 in range(map_size)]

declare_methods('act', rifle_assault, grenade_assault, *move_list)

state1 = State('state1')
state1.weapons = {'ally': ['rifle', 'grenade'], 'enemy': ['rifle']}
state1.hp = {'ally': 20, 'enemy': 20}
state1.ap = {'ally': 15, 'enemy': 10}
state1.position = {'ally': (5, 0), 'enemy': (15, 0)}

goal1 = Goal('goal1')
goal1.hp = {'enemy': 0}

pyhop(state1, [('act', 'ally', 'enemy', goal1)], verbose=3)
