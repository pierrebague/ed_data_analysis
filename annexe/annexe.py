import numpy as np
import pandas as pd

fichiers = ["EdStatsCountry.csv","EdStatsCountry-Series.csv","EdStatsData.csv","EdStatsFootNote.csv","EdStatsSeries.csv"]
localisation ='F:/cour/OC/projet2/'



def ouvre_csv(num_fichier):
    fichierLu = pd.read_csv(localisation + fichiers[num_fichier])
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


def premiere_epuration(df,nbLignes,ratio):
    tabIsna = df.isna().sum()
    listIndex = tabIsna.index.tolist()
    dfEpure = pd.DataFrame()
    for index,value in enumerate(tabIsna):
        if value <= nbLignes/ratio:
            dfEpure[listIndex[index]] = df[listIndex[index]]
    return(dfEpure)


def print_some_info(df)
	print("shape of the dataframe",df.shape)
	for column in df.columns:
		print('\n' + column)
		print(df[column].nunique() , "n uniques")
		print(df[column].isna().sum(), "somme des non nul dans la colonne")
		print("Some exemples :\n"dataFrame.sample(10,random_state = 16))
	
	
def test_nunique_isna(df):
	print("shape of the dataframe",df.shape)
	for column in df.columns:
		print('\n' + column)
		print(df[column].nunique() , "n uniques")
		print(df[column].isna().sum(), "somme des non nul dans la colonne")
	return()



def print_samples(dataFrame):
    print(dataFrame.sample(5))
    return()
        
def sup_empty_row(dfdate,dfNormal):
    dfNormalCopy = dfNormal.copy()
    tabIsnaCumsum = dfdate.isna().cumsum(axis=1)
    tabSize = len(tabIsnaCumsum.columns)    
    lastValues = tabIsnaCumsum.iloc[:,-1:]
    dfNotForDate = pd.DataFrame()
    indexNoteForDate = 0
    for index,value in reversed(list(enumerate(lastValues.values))):
        if value == tabSize:
            dfNotForDate[indexNoteForDate] = dfNormal[index]
            indexNoteForDate += 1
            dfdate = dfdate.drop(index)
            dfNormalCopy = dfNormalCopy.drop(index)
        
    dfNormal = dfNormalCopy        
    return(dfNotForDate)

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

            
