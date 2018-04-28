import pandas as pd
import plotly.graph_objs as go
import colorlover as cl

from plotly.offline import plot
from scipy.stats import gaussian_kde

from Analyze.point_calc import df_six_d

map_method = {'min': 0, '0.25': 1, '0.5': 2, '0.75': 3, 'max': 4, 'mean': 5}


def plot_map(df, method=map_method['max'], plot_by='ova', show_by='ova', min_players=10, geography='Nation'):
    df_m = df.copy()

    if method == 0:
        df_map = df_m.groupby([geography])[plot_by].min()
    elif method == 1:
        # the 1st Quartile
        df_map = df_m.groupby([geography])[plot_by].quantile(0.25)
    elif method == 2:
        # the 2nd Quartile
        df_map = df_m.groupby([geography])[plot_by].quantile(0.5)
    elif method == 3:
        # the 3rd Quartile
        df_map = df_m.groupby([geography])[plot_by].quantile(0.75)
    elif method == 4:
        # the max
        df_map = df_m.groupby([geography])[plot_by].max()
    elif method == 5:
        # the mean
        df_map = df_m.groupby([geography])[plot_by].mean()

    df_map = pd.DataFrame(data=df_map)
    df_map['text'] = ''
    # drop nations whose players-number is below min_players
    df_geo_s = df_map.copy()
    for i in range(df_map.__len__()):
        if df[['ID', geography]].groupby([geography]).count().iloc[i].values[0] < min_players:
            df_geo_s = df_geo_s.drop(df_map.index[i])
    df_map = df_geo_s
    # get first 5 players among the whole legal players
    df_geo_player = df[[geography, 'Name', show_by]].sort_values(
        show_by, ascending=False).groupby([geography]).head(5)
    # sort by nation name
    df_geo_player = df_geo_player.sort_values([geography, show_by], ascending=[True, False])
    # show as name + ova
    df_geo_player['Name_text'] = df_geo_player['Name'] + ' (' + df_geo_player[show_by].map(str) + ')'
    # get text
    for i in range(df_map.__len__()):
        df_map['text'][i] = '<br>'.join(df_geo_player[df_geo_player[geography] == df_map.index[i]]['Name_text'].values)

    df_map.rename(index={'England': 'United Kingdom'}, inplace=True)

    data = dict(type='choropleth', locations=df_map.index, locationmode='country names',
                z=df_map[plot_by], text=df_map['text'], colorbar={'title': 'Scale'},
                # well i think green is the color of soccer
                colorscale=[[0.0, 'rgb(255,0,0)'], [0.5, 'rgb(255,255,0)'], [0.8, 'rgb(0,255,0)'],
                            [1.0, 'rgb(0,127,0)']], reversescale=False)

    layout = dict(title='plot by ' + plot_by + ' show by ' + show_by,
                  geo=dict(showframe=True, showcoastlines=True, projection={'type': 'Mercator'}))
    _map = go.Figure(data=[data], layout=layout)

    plot(_map, validate=False)


# pointPAC,pointSHO,pointPAS,pointDRI,pointDEF,pointPHY
# plot a 6d radar chart to compare (two) players, input the df contains the players
def plot_radar6d(df, is_GK=False):
    n = df.index.__len__()
    if n > 6:
        print('Too Many Players!')
        return
    df = df_six_d(df)
    data = []
    if not is_GK:
        for i in df.index:
            data.append(go.Scatterpolar(
                r=[df['PAC'][i], df['SHO'][i], df['PAS'][i], df['DRI'][i], df['DEF'][i], df['PHY'][i], df['PAC'][i]],
                theta=['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'PAC'],
                name=df['Name'][i]
            ))
    else:
        for i in df.index:
            data.append(go.Scatterpolar(
                r=[df['DIV'][i], df['HAN'][i], df['KIC'][i], df['REF'][i], df['SPD'][i], df['POS'][i], df['DIV'][i]],
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

    _radar = go.Figure(data=data, layout=layout)
    plot(_radar)


# plot a density map for two relations, such as Age and ova
def plot_density(df, x='Age', y='ova'):
    scl = cl.scales['9']['seq']['Blues']
    colorscale = [[float(i) / float(len(scl) - 1), scl[i]] for i in range(len(scl))]

    def kde_scipy(x, x_grid, bandwidth=0.2):
        kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1))
        return kde.evaluate(x_grid)

    x_grid = pd.np.linspace(df[y].min(), df[y].max(), 100)
    y_grid = pd.np.linspace(df[x].min(), df[x].max(), 100)

    trace1 = go.Histogram2dContour(
        x=df[x], y=df[y], name='density', ncontours=20, colorscale=colorscale, showscale=False
    )
    trace2 = go.Histogram(
        x=df[x], name='x density', yaxis='y2', histnorm='probability density',
        marker=dict(color='rgb(217, 217, 217)'), nbinsx=25
    )
    trace2s = go.Scatter(
        x=x_grid, y=kde_scipy(df[x].as_matrix(), x_grid), yaxis='y2',
        line=dict(color='rgb(31, 119, 180)'), fill='tonexty',
    )
    trace3 = go.Histogram(
        y=df[y], name='y density', xaxis='x2', histnorm='probability density',
        marker=dict(color='rgb(217, 217, 217)'), nbinsy=50
    )
    trace3s = go.Scatter(
        y=y_grid, x=kde_scipy(df[y].as_matrix(), y_grid), xaxis='x2',
        line=dict(color='rgb(31, 119, 180)'), fill='tonextx',
    )
    data = [trace1, trace2, trace2s, trace3, trace3s]
    layout = go.Layout(
        showlegend=False,
        autosize=True,
        width=700,
        height=700,
        hovermode='closest',
        bargap=0,
        xaxis=dict(domain=[0, 0.746], linewidth=2, linecolor='#444', title=x, showgrid=False,
                   zeroline=False, ticks='', showline=True, mirror=True),
        yaxis=dict(domain=[0, 0.746], linewidth=2, linecolor='#444', title=y, showgrid=False,
                   zeroline=False, ticks='', showline=True, mirror=True),
        xaxis2=dict(domain=[0.75, 1], showgrid=False, zeroline=False, ticks='', showticklabels=False),
        yaxis2=dict(domain=[0.75, 1], showgrid=False, zeroline=False, ticks='', showticklabels=False),
    )

    fig = go.Figure(data=data, layout=layout)

    plot(fig)


# plot the candlestick chart for Age versus ova and potential for a df of players
def plot_candlestick(df, x='Age', y1='ova', y2='potential'):
    trace0 = go.Candlestick(x=df.groupby(x)[y1].mean().index,
                            open=(df.groupby(x)[y1].median()),
                            high=(df.groupby(x)[y1].quantile(0.75)),
                            low=(df.groupby(x)[y1].quantile(0.25)),
                            close=(df.groupby(x)[y1].mean()), name=y1)
    trace1 = go.Candlestick(x=df.groupby(x)[y2].mean().index,
                            open=(df.groupby(x)[y2].median()),
                            high=(df.groupby(x)[y2].quantile(0.75)),
                            low=(df.groupby(x)[y2].quantile(0.25)),
                            close=(df.groupby(x)[y2].mean()), name=y2)
    data = [trace0, trace1]
    plot(data)


def plot_age(df,  method=map_method['mean'], x='Age', y=['ova', 'potential']):
    data=[]
    for i in y:
        if method == 0:
            df_i = df.groupby([x])[i].min()
        elif method==1:
            df_i = df.groupby([x])[i].quantile(0.25)
        elif method == 2:
            df_i = df.groupby([x])[i].quantile(0.5)
        elif method == 3:
            df_i = df.groupby([x])[i].quantile(0.75)
        elif method == 4:
            df_i = df.groupby([x])[i].max()
        elif method == 5:
            df_i = df.groupby([x])[i].mean()

        data.append(go.Scatter(
        x=df_i.index,
        y=df_i,
        name=i
    ))
    plot(data)


def plot_num(df, x='Age', y='ID'):
    df = df.groupby([x])[y].count()

    trace = go.Scatter(
        x=df.index,
        y=df,
        name=y
    )
    data = [trace]
    plot(data)
