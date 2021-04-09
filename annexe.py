import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

FICHIERS = ["EdStatsCountry.csv","EdStatsCountry-Series.csv","EdStatsData.csv","EdStatsFootNote.csv"
            ,"EdStatsSeries.csv"]
NOUVEAUX_FICHIERS = ["NewEdStatsCountry.csv","NewEdStatsData.csv"]
LOCALISATION ='F:/cour/OC/projet2/'



def ouvre_csv(num_fichier,index_column="",column_list=""):
    if index_column == "" and column_list == "":
        fichier_lu = pd.read_csv(LOCALISATION + FICHIERS[num_fichier])
        fichier_lu = fichier_lu.dropna(axis = 'columns', how = 'all')
    elif index_column != "" and column_list != "":
        fichier_lu = pd.read_csv(LOCALISATION + FICHIERS[num_fichier],index_col=index_column,names=column_list)
        fichier_lu = fichier_lu.dropna(axis = 'columns', how = 'all')
    elif index_column == "" and column_list != "":
        fichier_lu = pd.read_csv(LOCALISATION + FICHIERS[num_fichier],names=column_list)
        fichier_lu = fichier_lu.dropna(axis = 'columns', how = 'all')
    else:
        fichier_lu = pd.read_csv(LOCALISATION + FICHIERS[num_fichier],index_col=index_column)
        fichier_lu = fichier_lu.dropna(axis = 'columns', how = 'all')
    print(FICHIERS[num_fichier], " is open")
    print("fichier avec ",fichier_lu.shape[0]," lignes et ",fichier_lu.shape[1]," colonnes.\n")
    return fichier_lu

def garde_nombre(data_frame):
    df_years = pd.DataFrame()
    for column in data_frame.columns:
        if column.isdigit():
            df_years[column] = data_frame[column]
    return df_years

def tri_col_nombre(data_frame):
    df_years = pd.DataFrame()
    for column in data_frame.columns:
        if column.isdigit():
            df_years[column]=data_frame[column]
    return df_years

def tri_col_not_nombre(data_frame):
    df_not_numbers = pd.DataFrame()
    for column in data_frame.columns:
        if not column.isdigit():
            df_not_numbers[column]=data_frame[column]
    return df_not_numbers


def ratio_epuration(data_frame,ratio):
    nb_lignes = data_frame.shape[0]
    tab_is_na = data_frame.isna().sum()
    list_index = tab_is_na.index.tolist()
    df_epure = pd.DataFrame()
    for index,value in enumerate(tab_is_na):
        if value <= nb_lignes/ratio:
            df_epure[list_index[index]] = data_frame[list_index[index]]
    return df_epure

def print_info_col(data_frame,col_names):
    for column in col_names:
        print('\n' + column)
        print(data_frame[column].nunique() , "n uniques")
        print(data_frame[column].isna().sum(), "somme des naN dans la colonne")

def print_some_info(data_frame):
    print("shape of the dataframe",data_frame.shape)
    for column in data_frame.columns:
        print('\n' + column)
        print(data_frame[column].nunique() , "n uniques")
        print(data_frame[column].isna().sum(), "somme des naN dans la colonne")
# print("Some exemples :\n",df.sample(10,random_state = 16))


def test_nunique_isna(data_frame):
    print("shape of the dataframe",data_frame.shape)
    for column in data_frame.columns:
        print('\n' + column)
        print(data_frame[column].nunique() , "n uniques")
        print(data_frame[column].isna().sum(), "somme des naN dans la colonne")


def print_samples(data_frame,number_of_rows):
    display(data_frame.sample(number_of_rows,random_state = 148625))

def sup_empty_row(df_date):
#     tabIsnaCumsum = dfdate.isna().cumsum(axis=1)
#    tabSize = len(dfdate.columns)
#     lastValues = tabIsnaCumsum.iloc[:,-1:]
#     tab_empty_rows = []
# #    for index,value in reversed(list(enumerate(lastValues.values))):
#     for index,value in enumerate(lastValues.values):
#         if value == tabSize:
#             tab_empty_rows.append(index)
    df_date = df_date.dropna(axis = 'index', how = 'all')
#     return(dfNotForDate)

def plot_smt(data_frame,nb_value_by_graphe):
    nb_values = data_frame.shape[0]
    column_nb = 0
    for column in data_frame.columns:
        if column.isdigit():
            if column_nb % nb_value_by_graphe == 0:
                fig = plt.figure()
                axes = plt.axes()
            column_nb += 1
            data = data_frame[column].sort_index()
            maxi = data.max()
            mini = data.min()
            abscissa = np.linspace(mini,maxi,nb_values)
            axes.plot(abscissa,data)
    return()

def part_dataframe(df_enter,mini = 0,maxi = 0):
    if maxi == 0:
        df_part = df_enter[df_enter.gt(mini)].dropna(axis = 'index',how = 'all')
    elif maxi == -1:
        df_part = df_enter[df_enter.lt(mini)].dropna(axis = 'index',how = 'all')
    else:
        df_part = df_enter[df_enter.gt(mini) & df_enter.le(maxi)].dropna(axis = 'index',how = 'all')
    df_part2 = df_enter.join(df_part,how ='inner',lsuffix=['2001', '2002', '2003', '2004',
                                                        '2005', '2006', '2007', '2008', '2009',
                                                        '2010','2011', '2012', '2013', '2014',
                                                        '2015', '2016','2017', '2020','2025',
                                                        '2030'])
    return df_part2

# def find_def(df_to_define,df_with_def):
#     list_of_index = df_to_define.index
#     list_of_id_and_country = list_of_index.split(separator = '_')