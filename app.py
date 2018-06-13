#################################################
# Import Dependencies
#################################################
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func

import numpy as np

from flask import Flask, render_template, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Queries Setup
#################################################
# Create engine using the RestonDev.sqlite database file
engine = create_engine("sqlite:///static/resources/data/RestonDev.sqlite")

# Create a connection to the engine called `conn`
conn = engine.connect()
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
# Print all of the classes mapped to the Base
Base.classes.keys()
# Assign the classes
Existing = Base.classes.Existing
PlanMax = Base.classes.PlanMax
ExApp = Base.classes.ExApp
ExURApp = Base.classes.ExURApp

# Create a session
session = Session(engine)

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return render_template('index.html')

csvdata = pd.read_csv("static/resources/data/summaryData.csv")

## Route to create dropdownlists
@app.route("/selectlist")
def get_select_list():
    
    data = csvdata.sort_values('TSA')
    data_selectlist = data[['TSA','Dis_SubDis', 'LUCategory']]
    data_selectlist.reset_index(inplace=True, drop=True)
    
    initial_val = "Herndon TSA"
    district_list = ["Select"]
    landuse_list = ["Select"]
    final_list = {}
    final_list['district'] = []
    final_list['landuse'] = []

    for row1 in range(len(data_selectlist.TSA)-1):
        if data_selectlist.TSA[row1] == initial_val:
            if data_selectlist.Dis_SubDis[row1] not in district_list:
                district_list.append(data_selectlist.Dis_SubDis[row1])
            if data_selectlist.LUCategory[row1] not in landuse_list:
                landuse_list.append(data_selectlist.LUCategory[row1])
        
        else:
            final_list['district'].append(district_list)
            final_list['landuse'].append(landuse_list)        
            initial_val = data_selectlist.TSA[row1]
            district_list = ["Select"]
            landuse_list = ["Select"]
    final_list['district'].append(district_list) 
    final_list['landuse'].append(landuse_list)

    select_dropdown_list = {"Herndon TSA":{"district":final_list['district'][0],"landuse":final_list['landuse'][0]},
                "Reston Town Center TSA":{"district":final_list['district'][1],"landuse":final_list['landuse'][1]},
                "Wiehle-Reston East TSA":{"district":final_list['district'][2],"landuse":final_list['landuse'][2]}}
        
    return jsonify(select_dropdown_list)


@app.route("/unique")
def unique():
    
    unique_id=[]
    for unique in csvdata["UniqueID"]:
        u = unique.replace(" ", "")
        u = u.replace(":","")
        u = u.replace("-","")
        unique_id.append(u)
    return (jsonify(unique_id))

@app.route("/areaSelection/<selectionString>")
def areaSelection(selectionString):
    TSA = ""
    DistSubDist = ""
    LUCategory = ""
    
    if (len(selectionString)>2):
        userSelection = selectionString.split("_")  ### ',' character not allowed in filenames http protocol change to '_'
        TSA = userSelection[0]
        DistSubDist = userSelection[1]
        LUCategory = userSelection[2]
        
    # Filter strings   
    EX_FilterString = ""
    PlanMax_FilterString = ""
    EXApp_FilterString = ""
    EXURApp_FilterString = ""
    
    
    if TSA != "":
        EX_FilterString = "Existing.TSA == '" + TSA + "'"
        PlanMax_FilterString = "PlanMax.TSA == '" + TSA + "'"
        EXApp_FilterString = "EXApp.TSA == '" + TSA + "'"
        EXURApp_FilterString = "EXURApp.TSA == '" + TSA + "'"
        
    if DistSubDist != "":
        if TSA != "":
            EX_FilterString = EX_FilterString +" AND Existing.Dis_SubDis == '" + DistSubDist + "'"
            PlanMax_FilterString = PlanMax_FilterString +" AND PlanMax.Dis_SubDis == '" + DistSubDist + "'"
            EXApp_FilterString = EXApp_FilterString +" AND EXApp.Dis_SubDis == '" + DistSubDist + "'"
            EXURApp_FilterString = EXURApp_FilterString +" AND EXURApp.Dis_SubDis == '" + DistSubDist + "'"
        else:
            EX_FilterString ="Existing.Dis_SubDis == '" + DistSubDist + "'"
            PlanMax_FilterString = "PlanMax.Dis_SubDis == '" + DistSubDist + "'"
            EXApp_FilterString = "EXApp.Dis_SubDis == '" + DistSubDist + "'"
            EXURApp_FilterString = "EXURApp.Dis_SubDis == '" + DistSubDist + "'"
        
    if LUCategory != "":
        if TSA != "" or DistSubDist != "":
            EX_FilterString = EX_FilterString +" AND Existing.LUCategory == '" + LUCategory + "'"
            PlanMax_FilterString = PlanMax_FilterString +" AND PlanMax.LUCategory == '" + LUCategory + "'"
            EXApp_FilterString = EXApp_FilterString +" AND EXApp.LUCategory == '" + LUCategory + "'"
            EXURApp_FilterString = EXURApp_FilterString +" AND EXURApp.LUCategory == '" + LUCategory + "'"
        elif TSA == "" and DistSubDist == "":
            EX_FilterString = "Existing.LUCategory == '" + LUCategory + "'"
            PlanMax_FilterString = "PlanMax.LUCategory == '" + LUCategory + "'"
            EXApp_FilterString = "EXApp.LUCategory == '" + LUCategory + "'"
            EXURApp_FilterString = "EXURApp.LUCategory == '" + LUCategory + "'"
            
    ExistingData = session.query(Existing.Scenario,func.sum(Existing.Office).label('Office'),\
                                func.sum(Existing.Retail).label('Retail'),\
                                func.sum(Existing.Hotel).label('Hotel'),\
                                func.sum(Existing.Institutional).label('Institutional'),\
                                func.sum(Existing.Industrial).label('Industrial'),\
                                func.sum(Existing.Nonresidential_GFA).label('Nonresidential_GFA'),\
                                func.sum(Existing.Residential_GFA).label('Residential_GFA'),\
                                func.sum(Existing.Residential_Units).label('Residential_Units')).filter(EX_FilterString).\
                                group_by(Existing.Scenario).all()
                                
    PlanMaxData = session.query(PlanMax.Scenario,func.sum(PlanMax.Office).label('Office'),\
                                func.sum(PlanMax.Retail).label('Retail'),\
                                func.sum(PlanMax.Hotel).label('Hotel'),\
                                func.sum(PlanMax.Institutional).label('Institutional'),\
                                func.sum(PlanMax.Industrial).label('Industrial'),\
                                func.sum(PlanMax.Nonresidential_GFA).label('Nonresidential_GFA'),\
                                func.sum(PlanMax.Residential_GFA).label('Residential_GFA'),\
                                func.sum(PlanMax.Residential_Units).label('Residential_Units')).filter(PlanMax_FilterString).\
                                group_by(PlanMax.Scenario).all()
    
    ExAppData = session.query(ExApp.Scenario,func.sum(ExApp.Office).label('Office'),\
                                func.sum(ExApp.Retail).label('Retail'),\
                                func.sum(ExApp.Hotel).label('Hotel'),\
                                func.sum(ExApp.Institutional).label('Institutional'),\
                                func.sum(ExApp.Industrial).label('Industrial'),\
                                func.sum(ExApp.Nonresidential_GFA).label('Nonresidential_GFA'),\
                                func.sum(ExApp.Residential_GFA).label('Residential_GFA'),\
                                func.sum(ExApp.Residential_Units).label('Residential_Units')).filter(EXApp_FilterString).\
                                group_by(ExApp.Scenario).all()
            
    ExURAppData = session.query(ExURApp.Scenario,func.sum(ExURApp.Office).label('Office'),\
                                func.sum(ExURApp.Retail).label('Retail'),\
                                func.sum(ExURApp.Hotel).label('Hotel'),\
                                func.sum(ExURApp.Institutional).label('Institutional'),\
                                func.sum(ExURApp.Industrial).label('Industrial'),\
                                func.sum(ExURApp.Nonresidential_GFA).label('Nonresidential_GFA'),\
                                func.sum(ExURApp.Residential_GFA).label('Residential_GFA'),\
                                func.sum(ExURApp.Residential_Units).label('Residential_Units')).filter(EXURApp_FilterString).\
                                group_by(ExURApp.Scenario).all()
                                                          
    ExistingDataDF = pd.DataFrame(ExistingData)
    PlanMaxDataDF = pd.DataFrame(PlanMaxData)
    ExAppDataDF = pd.DataFrame(ExAppData)
    ExURAppDataDF = pd.DataFrame(ExURAppData)
    
    Testframes = [ExistingDataDF, PlanMaxDataDF, ExAppDataDF,ExURAppDataDF]
    
    summaryTableDF = pd.concat(Testframes)
    summaryTableDF['Percent Residential'] = round(100*(summaryTableDF['Residential_GFA']/(summaryTableDF['Residential_GFA']+summaryTableDF['Nonresidential_GFA'])))
    summaryTableDF = summaryTableDF.set_index('Scenario')

    summaryTableDF.to_csv("static/resources/data/selection.csv")
    
    #summaryTableDict = summaryTableDF.to_dict('records')
    return jsonify(summaryTableDF.to_html())
    #return jsonify(summaryTableDict)


@app.route("/table/<uniqueid_selection>")
def table(uniqueid_selection):
    data = csvdata
    data['id'] = data['UniqueID'].str.replace(" ","")
    data['id'] = data['id'].str.replace(":","")
    data['UniqueID'] = data['id'].str.replace("-","")

    row_selected = data.loc[data['UniqueID'] == uniqueid_selection]

    off_col = ('EX_OffSQFT', 'MR_OFF_SQFT','EARMR_OffSQFT','EUARMR_OffSQFT')
    ret_col = ('EX_RetSQFT', 'MR_RET_SQFT', 'EARMR_RetSQFT', 'EUARMR_RetSQFT')
    hot_col = ('EX_HotSQFT', 'MR_HOT_SQFT', 'EARMR_HotSQFT', 'EUARMR_HotelSQFT')
    ins_col = ('EX_InstSQFT', 'MR_INS_SQFT', 'EARMR_InstSQFT', 'EUARMR_InstSQFT')
    ind_col = ('EX_IndusSQFT', 'MR_IND_SQFT', 'EARMR_IndusSQFT', 'EUARMR_IndusSQFT')
    res_col = ('EX_ResSQFT', 'MR_ResGFA','EARMR_ResSQFT','EUARMR_ResSQFT')
    office = []
    for col in off_col:
        office.append(row_selected[col].item())
    retail = []
    for col in ret_col:
        retail.append(row_selected[col].item())
    hotel = []
    for col in hot_col:
        hotel.append(row_selected[col].item())
    institute = []
    for col in ins_col:
        institute.append(row_selected[col].item())
    indust = []
    for col in ind_col:
        indust.append(row_selected[col].item())
    residen = []
    for col in res_col:
        residen.append(row_selected[col].item())

    label = ['Existing','Plan','Development','Review']
    
    newtable = {
        'label' : label,
        'Office': office,
        'Retail':retail,
        'Hotel':hotel,
        'Industry':indust,
        'Institutions': institute,
        'Residential':residen}
    newtable_df = pd.DataFrame(newtable)
    newtable_df['Total'] = (newtable_df['Residential']+ newtable_df['Hotel']+ newtable_df['Office']+
                            newtable_df['Institutions']+
                            newtable_df['Retail']+
                            newtable_df['Industry'])                            
    newtable_df['Percent Residential'] = round(100*(newtable_df['Residential']/newtable_df['Total']))
    newtable_df = newtable_df.fillna(0)
    
    filtered_selection = newtable_df.set_index('label')

    filtered_selection.to_csv("static/resources/data/selection.csv")
    

    return jsonify(filtered_selection.to_html())

@app.route("/gauges")
def gauge():
    filtered_selection = pd.read_csv("static/resources/data/selection.csv")
    # check that selection has returned value
    
    if len(filtered_selection) == 0:
        percentages = [0,0,0,0]
        return jsonify(percentages)     
    
    # get the percentages passed to JS
    percentages = []
    for p in filtered_selection["Percent Residential"]:
        percentages.append(p)
    
    print(percentages)
    return jsonify(percentages)

if __name__ == "__main__":
    app.run(debug=True)