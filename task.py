from pyhop import *
from math import *

act_ap = {'shoot': 5, 'throw_grenade': 5, 'stab': 2}
dmg = {'shoot': 5, 'throw_grenade': 10, 'stab': 20}
assault_weapon = {'shoot': 'rifle', 'throw_grenade': 'grenade', 'stab': 'knife'}
weapon_range = {'rifle': 10, 'grenade': 5, 'knife': 1}
ap_dist_mul = 1


def ap_to_steps(ap):
    return floor(ap * ap_dist_mul)


def steps_to_ap(dist):
    return ceil(dist / ap_dist_mul)


def shoot(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['shoot']
    state.hp[t] = state.hp[t] - dmg['shoot']
    return state


def throw_grenade(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['throw_grenade']
    state.hp[t] = state.hp[t] - dmg['throw_grenade']
    state.weapons[a].remove('grenade')
    return state


def walk(state, a, t, steps):
    state.ap[a] = state.ap[a] - steps_to_ap(steps)
    state.distance[a][t] = state.distance[a][t] - steps
    return state


def stab(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['stab']
    state.hp[t] = state.hp[t] - dmg['stab']
    return state


declare_operators(shoot, throw_grenade, stab, walk)


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


def move_gen(steps):
    def move(state, a, t, goal):
        if state.ap[a] >= steps_to_ap(dist):
            return [('walk', a, t, steps), ('act', a, t, goal)]
        return False

    return move


dist = 10

move_list = [move_gen(x) for x in range(dist)]

declare_methods('act', rifle_assault, grenade_assault, *move_list)

state1 = State('state1')
state1.weapons = {'ally': ['rifle', 'grenade'], 'enemy': ['rifle']}
state1.hp = {'ally': 20, 'enemy': 30}
state1.ap = {'ally': 15, 'enemy': 10}
state1.distance = {'ally': {'enemy': dist}}

goal1 = Goal('goal1')
goal1.hp = {'enemy': 0}

pyhop(state1, [('act', 'ally', 'enemy', goal1)], verbose=3)
