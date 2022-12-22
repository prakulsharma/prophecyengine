import os

os.environ['TRAINING_OUTPUT_PATH'] = '../../models'
from analyticexecution.analytic_model import DataPayload
import plotly.graph_objs as go
from analytic import Analytic
from config.analytic_config import AnalyticConfig
import pandas as pd
import json
import time


def out_json_to_csv(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    d = data['outputs']
    df = pd.DataFrame(columns=[x for x in d[0]['context'].keys()])
    for point in d:
        if point['channelKey'] != 'alert_indicator' and point['channelKey'] != 'ade_threshold':
            df.loc[point['ts']] = {key: val['value'] for key, val in point['context'].items()}

    df['anomaly_score'] = [x['value'] for x in d if (x['channelKey'] != 'alert_indicator' and
                                                     x['channelKey'] != 'ade_threshold')]
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df.to_csv(filename.replace('.json', '') + '.csv', index_label='datetime')

    return df


def plot_anomaly_score_chart(df, debug=False, h=400, w=1100):
    df_score = df[['anomaly_score']].copy()
    df_score['th'] = (df_score['anomaly_score'] > 1).astype(int)
    df_score['block'] = (df_score['th'] != df_score['th'].shift(1)).cumsum()
    unique_block = df_score['block'].unique()
    fig = go.Figure()
    for i in unique_block:
        df_u = df_score[df_score['block'] == i]
        if df_u['anomaly_score'].mean() > 1:

            fig.add_trace(go.Scatter(x=df_u.index, y=df_u['anomaly_score'],
                                     fill='tozeroy', mode='none', fillcolor='#F39C12'))
        else:
            fig.add_trace(go.Scatter(x=df_u.index, y=df_u['anomaly_score'],
                                     fill='tozeroy', mode='none', fillcolor='#A3E4D7'))

    fig.update_yaxes(title_text='Anomaly Score')
    fig.update_layout(title={
        'text': "Anomaly Score Chart",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False, height=h, width=w)
    if debug:
        fig.show()
    return fig


def cf_barchart_with_slider(df, debug=False):
    fig1 = go.Figure()
    for t in df.index:
        cf_all = df.loc[t, :]
        cf_all.sort_values(ascending=False, axis=0, inplace=True)
        cf_5 = cf_all[:5]
        fig1.add_trace(go.Bar(x=cf_5.index, y=cf_5.values, visible=False, name=str(cf_5.name)))

    fig1.data[0].visible = True

    steps = []
    for i, t in enumerate(df.index):
        step = dict(
            method="update",
            label="",
            args=[{"visible": [False] * len(fig1.data)},
                  {"title": "Selected Timestamp: " + str(t)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Timestep: "},
        pad={"t": 50},
        steps=steps
    )]

    fig1.update_layout(
        sliders=sliders
    )

    if debug:
        fig1.show()

    return fig1


def cf_barchart(df, slider_pos, int_index=True, h=400, w=1100):
    if int_index:
        cf_all = df.iloc[slider_pos, :]
    else:
        cf_all = df.loc[slider_pos, :]
    cf_all.sort_values(ascending=False, axis=0, inplace=True)
    cf_5 = cf_all[:5]

    fig = go.Figure()

    colors = []
    for val in cf_5.values:
        if val >= 25:
            colors.append('#D55E00')
        elif 25 > val >= 10:
            colors.append('#E69F00')
        elif 10 > val >= 5:
            colors.append('#F0E441')
        elif val < 5:
            colors.append('#009E73')
    fig.add_trace(go.Bar(x=cf_5.index, y=cf_5.values, visible=True, name=str(cf_5.name),
                         marker_color=colors))
    fig.update_layout(title={
        'text': "CF at timestamp " + str(cf_5.name),
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        yaxis_title="% Contributions",
        height=h,
        width=w
    )

    return fig


def train_workbench(df, param_ui,
                    config_yml_path="../../config/air_comp_config.yaml",
                    trained_model_path='ogc_trained_artifacts'):
    analytic_config = AnalyticConfig(config_yml_path=config_yml_path, verbose=True)
    config_dict = analytic_config.get_config()
    train_param = config_dict.get('train_param')
    model_name = config_dict.get('model_name')
    print("For train")
    print("Default param")
    print(train_param)
    if param_ui:
        train_param.update(param_ui)
        print("New param")
        print(train_param)
    if trained_model_path:
        train_param['trained_model_path'] = trained_model_path
    else:
        train_param['trained_model_path'] = None

    # Load data
    df_data = df.dropna()

    # Create training payload
    training_payload = DataPayload()
    training_payload.df = df_data.copy()
    training_payload.parameters = train_param
    training_payload.model_name = model_name

    # call training
    e = Analytic()
    out = e.train(training_payload)
    return out


def score_workbench(df_data, param_ui,
                    config_yml_path="../../config/air_comp_config.yaml",
                    outpath="../../output/score.json",
                    trained_model_fpath=None):
    config_dict = AnalyticConfig(config_yml_path=config_yml_path, verbose=True).get_config()
    score_param = config_dict.get('score_param')
    print("For score")
    print("Default param")
    print(score_param)
    if param_ui:
        score_param.update(param_ui)
        print("New param")
        print(score_param)
    model_name = config_dict.get('model_name')
    score_output_fpath = config_dict.get('score_output_fpath')
    local_train_score = config_dict.get('local_train_score')
    trained_model_path = config_dict.get('trained_model_path')
    score_param['local_train_score'] = local_train_score
    score_param['trained_model_path'] = trained_model_path
    if trained_model_fpath:
        score_param['trained_model_path'] = trained_model_fpath

    if outpath:
        score_output_fpath = outpath

    # Create dummy mapping for the local scoring
    dummy_mappings = {}
    imaps = df_data.columns.tolist()
    for imap in imaps:
        dummy_mappings.update({imap: ('-1', imap)})
    dummy_mappings.update({'anomaly_score': ('-1', 'anomaly_score')})
    dummy_mappings.update({'alert_indicator': ('-1', 'alert_indicator')})
    dummy_mappings.update({'anomaly_threshold': ('-1', 'ade_threshold')})

    # Create input payload
    score_input_payload = DataPayload()
    score_input_payload.df = df_data.copy()
    score_input_payload.parameters = score_param
    score_input_payload.mappings = dummy_mappings
    score_input_payload.model_name = model_name

    # score analytic
    e = Analytic()
    score_output_payload = e.score(score_input_payload)

    # write output in a file
    with open(score_output_fpath, 'w') as f:
        f.write(score_output_payload.to_json())
    df_output = out_json_to_csv(score_output_fpath)
    fig1 = plot_anomaly_score_chart(df_output)
    return df_output, df_output.shape[0] - 1, fig1
