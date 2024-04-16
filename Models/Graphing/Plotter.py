import plotly.graph_objects as go

'''The following are helper functions for plotting results from enformer'''

def Plotter(Query, Organizer, track_no):
   # get actual results
   original = Query.return_orig_result(track_no)
   modded = Query.return_modded(track_no)
   start = Query.return_start()

   indices = [(start + (i * 128)) for i in range(len(original))]

   # get difference boxes
   dims = Organizer.return_dims()
   boxes = Organizer.return_boxes()
   colors = Organizer.return_colors()
   
   # create figure
   fig = go.Figure(
    data = [
       go.Scatter(x=indices, y=original, name="Original"),
       go.Scatter(x=indices, y=modded, name="Modified")
    ]
   )

   for i in dims.keys():
        # drawing box boundaries
        fig.add_vrect(x0=start + (dims[i][0]*128), x1=start + (dims[i][1]*128))
        # drawing the regions of signficant difference in the box
        for diff_coords in boxes[i]:
            fig.add_vrect(x0=start + (diff_coords[0]*128), x1=start + (diff_coords[1]*128),
                        fillcolor=colors[i], opacity=0.2)
            
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
        )
    )
   
   return fig