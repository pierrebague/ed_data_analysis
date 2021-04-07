import numpy as np
import pandas as pd

fichiers = ["EdStatsCountry.csv","EdStatsCountry-Series.csv","EdStatsData.csv","EdStatsFootNote.csv","EdStatsSeries.csv"]
localisation ='F:/cour/OC/projet2/'



def ouvre_csv(num_fichier,nom_colonne = ""):
    if nom_colonne == "":
        fichierLu = pd.read_csv(localisation + fichiers[num_fichier])
        fichierLu = fichierLu.dropna(axis = 'columns', how = 'all')
        print(fichiers[num_fichier], " is open")
    else:
        fichierLu = pd.read_csv(localisation + fichiers[num_fichier],index_col=nom_colonne)
        fichierLu = fichierLu.dropna(axis = 'columns', how = 'all')
        print(fichiers[num_fichier], " is open")
    return(fichierLu)

def garde_nombre(df):
    dfYears = pd.DataFrame()
    for column in df.columns:
        if column.isdigit():
            dfYears[column] = df[column]
    return(dfYears)

def tri_col_nombre(df):
    dfYears = pd.DataFrame()
    for column in df.columns:
        if column.isdigit():
            dfYears[column] = df[column]
         
    return(dfYears)

def tri_col_not_nombre(df):
    dfNotNumbers = pd.DataFrame()
    for column in df.columns:
        if not column.isdigit():
            dfNotNumbers[column] = df[column]
        
    return(dfNotNumbers)


def ratio_epuration(df,ratio):
    nbLignes = df.shape[0]
    tabIsna = df.isna().sum()
    listIndex = tabIsna.index.tolist()
    dfEpure = pd.DataFrame()
    for index,value in enumerate(tabIsna):
        if value <= nbLignes/ratio:
            dfEpure[listIndex[index]] = df[listIndex[index]]
    return(dfEpure)

def print_info_col(df,col_names):
    for column in col_names:
        print('\n' + column)
        print(df[column].nunique() , "n uniques")
        print(df[column].isna().sum(), "somme des naN dans la colonne")

def print_some_info(df):
	print("shape of the dataframe",df.shape)
	for column in df.columns:
		print('\n' + column)
		print(df[column].nunique() , "n uniques")
		print(df[column].isna().sum(), "somme des naN dans la colonne")
# 		print("Some exemples :\n",df.sample(10,random_state = 16))


def test_nunique_isna(df):
	print("shape of the dataframe",df.shape)
	for column in df.columns:
		print('\n' + column)
		print(df[column].nunique() , "n uniques")
		print(df[column].isna().sum(), "somme des naN dans la colonne")


def print_samples(dataFrame,number_of_rows):
    display(dataFrame.sample(number_of_rows,random_state = 148625))

        
def sup_empty_row(dfdate):
#     tabIsnaCumsum = dfdate.isna().cumsum(axis=1)
#    tabSize = len(dfdate.columns)    
#     lastValues = tabIsnaCumsum.iloc[:,-1:]
#     tab_empty_rows = []
# #    for index,value in reversed(list(enumerate(lastValues.values))):
#     for index,value in enumerate(lastValues.values):
#         if value == tabSize:
#             tab_empty_rows.append(index)
    dfdate = dfdate.dropna(axis = 'index', how = 'all')
#     return(dfNotForDate)

def plotSmt(df,nbValueByGraphe):
    nbValues = df.shape[0]
    columnNb = 0
    for column in df.columns:
        if column.isdigit():  
            if(columnNb % nbValueByGraphe == 0):
                fig = plt.figure()
                ax = plt.axes()
            columnNb += 1
            data = df[column].sort_index()
            max = data.max()
            min = data.min()
            x= np.linspace(min,max,nbValues)
            ax.plot(x,data)
    return()

def part_dataframe(dfenter,mini = 0,maxi = 0):
    if maxi == 0:
        dfpart = dfenter[dfenter.gt(mini)].dropna(axis = 'index',how = 'all')
    elif maxi == -1:
        dfpart = dfenter[dfenter.lt(mini)].dropna(axis = 'index',how = 'all')
    else:
        dfpart = dfenter[dfenter.gt(mini) & dfenter.le(maxi)].dropna(axis = 'index',how = 'all')
    dfpart2 = dfenter.join(dfpart,how ='inner',lsuffix=['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009','2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2020','2025', '2030'])
    return(dfpart2)
        
        
def find_def(df_to_define,df_with_def):
    list_of_index = df_to_define.index
    list_of_id_and_country = list_of_index.split(separator = '_')
    
