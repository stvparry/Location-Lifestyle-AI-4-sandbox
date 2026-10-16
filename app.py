import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Location Lifestyle AI V4", page_icon="🏡", layout="wide")

df = pd.read_csv("locations_master.csv")

DIMENSIONS = [
    "active_life","walking_nature","waterside","learning","culture",
    "food_drink","community","practicality","healthcare","rail",
    "property_value","climate","terrain","heritage","retirement"
]

LABELS = {
    "active_life":"Active Life","walking_nature":"Walking & Nature",
    "waterside":"Waterside Living","learning":"Learning",
    "culture":"Culture","food_drink":"Food & Drink",
    "community":"Community","practicality":"Practicality",
    "healthcare":"Healthcare","rail":"Rail Connectivity",
    "property_value":"Property Value","climate":"Climate",
    "terrain":"Terrain","heritage":"Heritage",
    "retirement":"Retirement Suitability"
}

st.title('🏡 Location Lifestyle AI V4')
st.subheader('Where Should We Consider?')

st.sidebar.header('About Us')
current_location = st.sidebar.selectbox('Current Location', sorted(df['name'].tolist()))
household = st.sidebar.selectbox('Household',['Single','Couple','Family','Retired Couple'])
budget = st.sidebar.slider('Budget (£)',500000,3000000,1900000,50000)
horizon = st.sidebar.selectbox('Planning Horizon',['0–3 Years','3–8 Years','8–15 Years'])

st.sidebar.header('Important Locations')
important_locations = st.sidebar.multiselect('Family / Travel / Healthcare', sorted(df['name'].tolist()))
convenience_weight = st.sidebar.slider('Convenience Importance',0,10,7)

st.header('Lifestyle Priorities')
weights = {}
col1,col2,col3 = st.columns(3)
for i,dim in enumerate(DIMENSIONS):
    tgt=[col1,col2,col3][i%3]
    weights[dim]=tgt.slider(LABELS[dim],0,10,7)

def lifestyle_score(row):
    total=sum(row[d]*weights[d] for d in DIMENSIONS)
    max_possible=sum(weights.values())*10
    return round((total/max_possible)*100,1) if max_possible else 0


def convenience_score(name):
    if not important_locations:
        return 100
    current_idx=df[df['name']==current_location].index[0]
    candidate_idx=df[df['name']==name].index[0]
    diff=abs(candidate_idx-current_idx)
    score=100-min(80,diff)
    return max(score,20)


df['lifestyle_match']=df.apply(lifestyle_score,axis=1)
df['convenience_quotient']=df['name'].apply(convenience_score)
current_score=float(df.loc[df['name']==current_location,'lifestyle_match'].iloc[0])
df['opportunity_gain']=df['lifestyle_match']-current_score
df['balanced_score']=df['lifestyle_match']*0.7+df['convenience_quotient']*0.3

recs=df.sort_values('balanced_score',ascending=False)

st.header('Top Recommendations')
st.dataframe(recs.head(10)[['name','lifestyle_match','convenience_quotient','opportunity_gain','balanced_score']],use_container_width=True)

st.header('Town Explorer')
selected=st.selectbox('Explore a Location',sorted(df['name'].tolist()))
row=df[df['name']==selected].iloc[0]

c1,c2,c3=st.columns(3)
c1.metric('Lifestyle Match',round(row['lifestyle_match'],1))
c2.metric('Convenience Quotient',round(row['convenience_quotient'],1))
c3.metric('Opportunity Gain',round(row['opportunity_gain'],1))

cats=[LABELS[d] for d in DIMENSIONS]
vals=[row[d] for d in DIMENSIONS]
vals.append(vals[0])
rc=cats+[cats[0]]
fig=go.Figure()
fig.add_trace(go.Scatterpolar(r=vals,theta=rc,fill='toself'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,10])),showlegend=False,height=600)
st.plotly_chart(fig,use_container_width=True)

st.info('Family Demo Edition')
