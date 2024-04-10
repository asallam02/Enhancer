import plotly.graph_objects as go

def Plotter(Query, Organizer, track_no):
   #get actual results
   original = Query.return_orig_result(track_no)
   modded = Query.return_modded(track_no)
   genes = Query.return_genes()

   indices = list(range(len(original)))

   #get boxes
   dims = Organizer.return_dims()
   boxes = Organizer.return_boxes()
   colors = Organizer.return_colors()
   
   fig = go.Figure(
    data = [
       go.Scatter(x=indices, y=original, name="Original"),
       go.Scatter(x=indices, y=modded, name="Modified")
    ]
   )

   for i in dims.keys():
        #drawing box boundaries
        fig.add_vrect(x0=dims[i][0], x1=dims[i][1])
        #drawing the regions of signficant difference in the box
        for diff_coords in boxes[i]:
            fig.add_vrect(x0=diff_coords[0], x1=diff_coords[1],
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
   
   fig.show()