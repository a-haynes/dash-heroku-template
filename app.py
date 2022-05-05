%%capture
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

labels = {'sex':'Sex',
          'income':'Income ($)',
          'job_prestige':'Occupational Prestige',
          'education':'Years of Education',
          'socioeconomic_index':'Socioeconomic Index',
          'male_breadwinner':'Level of Agreement',
          'education':'Years of Education',
          'count':'Count',
          'value':'Value',
          'region':'Region',
          'age':'Age',
          'satjob':'Job Satisfaction',
          'relationship':'Working Mother Impact on Relationship',
          'male_breadwinner':'Male Breadwinner',
          'men_bettersuited':'Men Better Suited',
          'child_suffer':'Child Suffers from Mother Working',
          'men_overwork':'Men Overwork'
}
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = '''
### What is the gender wage gap?

Source: https://pubs.aeaweb.org/doi/pdfplus/10.1257/jel.20160995

Simply put, the gender wage gap refers to the disparity between compensation between men and women. There are a handful of variables that factor into this, such as labor participation rate, bias in industry sleection, work experience, education, and much more. However, despite factoring in as many material variables as possible, there still remains an unexplained variance. Since women began entering the workforce in much larger numbers since the conclusion World War II the wage gap has fluctuated and overall has lessened. The convergence of compensation has begun to slow in recent years. Futhermore, while the raw wage gap has decreased, most of this change can be explained by the increase of favorable indicators in women, such as work experience and years of education. The unexplained variance has remained mostly constant over the last few decades and has even slightly widened.

### What is the GSS?

Source: https://www.gss.norc.org/About-The-GSS
        https://en.wikipedia.org/wiki/General_Social_Survey

The General Social Survey (GSS) is a survey that spans over the last five decades as a means of gauging the contemporary sentiments of sociological and attitudinal topics. The survey is currently conducted every other year through a face-to-face interview with subjects lasting approximately 90 minutes. A few thousand subjects are randomly sampled to voluntarily participate in the main study. Since it's iteration, over 5,900 variables have been collected. This particular dashboard will focus on 17 factors related to the gender wage gap matter.
'''

gss_prob_2 = gss_clean.groupby('sex', sort=False).agg({'income':'mean',
                                    'job_prestige':'mean',
                                    'education':'mean',
                                    'socioeconomic_index':'mean'})
gss_prob_2 = gss_prob_2.reset_index()
gss_prob_2 = gss_prob_2.rename({'sex':'Sex','income':'Income','job_prestige':'Occupational Prestige','education':'Years of Education','socioeconomic_index':'Socioeconomic Index'}, axis=1)
gss_prob_2 = gss_prob_2.replace({'male': 'Male', 'female': 'Female'})
gss_prob_2.style.hide(axis='index').format(precision=2) # Can't actually pass this ):
gss_prob_2.iloc[:,0:] = gss_prob_2.iloc[:,0:].round(2)
table = ff.create_table(gss_prob_2)

fig_scatter = px.scatter(gss_clean.head(200), x='job_prestige', y='income', 
                 color = 'sex',
                 trendline="lowess", trendline_options=dict(frac=0.9),
                 height=600, width=600,
                 labels=labels,
                 hover_data=['education', 'socioeconomic_index'],
                color_discrete_map = {'male':'blue', 'female':'red'})
fig_scatter.update(layout=dict(title=dict(x=0.5)))

fig_box_income = px.box(gss_clean, x="sex", y="income",  labels=labels, color = 'sex',width=800, height=400,
            color_discrete_map = {'male':'blue', 'female':'red'})
fig_box_income.update_layout(
    showlegend=False,
    width=400,
    height=400)
fig_box_income.update_xaxes(visible=False)

fig_box_job = px.box(gss_clean, x="sex", y="job_prestige",  labels=labels, color = 'sex',width=800, height=400,
            color_discrete_map = {'male':'blue', 'female':'red'})
fig_box_job.update_layout(
    showlegend=False,
    width=400,
    height=400)
fig_box_job.update_xaxes(visible=False)

gss_prob_6 = gss_clean[['sex','income','job_prestige']]
gss_prob_6['job_prestige_bin'] = pd.qcut(gss_prob_6['job_prestige'],6,
                                         labels=["Bottom 6th", "Lower 6th", "Mid-Low 6th","Mid-High 6th","Higher 6th","Top 6th"])
gss_prob_6 = gss_prob_6[~gss_prob_6.job_prestige_bin.isnull()]
fig_box_facet = px.box(gss_prob_6, x="sex", y="income", facet_col='job_prestige_bin',facet_col_wrap=2, labels=labels, color = 'sex',
            category_orders={"job_prestige_bin": ["Bottom 6th", "Lower 6th", "Mid-Low 6th","Mid-High 6th","Higher 6th","Top 6th"]},
            width=800, height=800,
            color_discrete_map = {'male':'blue', 'female':'red'})
fig_box_facet.update_xaxes(visible=False)
fig_box_facet.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_bin=", "")))

ft_columns =['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'] 
cat_columns = ['sex', 'region', 'education'] 
gss_ft = gss_clean[ft_columns + cat_columns].dropna()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Diving into the Gender Wage Gap through the General Social Survey"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Gender Wage Gap Table"),
        
        dcc.Graph(figure=table),
        
        html.H2("Income Scatterplot"),
        
        dcc.Graph(figure=fig_scatter),
        
        html.Div([
            
            html.H2("Income Boxplot by Sex"),
            
            dcc.Graph(figure=fig_box_income)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Occupational Prestige Boxplot by Sex"),
            
            dcc.Graph(figure=fig_box_job)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Income Boxplots Stratified by Job Prestige Sextile"),
        
        dcc.Graph(figure=fig_box_facet),
        
        html.H2("User-Selected Barchart"),
        
        html.Div([
            
            html.H3("Aggregated Feature"),
            
            dcc.Dropdown(id='agg_ft',
                         options=[{'label': i, 'value': i} for i in ft_columns],
                         value='relationship'),
            
            html.H3("Stratifying Feature"),
            
            dcc.Dropdown(id='strat_ft',
                         options=[{'label': i, 'value': i} for i in cat_columns],
                         value='sex'),
        
        ], style={'width': '25%', 'float': 'left'}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'})
    
    ]
)
@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='agg_ft',component_property="value"),
                   Input(component_id='strat_ft',component_property="value")])


def make_figure(agg_ft, strat_ft):
    return px.bar(
        gss_clean.groupby([agg_ft, strat_ft]).size().reset_index().rename({0:'count'}, axis=1), 
        barmode='group',
        labels=labels,
        x=agg_ft,
        y='count',
        color=strat_ft,
        hover_data=[agg_ft, strat_ft, 'count'],
        width=1000, height=600
)

if __name__ == '__main__':
    app.run_server(debug=True)




