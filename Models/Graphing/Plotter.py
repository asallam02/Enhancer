import plotly.graph_objects as go
import numpy as np
import random

def Plotter(Organizer):
   T1, T2 = Organizer.return_tracks()
   # Create figure
   indices = list(range(len(T1)))

   #Since it's having errors, for now, generate random GC content
   T1GC = []
   T2GC = []
   for _ in range(len(T1)):
        T1GC.append(round(random.uniform(0, 1), 2))  # round to 2 decimal places
        T2GC.append(round(random.uniform(0, 1), 2))

   fig = go.Figure(
       data = [
        go.Scatter(x=indices, y=T1, name="Seq 1", hovertext = T1GC, hoverinfo='x+text'),
        go.Scatter(x=indices, y=T2, name="Seq 2", hovertext = T2GC, hoverinfo='x+text')
        ]
    )
   
   #highlighting the regions of signficant difference for boxed settings
   box_dims = Organizer.return_dims()
   box_diffs, box_color = Organizer.return_boxes()

   for i in box_dims.keys():
        #drawing box boundaries
        fig.add_vrect(x0=box_dims[i][0], x1=box_dims[i][1])
        #drawing the regions of signficant difference in the box
        for diff_coords in box_diffs[i]:
            fig.add_vrect(x0=diff_coords[0], x1=diff_coords[1],
                        fillcolor=box_color[i], opacity=0.2)
            
   fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        ),
        updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[{"visible": [True, True]},
                           {"title": "Yahoo1",
                            "annotations": []}],
                    label="Track A",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False, False]},
                           {"title": "Yahoo2",
                            "annotations": []}],
                    label="Track B",
                    method="update"
                )
            ]),
            direction="down",
            pad={"t": 10},
            showactive=True,
            x=1.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
    )
    #filling in gaps with default setting
    #haven't actually come up with adaquate intersecting box logic yet
   
   fig.show()

    