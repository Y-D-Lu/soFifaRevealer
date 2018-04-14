import plotly.graph_objs as go
from plotly.offline import plot

from Analyze.point_calc import six_d, df_six_d


# pointPAC,pointSHO,pointPAS,pointDRI,pointDEF,pointPHY
# plot a 6d radar chart to compare (two) players, input the df contains the players
def plot_radar6d(df, is_GK=False):
    n = df.index.__len__()
    if n>6:
        print('Too Many Players!')
        return
    df=df_six_d(df)
    data = []
    if not is_GK:
        for i in df.index:
            data.append(go.Scatterpolar(
                r=[df['PAC'][i],df['SHO'][i],df['PAS'][i],df['DRI'][i],df['DEF'][i],df['PHY'][i],df['PAC'][i]],
                theta=['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'PAC'],
                name=df['Name'][i]
            ))
    else:
        for i in df.index:
            data.append(go.Scatterpolar(
                r=[df['DIV'][i],df['HAN'][i],df['KIC'][i],df['REF'][i],df['SPD'][i],df['POS'][i],df['DIV'][i]],
                theta=['DIV', 'HAN', 'KIC', 'REF', 'SPD', 'POS', 'DIV'],
                name=df['Name'][i]
            ))
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 99]
            )
        ),
        showlegend=False
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig)
