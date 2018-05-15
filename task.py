from pyhop import *

act_ap = {'shoot': 5, 'throw_grenade': 5}
dmg = {'shoot': 5, 'throw_grenade': 10}
assault_weapon = {'shoot': 'rifle', 'throw_grenade': 'grenade'}


def shoot(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['shoot']
    state.hp[t] = state.hp[t] - dmg['shoot']
    return state


def throw_grenade(state, a, t):
    state.ap[a] = state.ap[a] - act_ap['throw_grenade']
    state.hp[t] = state.hp[t] - dmg['throw_grenade']
    state.weapons[a].remove('grenade')
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


declare_methods('act', rifle_assault, grenade_assault)

state1 = State('state1')
state1.weapons = {'ally': ['rifle', 'grenade'], 'enemy': ['rifle']}
state1.hp = {'ally': 20, 'enemy': 20}
state1.ap = {'ally': 15, 'enemy': 10}

goal1 = Goal('goal1')
goal1.hp = {'enemy': 0}

pyhop(state1, [('act', 'ally', 'enemy', goal1)], verbose=3)
