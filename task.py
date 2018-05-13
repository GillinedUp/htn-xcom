from pyhop import *

move_ap = {'shoot': 5}


def shoot(state, a, t):
    if 'rifle' in state.weapons[a] and state.ap[a] >= 5:
        state.ap[a] = state.ap[a] - 5
        state.hp[t] = state.hp[t] - 5
        return state
    else:
        return False


declare_operators(shoot)


def move(state, a, t):
    while any(state.ap[a] >= x for x in list(move_ap.values())):
        return [('shoot', a, t), ('move', a, t)]
    return []


declare_methods('move', move)

state1 = State('state1')
state1.weapons = {'ally': ['rifle'], 'enemy': ['rifle']}
state1.hp = {'ally': 20, 'enemy': 10}
state1.ap = {'ally': 20, 'enemy': 10}

goal1 = Goal('goal1')
goal1.hp = {'enemy': 0}

pyhop(state1, [('move', 'ally', 'enemy')], verbose=3)
