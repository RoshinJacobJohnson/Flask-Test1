import pandas as pd


def measurements(fitness,size):
    df = pd.read_excel('Default_Size_Chart.xlsx', sheet_name='Sheet1')
    df2=df[(df["All in Inches \nFit (Men)"]==fitness) &(df["Size"]==size)]
    dimns={}
    dimns["collar"]=df2["Collar"].tolist()[0]
    dimns["chest"]=df2["Chest"].tolist()[0]
    dimns["waist"]=df2["Waist"].tolist()[0]
    dimns["hip"]=df2["Hip"].tolist()[0]
    dimns["shirt_length"]=df2["Shirt Length"].tolist()[0]
    dimns["sleeve_length"]=df2["Sleeve Length "].tolist()[0]
    dimns["shoulder_width"]=df2["Shoulder(Width)"].tolist()[0]
    dimns["biceps"]=df2["Biceps"].tolist()[0]
    dimns["cuffs"]=df2["Cuffs"].tolist()[0]
    dimns["sleeve_width_armpit"]=df2["Sleeve Width (At Armpit)"].tolist()[0]
    dimns["short_sleeve_length"]=df2["Short Sleeve Length"].tolist()[0]
    return dimns


