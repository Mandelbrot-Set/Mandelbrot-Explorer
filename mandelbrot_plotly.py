import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import time
from utils import *

iw = 1500
ih = 1500
cw = 1250
ch = 1250

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app = dash.Dash()
app.config['suppress_callback_exceptions'] = True


def mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=250, width=iw, height=ih):
    re = np.linspace(xmin, xmax, width, dtype=np.float64)
    im = np.linspace(ymin, ymax, height, dtype=np.float64)
    c = re + im[:, None]*1j

    n3 = mandelbrot_numpy(c, maxiter)

    return re, im, n3.T

# @jit
# def mandelbrot(c, maxiter, threshold=2):
#     z_ = c
#     for n in range(maxiter):
#         if abs(z_) > threshold:
#             return n
#         z_ = z_ * z_ + c
#     return 0
#
#
# @jit
# def mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=250, width=iw, height=ih):
#     r1 = np.linspace(xmin, xmax, width)
#     r2 = np.linspace(ymin, ymax, height)
#     n3 = np.empty((width, height))
#     for i in range(width):
#         for j in range(height):
#             n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], maxiter)
#     return r1, r2, n3


x, y, z = mandelbrot_set(-2.0, 0.5, -1.25, 1.25)
trace = go.Heatmap(x=x,
                   y=y,
                   z=z.T)

data = [trace]

layout = go.Layout(
    title='Mandelbrot Plot',
    width=cw,
    height=ch,
    xaxis=dict(
    ),
    yaxis=dict(
        scaleanchor="x",
    ),
)

fig = go.Figure(data=data, layout=layout)


app.layout = html.Div([
    # Title
    html.H2('Zoom Application',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '10px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }),
    html.H2('for',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '20px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '2.0rem',
                'color': '#4D637F'
            }),
    html.H2('MandelBrot',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '27px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }),

    html.Br(),

    html.Div([

        dcc.Graph(
            id='graph',
            figure=fig
        ),

        dcc.Slider(
            id='iterations',
            min=0,
            max=500,
            marks={
                0: {'label': '0'},
                50: {'label': '50'},
                100: {'label': '100'},
                150: {'label': '150'},
                200: {'label': '200'},
                250: {'label': '250'},
                300: {'label': '300'},
                350: {'label': '350'},
                400: {'label': '400'},
                450: {'label': '450'},
                500: {'label': '500'},
            },
            value=250,
        ),
    ])
])


@app.callback(
    Output('graph', 'figure'),
    [Input('iterations', 'value'),
     Input('graph', 'relayoutData')])
def display_selected_data(iterations, relayoutData):
    if relayoutData is None:
        xmin, xmax, ymin, ymax = -2.0, 0.5, -1.25, 1.25
    else:
        xmin = relayoutData['xaxis.range[0]']
        xmax = relayoutData['xaxis.range[1]']
        ymin = relayoutData['yaxis.range[0]']
        ymax = relayoutData['yaxis.range[1]']

    start_i = time.time()
    x_, y_, z_ = mandelbrot_set(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, maxiter=iterations)
    print("迭代执行时间 {} 秒".format(round(time.time() - start_i, 2)))
    start_i = time.time()
    trace_ = go.Heatmap(x=x_,
                        y=y_,
                        z=z_.T)

    data_ = [trace_]

    layout_ = go.Layout(
        title='Mandelbrot Plot',
        width=cw,
        height=ch,
        xaxis=dict(
        ),
        yaxis=dict(
            scaleanchor="x",
        ),
    )

    fig_ = go.Figure(data=data_, layout=layout_)
    print("渲染执行时间 {} 秒".format(round(time.time() - start_i, 2)))
    return fig_


if __name__ == '__main__':
    app.run_server(debug=True)
