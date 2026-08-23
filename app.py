from pathlib import Path
import json
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Predicting Customer Demand to Help UAE Retailers Plan Their Inventory", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'

@st.cache_data
def jload(name):
    with open(DATA/name,'r',encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def cload(name):
    p=DATA/name
    return pd.read_csv(p) if p.exists() else None

d=jload('dashboard_data.json')
q=jload('data_quality_report.json')
sample=cload('cleaned_sample_20k.csv')
rfm_customers=cload('week4_customer_rfm_segments_powerbi.csv')
rfm_summary=cload('week4_rfm_segment_summary.csv')
rfm_validation=cload('week4_rfm_validation_metrics.csv')
final_model=cload('week6_final_model_summary.csv')
inv_summary=cload('week6_inventory_summary_powerbi.csv')
inv_assumptions=cload('week6_inventory_assumptions.csv')
inv_backtest=cload('week6_inventory_backtest_summary.csv')
roadmap=cload('week7_three_year_roadmap.csv')
rfm_recs=cload('week7_rfm_business_recommendations.csv')
limitations=cload('week7_project_limitations.csv')
inv_auto=cload('week7_inventory_automation.csv')
forecast_rollout=cload('week7_forecasting_rollout.csv')
data_gov=cload('week7_data_governance.csv')
if sample is not None and 'InvoiceDate' in sample.columns:
    sample['InvoiceDate']=pd.to_datetime(sample['InvoiceDate'],errors='coerce')

SYM='£'
def money(v):
    if v is None or pd.isna(v): return '—'
    if abs(v)>=1_000_000: return f'{SYM}{v/1_000_000:,.2f}M'
    if abs(v)>=1_000: return f'{SYM}{v/1_000:,.1f}K'
    return f'{SYM}{v:,.0f}'

def pct(v):
    try:
        x=float(str(v).strip().replace('%','')) if isinstance(v,str) else float(v)
        if x<=1: x*=100
        return x
    except Exception:
        return 95.0

def hero(title,subtitle):
    st.markdown(f"""<section class='hero'><div class='eyebrow'>ZAKA · DATA ANALYTICS IN COMMERCE</div><h1>{title}</h1><p>{subtitle}</p></section>""",unsafe_allow_html=True)

def kpi(label,value,note=''):
    st.markdown(f"""<div class='kpi'><div class='klabel'>{label}</div><div class='kvalue'>{value}</div><div class='knote'>{note}</div></div>""",unsafe_allow_html=True)

def insight(title,body,kind='orange'):
    st.markdown(f"""<div class='insight {kind}'><b>{title}</b><span>{body}</span></div>""",unsafe_allow_html=True)

def section(title):
    st.markdown(f"<div class='section-title'>{title}</div>",unsafe_allow_html=True)

def html_table(df, number_cols=None):
    if df is None or len(df)==0:
        return
    x=df.copy()
    number_cols=number_cols or []
    for c in number_cols:
        if c in x.columns:
            x[c]=x[c].apply(lambda v: f"{v:,.2f}" if isinstance(v,(int,float,np.integer,np.floating)) else v)
    st.markdown(x.to_html(index=False, classes='ztable', border=0), unsafe_allow_html=True)

def csv_download(df,label,filename):
    if df is not None:
        st.download_button(label,df.to_csv(index=False).encode('utf-8'),filename,'text/csv')

def print_button():
    components.html("""
    <style>body{margin:0;font-family:Arial,sans-serif}.p{display:flex;justify-content:flex-end}.b{border:0;border-radius:12px;padding:10px 16px;background:linear-gradient(90deg,#f28a2e,#ffc94a);color:#fff;font-weight:700;cursor:pointer;box-shadow:0 5px 14px rgba(242,138,46,.18)}.b:hover{filter:brightness(.98)}</style>
    <div class='p'><button class='b' onclick='window.parent.print()'>⇩ Export current page as PDF</button></div>
    """,height=48)

st.markdown("""
<style>
:root{--o:#F28A2E;--o2:#FF9E3D;--a:#FFB94D;--y:#FFD35A;--cream:#FFF9EF;--paper:#FFFFFF;--ink:#292016;--muted:#836D58;--line:#F2E3D1;}
.stApp{background:linear-gradient(180deg,#FFFDF9 0%,#FFF8ED 100%)}
.block-container{padding-top:.55rem;padding-bottom:3rem;max-width:1480px}
[data-testid='stSidebar']{display:none} header[data-testid='stHeader']{background:transparent}
.hero{padding:28px 31px;border-radius:25px;background:linear-gradient(112deg,#F47F24 0%,#FFA33C 48%,#FFD15A 100%);color:white;margin:5px 0 14px;box-shadow:0 14px 32px rgba(240,138,46,.20);border:1px solid rgba(255,255,255,.5)}
.eyebrow{font-size:.74rem;letter-spacing:.17em;font-weight:850;color:#fff8ec}.hero h1{font-size:2.2rem;margin:.3rem 0 .42rem;font-weight:850}.hero p{margin:0;max-width:1080px;color:#fffdfa;font-size:1rem}
.kpi{background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px 18px;min-height:112px;box-shadow:0 5px 18px rgba(97,58,18,.055)}.klabel{font-size:.74rem;font-weight:850;letter-spacing:.065em;text-transform:uppercase;color:#98795b}.kvalue{font-size:1.72rem;font-weight:850;color:#2c2118;margin-top:7px}.knote{font-size:.78rem;color:#aa8f75;margin-top:4px}
.section-title{font-size:1.22rem;font-weight:850;color:#2a2018;margin:18px 0 10px}.insight{display:flex;gap:8px;padding:14px 16px;border-radius:14px;margin:10px 0;color:#503822}.insight.orange{background:#FFF0E1;border-left:5px solid #F28A2E}.insight.yellow{background:#FFF7D6;border-left:5px solid #FFD35A}.insight b{white-space:nowrap}.insight span{line-height:1.45}
.stButton>button{height:58px;border-radius:15px;border:1px solid #F1DEC6;background:#fff;color:#4b3523;font-weight:800;box-shadow:0 4px 12px rgba(82,49,17,.045);white-space:normal}.stButton>button:hover{border-color:#F28A2E;color:#F28A2E;background:#FFF9F2}.stButton>button:focus{border-color:#F28A2E;color:#F28A2E;box-shadow:0 0 0 2px rgba(242,138,46,.12)}
.stDownloadButton>button{border:0;border-radius:12px;background:linear-gradient(90deg,#F28A2E,#FFC94A);color:#fff;font-weight:800}
[data-testid='stDataFrame']{border:1px solid var(--line);border-radius:14px;overflow:hidden}
@media print{header,[data-testid='stToolbar'],.stButton,iframe{display:none!important}.block-container{max-width:none;padding:0!important}.hero{box-shadow:none}.stApp{background:#fff!important}div[data-testid='stVerticalBlock']{break-inside:auto}div[data-testid='column']{break-inside:avoid}.js-plotly-plot{break-inside:avoid}.kpi{box-shadow:none}.main{overflow:visible!important}}

.ztable{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;font-size:.9rem}
.ztable th{background:#FFF4E5;color:#6f4d2d;text-align:left;padding:11px 12px;font-weight:850;border-bottom:1px solid var(--line)}
.ztable td{padding:10px 12px;border-bottom:1px solid #F7EBDD;color:#3f3125}
.ztable tr:last-child td{border-bottom:0}
</style>
""",unsafe_allow_html=True)

NAV=[('Overview','⌂'),('Sales','↗'),('Products','◇'),('Customers','◎'),('Demand Forecast','∿'),('Inventory Insights','▣'),('Strategy','◫'),('Data Quality','✓'),('About','')]
if 'page' not in st.session_state:
    st.session_state.page='Overview'
cols=st.columns(9)
for i,(name,ico) in enumerate(NAV):
    with cols[i]:
        if st.button(f'{ico}  {name}',key='n_'+name,use_container_width=True):
            st.session_state.page=name
page=st.session_state.page
print_button()

if page=='Overview':
    hero('Predicting Customer Demand to Help UAE Retailers Plan Their Inventory','A decision-support view connecting commerce performance, customer behaviour, product priority, forecasting and inventory planning using the public Online Retail II dataset.')
    k=d['kpis']; c=st.columns(4)
    with c[0]: kpi('Total Revenue',money(k['total_revenue']),'Clean product-sales revenue')
    with c[1]: kpi('Orders',f"{k['total_orders']:,}",'Completed invoices')
    with c[2]: kpi('Customers',f"{k['total_customers']:,}",'Identified customer IDs')
    with c[3]: kpi('Products',f"{k['total_products']:,}",'Active SKUs')
    c=st.columns(4)
    with c[0]: kpi('Units Sold',f"{k['total_units']:,}")
    with c[1]: kpi('Average Order Value',money(k['avg_order_value']))
    with c[2]: kpi('Countries',f"{k['n_countries']:,}")
    with c[3]: kpi('UK Revenue Share',f"{d['uk_revenue_share']:.1f}%")
    m=pd.DataFrame(d['monthly']); m['month']=pd.to_datetime(m['month']); cats=pd.DataFrame(d['by_category']).sort_values('revenue')
    c1,c2=st.columns([1.6,1])
    with c1:
        fig=px.area(m,x='month',y='revenue',markers=True,title='Monthly Revenue Trend',color_discrete_sequence=['#F28A2E']); fig.update_layout(xaxis_title='',yaxis_title='Revenue',hovermode='x unified'); st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig=px.bar(cats,x='revenue',y='category',orientation='h',title='Revenue by Category',color_discrete_sequence=['#FFB94D']); fig.update_layout(xaxis_title='Revenue',yaxis_title=''); st.plotly_chart(fig,use_container_width=True)
    insight('Decision signal:','Revenue builds into the Q4 gifting period, so seasonality is a key planning signal for stock and purchasing.','orange')

elif page=='Sales':
    hero('Sales Performance','Explore seasonality, trading rhythm and geographic contribution to historical retail revenue.')
    k=d['kpis']; c=st.columns(4)
    with c[0]: kpi('Revenue',money(k['total_revenue']))
    with c[1]: kpi('Orders',f"{k['total_orders']:,}")
    with c[2]: kpi('Average Order Value',money(k['avg_order_value']))
    with c[3]: kpi('Average Items / Order',f"{k['avg_items_per_order']:,.1f}")
    m=pd.DataFrame(d['monthly']);m['month']=pd.to_datetime(m['month']);dow=pd.DataFrame(d['by_dow']);hours=pd.DataFrame(d['by_hour']);countries=pd.DataFrame(d['top_countries_ex_uk']).sort_values('revenue')
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.line(m,x='month',y='revenue',markers=True,title='Monthly Revenue',color_discrete_sequence=['#F28A2E']),use_container_width=True)
    with c2: st.plotly_chart(px.bar(dow,x='day',y='revenue',title='Revenue by Day',color_discrete_sequence=['#FFD35A']),use_container_width=True)
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(hours,x='hour',y='revenue',title='Revenue by Trading Hour',color_discrete_sequence=['#FF9E3D']),use_container_width=True)
    with c2: st.plotly_chart(px.bar(countries,x='revenue',y='country',orientation='h',title='Top Non-UK Markets',color_discrete_sequence=['#F6B73C']),use_container_width=True)
    insight('Commercial read:','Trading is concentrated in weekday working hours. The UK is the dominant market in this public dataset.','yellow')

elif page=='Products':
    hero('Product & ABC Intelligence','Prioritise products by historical unit demand so forecasting and inventory attention follow the products that drive demand.')
    abc=pd.DataFrame([
        {'Class':'A','Products':1056,'ProductPct':21.57,'UnitDemand':8948626,'DemandPct':79.98},
        {'Class':'B','Products':1153,'ProductPct':23.55,'UnitDemand':1679288,'DemandPct':15.01},
        {'Class':'C','Products':2686,'ProductPct':54.87,'UnitDemand':560130,'DemandPct':5.01},
    ])
    top=pd.DataFrame(d['top_products_revenue'])
    a=abc.loc[abc['Class']=='A'].iloc[0]
    c=st.columns(4)
    with c[0]: kpi('Total SKUs',f"{int(abc['Products'].sum()):,}")
    with c[1]: kpi('A-Class SKUs',f"{int(a['Products']):,}",f"{a['ProductPct']:.1f}% of products")
    with c[2]: kpi('A-Class Demand',f"{int(a['UnitDemand']):,} units",f"{a['DemandPct']:.1f}% of unit demand")
    with c[3]: kpi('Top Revenue Product',top.iloc[0]['product'],money(top.iloc[0]['revenue']))
    c1,c2=st.columns(2)
    with c1:
        fig=px.bar(abc,x='Class',y='UnitDemand',text='DemandPct',title='ABC Demand Contribution',color='Class',
                   color_discrete_map={'A':'#F28A2E','B':'#FFB94D','C':'#FFE18B'})
        fig.update_traces(texttemplate='%{text:.1f}%')
        fig.update_layout(yaxis_title='Historical Unit Demand',xaxis_title='ABC Class')
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig=px.pie(abc,names='Class',values='Products',hole=.58,title='Product Mix by ABC Class',
                   color='Class',color_discrete_map={'A':'#F28A2E','B':'#FFB94D','C':'#FFE18B'})
        st.plotly_chart(fig,use_container_width=True)
    section('ABC Summary')
    html_table(abc.rename(columns={'ProductPct':'% of Products','UnitDemand':'Unit Demand','DemandPct':'% of Unit Demand'}))
    top10=top.head(10).sort_values('revenue')
    st.plotly_chart(px.bar(top10,x='revenue',y='product',orientation='h',title='Top Products by Revenue',
                           color_discrete_sequence=['#FF9E3D']),use_container_width=True)
    insight('Inventory implication:','A-items represent 21.6% of products and account for approximately 80.0% of historical unit demand. They should receive the tightest forecasting and inventory control.','orange')

elif page=='Customers':
    hero('Customer Intelligence','Use the verified RFM segmentation output to identify customer value, activity and practical engagement priorities.')
    df=rfm_customers.copy(); s=rfm_summary.copy()
    segs=sorted(df.CustomerSegment.dropna().unique())
    chosen=st.multiselect('Customer segments',segs,default=segs)
    f=df[df.CustomerSegment.isin(chosen)].copy()
    c=st.columns(4)
    with c[0]: kpi('Customers',f"{f.CustomerID.nunique():,}")
    with c[1]: kpi('Tracked Revenue',money(f.Monetary.sum()))
    with c[2]: kpi('Average Order Value',money(f.AverageOrderValue.mean()))
    with c[3]: kpi('Recently Active',f"{(f.CustomerStatus.eq('Recently Active').mean()*100):.1f}%")
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.pie(s,names='CustomerSegment',values='Customers',hole=.56,title='Customer Mix',color_discrete_sequence=['#F28A2E','#FF9E3D','#FFB94D','#FFD35A','#FFE4A0']),use_container_width=True)
    with c2:
        ss=s.sort_values('RevenuePct');fig=px.bar(ss,x='RevenuePct',y='CustomerSegment',orientation='h',title='Revenue Share by Segment',color_discrete_sequence=['#F28A2E']);fig.update_layout(xaxis_title='Revenue Share (%)',yaxis_title='');st.plotly_chart(fig,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        fig=px.scatter(f,x='Recency',y='Monetary',color='CustomerSegment',hover_data=['CustomerID','Frequency','AverageOrderValue'],title='Recency vs Customer Value',color_discrete_sequence=['#F28A2E','#FF9E3D','#FFB94D','#FFD35A','#FFE4A0']);fig.update_yaxes(type='log');st.plotly_chart(fig,use_container_width=True)
    with c2:
        ac=f.CustomerStatus.value_counts().rename_axis('Status').reset_index(name='Customers');st.plotly_chart(px.bar(ac,x='Status',y='Customers',title='Customer Activity Status',color_discrete_sequence=['#FFC94A']),use_container_width=True)
    section('Segment Summary');st.dataframe(s,use_container_width=True,hide_index=True)
    section('Top Customers');st.dataframe(f.nlargest(20,'Monetary')[['CustomerID','PrimaryCountry','CustomerSegment','Recency','Frequency','Monetary','AverageOrderValue','CustomerStatus']],use_container_width=True,hide_index=True)
    if rfm_recs is not None:
        section('Business Recommendations');st.dataframe(rfm_recs,use_container_width=True,hide_index=True)
    if rfm_validation is not None:
        section('Segmentation Validation')
        vals=dict(zip(rfm_validation['Metric'],rfm_validation['Value']))
        vc=st.columns(5)
        with vc[0]: kpi('Customers',f"{int(vals.get('Customers',0)):,}")
        with vc[1]: kpi('Clusters',f"{int(vals.get('Clusters',0))}")
        with vc[2]: kpi('Silhouette Score',f"{vals.get('Silhouette Score',0):.3f}")
        with vc[3]: kpi('Calinski-Harabasz',f"{vals.get('Calinski-Harabasz Index',0):,.2f}")
        with vc[4]: kpi('C-Index',f"{vals.get('C-Index',0):.4f}")
    csv_download(f,'Download filtered customer data','customers_filtered.csv')

elif page=='Demand Forecast':
    hero('Demand Forecast','Report the final product-level model and the final aggregate Category A benchmark without mixing in stale earlier experiments.')
    if final_model is not None and len(final_model):
        r=final_model.iloc[0]
        c=st.columns(5)
        with c[0]: kpi('Final Product-Level Model',str(r['FinalModel']),'Selected by lowest WAPE')
        with c[1]: kpi('MAE',f"{float(r['MAE']):.2f}")
        with c[2]: kpi('RMSE',f"{float(r['RMSE']):.2f}")
        with c[3]: kpi('WAPE',f"{float(r['WAPE']):.2f}%")
        with c[4]: kpi('R²',f"{float(r['R2']):.3f}")
    section('Aggregate Category A Comparison')
    agg=pd.DataFrame([
        {'Model':'4-Week Moving Average','MAE':17952.78,'RMSE':24326.16,'WAPE':16.35,'R2':0.373},
        {'Model':'Prophet','MAE':21573.21,'RMSE':31792.92,'WAPE':19.65,'R2':-0.071},
    ])
    c1,c2=st.columns([1.15,1])
    with c1:
        html_table(agg)
    with c2:
        mm=agg.melt(id_vars='Model',value_vars=['MAE','RMSE'],var_name='Metric',value_name='Error')
        fig=px.bar(mm,x='Model',y='Error',color='Metric',barmode='group',title='Aggregate Error Comparison',
                   color_discrete_sequence=['#F28A2E','#FFD35A'])
        fig.update_layout(xaxis_title='',yaxis_title='Error')
        st.plotly_chart(fig,use_container_width=True)
    hist=pd.DataFrame(d['weekly_units_history'])
    if len(hist):
        hist['week']=pd.to_datetime(hist['week'])
        st.plotly_chart(px.line(hist,x='week',y='units',title='Historical Weekly Units',
                               color_discrete_sequence=['#FF9E3D']),use_container_width=True)
    if forecast_rollout is not None:
        section('Forecasting Rollout')
        html_table(forecast_rollout)
    insight('Final interpretation:','The final product-week model is the 4-Week Moving Average. At the aggregate Category A level, the 4-Week Moving Average also outperforms Prophet on MAE, RMSE and WAPE. Earlier aggregate LightGBM results are intentionally excluded because they were not part of the final Colab analysis.','yellow')

elif page=='Inventory Insights':
    hero('Inventory Insights','Translate the final demand forecast into verified inventory-planning outputs while keeping scenario assumptions and unavailable stock data explicit.')
    if inv_summary is not None and len(inv_summary):
        r=inv_summary.iloc[0]
        c=st.columns(4)
        with c[0]: kpi('A Products',f"{int(r['Products']):,}",'Demand-based ABC scope')
        with c[1]: kpi('Forecast Units',f"{float(r['TotalForecastUnits']):,.0f}",'Next forecast week')
        with c[2]: kpi('Historical Coverage',f"{float(r['ObservedBacktestCoveragePct']):.1f}%",'Observed backtest')
        with c[3]: kpi('Final Model Products',f"{int(r['FinalModelProducts']):,}",f"{int(r['FallbackProducts']):,} fallback products")
        c=st.columns(4)
        with c[0]: kpi('Lead Time',f"{float(r['LeadTimeWeeks']):.0f} weeks",'Planning assumption')
        with c[1]: kpi('Target Service Level',f"{float(r['TargetServiceLevelPct']):.0f}%",'Planning assumption')
        z_val=1.645
        if inv_assumptions is not None and 'Assumption' in inv_assumptions.columns:
            zr=inv_assumptions[inv_assumptions['Assumption'].astype(str).str.contains('Z Score',case=False,na=False)]
            if len(zr): z_val=float(zr.iloc[0]['Value'])
        with c[2]: kpi('z-score',f"{z_val:.3f}")
        with c[3]: kpi('Total Reorder Point',f"{float(r['TotalReorderPointUnits']):,.0f} units")
        c=st.columns(2)
        with c[0]: kpi('Total Safety Stock',f"{float(r['TotalSafetyStockUnits']):,.0f} units")
        with c[1]: kpi('Average Reorder Point',f"{float(r['AverageReorderPointUnits']):,.1f} units per product")
        summary_chart=pd.DataFrame([
            {'Measure':'Forecast Units','Units':float(r['TotalForecastUnits'])},
            {'Measure':'Safety Stock','Units':float(r['TotalSafetyStockUnits'])},
            {'Measure':'Reorder Point','Units':float(r['TotalReorderPointUnits'])},
        ])
        st.plotly_chart(px.bar(summary_chart,x='Measure',y='Units',title='Final Inventory Planning Totals',
                               color='Measure',color_discrete_sequence=['#F28A2E','#FFB94D','#FFD35A']),
                        use_container_width=True)
    if inv_assumptions is not None:
        section('Inventory Assumptions')
        html_table(inv_assumptions)
    if inv_backtest is not None:
        section('Historical Inventory Backtest')
        html_table(inv_backtest)
    if inv_auto is not None:
        section('Inventory Automation Workflow')
        html_table(inv_auto)
    insight('Important limitation:','Current stock-on-hand is not available in Online Retail II. The project therefore calculates reorder thresholds and planning quantities, but it does not claim a truthful “reorder now” decision. Product-level detail from the older dashboard JSON has been removed so only final Week 6 outputs are shown.','orange')

elif page=='Strategy':
    hero('Implementation Strategy','Move from a public-data proof of concept toward a validated, integrated and monitored UAE retail implementation.')
    if roadmap is not None:
        section('Three-Year Roadmap');st.dataframe(roadmap,use_container_width=True,hide_index=True,height=300)
    if data_gov is not None:
        section('Data Governance');st.dataframe(data_gov,use_container_width=True,hide_index=True)
    if limitations is not None:
        section('Project Limitations');st.dataframe(limitations,use_container_width=True,hide_index=True)
    insight('Scope boundary:','Online Retail II is public international retail data used to demonstrate the analytical solution. UAE business implications are future implementation opportunities, not observed UAE transaction results.','yellow')

elif page=='About':
    hero('About','Predicting Customer Demand to Help UAE Retailers Plan Their Inventory')
    st.markdown('''
    <div style="background:#fff;border:1px solid #F1DEC6;border-radius:20px;padding:24px 26px;box-shadow:0 6px 18px rgba(82,49,17,.05);line-height:1.7;color:#493624">
    <h3 style="margin-top:0;color:#2a2018">Why this project matters</h3>
    <p>Retailers face a constant inventory trade-off: ordering too much stock ties up money and increases waste, while ordering too little can lead to missed sales. This project explores how historical transaction data can support more structured demand and inventory planning.</p>
    <p>The solution uses the public <b>Online Retail II</b> dataset as a proof of concept. Sales history is prepared for analysis, forecasting models are evaluated, and demand signals are translated into inventory-planning measures such as safety stock and reorder points. These outputs are brought together in one interactive decision-support dashboard.</p>
    <p>The dashboard covers sales trends, product performance, customer segmentation, demand forecasting and inventory insights. The customer layer uses recency, frequency and monetary value (RFM) to help distinguish customer groups and support more targeted business decisions.</p>
    <p><b>Important scope note:</b> the current dataset is public international retail data, not transaction data from a UAE retailer. A future UAE implementation would require validation with real local retailer sales, inventory, supplier and operational data.</p>
    </div>
    ''',unsafe_allow_html=True)
    section('Project Team')
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown('''<div class="kpi"><div class="klabel">PROJECT TEAM</div><div class="kvalue" style="font-size:1.25rem">Naila Alhameli</div><div class="knote">Capstone Project · ZAKA AI</div><div style="margin-top:12px"><a href="https://www.linkedin.com/in/nailaalhameli/" target="_blank" style="color:#F28A2E;font-weight:800;text-decoration:none">LinkedIn ↗</a></div></div>''',unsafe_allow_html=True)
    with c2:
        st.markdown('''<div class="kpi"><div class="klabel">PROJECT TEAM</div><div class="kvalue" style="font-size:1.25rem">Mouza Aldarmaki</div><div class="knote">Capstone Project · ZAKA AI</div><div style="margin-top:12px"><a href="https://www.linkedin.com/in/oj9o/" target="_blank" style="color:#F28A2E;font-weight:800;text-decoration:none">LinkedIn ↗</a></div></div>''',unsafe_allow_html=True)
    with c3:
        st.markdown('''<div class="kpi"><div class="klabel">PROJECT TEAM</div><div class="kvalue" style="font-size:1.25rem">Ibrahim Alzarooni</div><div class="knote">Capstone Project · ZAKA AI</div><div style="margin-top:12px"><a href="https://www.linkedin.com/in/ibrahim-mohamed-alzarooni/" target="_blank" style="color:#F28A2E;font-weight:800;text-decoration:none">LinkedIn ↗</a></div></div>''',unsafe_allow_html=True)
    insight('Models evaluated:','Random Forest, XGBoost, LightGBM and Prophet were used within the project forecasting work, alongside baseline comparison.','yellow')

else:
    hero('Data Quality & Reproducibility','An auditable cleaning ledger keeps every dashboard number traceable to the preparation pipeline.')
    rows=[('Raw combined rows',q['0_raw_combined_rows']),('Cancellations removed',q['1_cancellation_rows_removed']),('Service lines removed',q['2_service_line_rows_removed']),('Duplicate rows removed',q['3_duplicate_rows_removed']),('Non-positive quantity removed',q['4_nonpositive_quantity_removed']),('Non-positive price removed',q['5_nonpositive_price_removed']),('Clean product-sales rows',q['7_clean_product_sales_rows']),('Rows with customer ID',q['8_rows_with_customer_id']),('Rows without customer ID kept for sales',q['9_rows_without_customer_id_kept_for_sales'])]
    qdf=pd.DataFrame(rows,columns=['Step','Rows']);c=st.columns(4)
    with c[0]: kpi('Raw Rows',f"{q['0_raw_combined_rows']:,}")
    with c[1]: kpi('Clean Rows',f"{q['7_clean_product_sales_rows']:,}")
    with c[2]: kpi('Rows with Customer ID',f"{q['8_rows_with_customer_id']:,}")
    with c[3]: kpi('Missing Customer ID',f"{q['9_rows_without_customer_id_kept_for_sales']:,}",'Kept outside RFM')
    html_table(qdf)
    if sample is not None:
        section('Clean Sample Preview');st.dataframe(sample.head(250),use_container_width=True,hide_index=True,height=460)
    insight('Cleaning approach:','Transactions without customer IDs were retained for sales, product and forecasting analysis but excluded from RFM because segmentation requires a customer key.','orange')

st.markdown("<hr><div style='display:flex;justify-content:space-between;color:#a58362;font-size:.78rem;padding-bottom:8px'><span>ZAKA · Data Analytics in Commerce</span><span>Predicting Customer Demand to Help UAE Retailers Plan Their Inventory</span></div>",unsafe_allow_html=True)
