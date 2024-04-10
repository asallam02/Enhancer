import pandas as pd
import plotly.graph_objects as go

'''
Function that plots genes showing their position on the genome

Inputs:
- gene_data: an array of gene data with each item being of the form 
  ("human_transcript": str, "gene_name": str, gene_start_loc: int, gene_end_loc: int)
'''
def plot_genes(gene_data):
    fig = go.Figure()
    for (transcript, gene, start, end) in gene_data:
        y = [gene]*2
        x = [start, end]

        fig.add_trace(go.Bar(
            y=y, x=x, orientation='h', name=gene, base=start, width = 1,
            hovertext=f'Transcript: {transcript}<br>Gene: {gene}<br>Start Locus: {start}<br>End Locus: {end}'
        ))

    fig.update_layout(
        title='Genomic Data Visualization',
        xaxis_title='Genomic Locus',
        yaxis_title='Gene',
        showlegend=True
    )

    fig.show()

if __name__ == "__main__":
    gene_data = [('NR_024540', 'WASH7P', 14361, 29370), ('NR_106918', 'MIR6859-1', 17368, 17436), ('NR_107062', 'MIR6859-2', 17368, 17436), ('NR_107063', 'MIR6859-3', 17368, 17436), ('NR_128720', 'MIR6859-4', 17368, 17436), ('NR_036051', 'MIR1302-2', 30365, 30503), ('NR_036266', 'MIR1302-9', 30365, 30503), ('NR_036267', 'MIR1302-10', 30365, 30503), ('NR_036268', 'MIR1302-11', 30365, 30503), ('NR_026818', 'FAM138A', 34610, 36081), ('NR_026820', 'FAM138F', 34610, 36081), ('NR_026822', 'FAM138C', 34610, 36081), ('NM_001005484', 'OR4F5', 69090, 70008), ('NR_046018', 'DDX11L1', 11873, 14409), ('NR_039983', 'LOC729737', 134772, 140566), ('NR_106918', 'MIR6859-1', 187890, 187958), ('NR_107062', 'MIR6859-2', 187890, 187958), ('NR_107063', 'MIR6859-3', 187890, 187958), ('NR_128720', 'MIR6859-4', 187890, 187958), ('NR_026823', 'FAM138D', 205128, 206597), ('NR_148357', 'DDX11L17', 182387, 184878)]
    plot_genes(gene_data)