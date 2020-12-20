import plotly.graph_objects as go
import numpy as np
import plotly.graph_objects as go
import numpy as np
from wumpusWorld.environment.Environment import *


def draw_percepts(percept, agent, fig):
    if percept.breeze:
        fig.add_annotation(x=agent.location.x + 0.1, y=agent.location.y + 0.9, text="breeze")
    if percept.bump:
        fig.add_annotation(x=agent.location.x + 0.1, y=agent.location.y + 0.7, text="bump")
    if percept.glitter:
        fig.add_annotation(x=agent.location.x + 0.1, y=agent.location.y + 0.5, text="glitter")
    if percept.scream:
        fig.add_annotation(x=agent.location.x + 0.1, y=agent.location.y + 0.3, text="scream")
    if percept.stench:
        fig.add_annotation(x=agent.location.x + 0.1, y=agent.location.y + 0.1, text="stench")


def draw_arrow(agent, fig):
    if agent.hasArrow:
        fig.add_trace(go.Scatter(x=[agent.location.x + 0.2], y=[agent.location.y + 0.2],
                                 mode='markers',
                                 marker=dict(size=[10], color='brown'),
                                 name='Arrow'))


def draw_gold(agent, fig):
    if agent.hasGold:
        fig.add_trace(go.Scatter(x=[agent.location.x + 0.8], y=[agent.location.y + 0.2],
                                 mode='markers',
                                 marker=dict(size=[10], color='yellow'),
                                 name='Arrow'))


def draw_agent(agent, fig):
    fig.add_trace(go.Scatter(x=[agent.location.x + 0.5], y=[agent.location.y + 0.5],
                             mode='markers+text',
                             marker=dict(size=[50], color='lightblue'),
                             name='Agent',
                             text=[agent.orientation]))
    draw_arrow(agent, fig)
    draw_gold(agent, fig)


def create_figure(action, percept):
    fig = go.Figure(layout=go.Layout(title=go.layout.Title(text="Current Action : " + str(action) +
                                                                "  Current Reward : " + str(percept.reward)),
                                     autosize=False,
                                     width=700,
                                     height=500))
    fig.update_xaxes(showgrid=True, gridwidth=4, range=(0, 4), nticks=5)
    fig.update_yaxes(showgrid=True, gridwidth=4, range=(0, 4), nticks=5)

    return fig


def draw_environment(env, fig):
    fig.add_trace(go.Scatter(x=[env.wumpusLocation.x + 0.5], y=[env.wumpusLocation.y + 0.5],
                             mode='markers',
                             marker=dict(size=[50], color='green' if env.wumpusAlive else 'brown'),
                             name='Wumpus' if env.wumpusAlive else 'Dead Wumpus'))

    for pitLocation in env.pitLocations:
        fig.add_trace(go.Scatter(x=[pitLocation.x + 0.5], y=[pitLocation.y + 0.5],
                                 mode='markers',
                                 marker=dict(size=[50], color='black'),
                                 name='Pit'))

    fig.add_trace(go.Scatter(x=[env.goldLocation.x + 0.5], y=[env.goldLocation.y + 0.5],
                             mode='markers',
                             marker=dict(size=[50], color='yellow'),
                             name='Gold'))


def draw_beliefs(beliefs, fig, belief_type='pit_belief'):
    gridWidth = 4
    gridHeight = 4
    if belief_type == 'pit_belief':
        shift = 0.2
    elif belief_type == 'wumpus_belief':
        shift = 0.8
    else:
        raise ValueError("belief type can only be for wumpus or pit!!")
    for j in range(gridHeight):
        for i in range(gridWidth):
            fig.add_trace(go.Scatter(x=[i + shift], y=[j + 0.8],
                                     mode='text',
                                     # marker=dict(size=[50], color='lightblue'),
                                     name=belief_type,
                                     text="%0.2f" % beliefs[j * 4 + i]))


def visualize_env(env, agent, action, percept, pit_beliefs=[], wumpus_beliefs=[]):
    fig = create_figure(action, percept)

    draw_environment(env, fig)
    draw_agent(agent, fig)
    draw_percepts(percept, agent, fig)

    if pit_beliefs != []:
        draw_beliefs(pit_beliefs, fig, 'pit_belief')
    if wumpus_beliefs != []:
        draw_beliefs(wumpus_beliefs, fig, 'wumpus_belief')

    fig.show()