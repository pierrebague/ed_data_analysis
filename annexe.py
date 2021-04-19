
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns



FICHIERS = ["EdStatsCountry.csv","EdStatsCountry-Series.csv","EdStatsData.csv","EdStatsFootNote.csv"
            ,"EdStatsSeries.csv"]
NOUVEAUX_FICHIERS = ["NewEdStatsCountry.csv","NewEdStatsData.csv"]
LOCALISATION ='F:/cour/OC/projet2/'
INDEX = ["secondary","tertiary","school|educationnal","student","inhabitant|household","population","technology|computer|internet"]
VALUES_NOT_WANTED = ["WLD","ARE","LMC","LIC","LMY","UMC","MIC","HIC","NOC","OEC","EUU","EAS","EAP","SAS","OED","ECS","LCN","LAC","LDC","SSF","SSA","ECA","MEA","NAC","HPC","MNA","EMU","ARB","IDN","ZAF"]

def fill_dataframe(dataframe):
#     dataframe.fillna(method='ffill',inplace=True)
    return dataframe.replace(0,np.nan).transpose().fillna(method='ffill').transpose()
                                                   
def sort_dataframe(dataframe,sort_year=''):
    dataframe2 = fill_dataframe(dataframe)
    if sort_year=='':
        best_column_to_sort = most_filled_column(dataframe)
    else:
        best_column_to_sort = sort_year 
        for code in VALUES_NOT_WANTED:
            try:
                dataframe2 = dataframe2.drop([code],axis = 0)
            except:
                pass
    return dataframe2

def print_top_values(dataframe,title,value1,value2,sort_year=''):
    dataframe2 = sort_dataframe(dataframe,sort_year)
    if value1 == 0:
        dataframe3 = dataframe2.head(value2).transpose()
        title = "Top " + str(value2) + " " + title
    else:
        dataframe3 = dataframe2.head(value2).tail(value2 - value1 + 1).transpose()
        title = "Top " + str(value1) + " to " + str(value2) + " " + title
    
#     (dataframe3)
    lines = dataframe3.plot.line().set_title(title)
    

def most_filled_column(dataframe):
    mini = dataframe[dataframe.columns[-1]].isna().sum()
    column_mini = dataframe.columns[-1]
    for column in reversed(dataframe.columns):
        isna_sum = dataframe[column].isna().sum()
        if mini > isna_sum:
            mini = isna_sum
            column_mini = column
    return column_mini
           

def clean_data(dataframe,ratio):
    dataframe2 = dataframe.replace(0,np.nan)
    dataframe3 = dataframe2.dropna(axis = 'columns', how = 'all')
    dataframe4 = ratio_epuration(dataframe3,ratio)
   
    return dataframe4
   
def create_range(dataframe,quantity_print,which_one=-1):
    if quantity_print == 1:
        if which_one == 0:
            return [dataframe.columns[0]]
        elif which_one == -1:
            return [dataframe.columns[-1]]
        else:
            try:
                dataframe[str(which_one)]
            except ValueError:
                print("Non valid column")
    else:
        last_elem = int(dataframe.columns[-1])
        column_nbr = int(len(dataframe.columns))
       
        if column_nbr % (quantity_print - 1) == 0:
            range_step = int(column_nbr / quantity_print)
        else:
            range_step = int(column_nbr / (quantity_print - 1))
        begin_year = last_elem
        for step in range(quantity_print-1):
            begin_year -= range_step
        return range(begin_year,last_elem+1,range_step)


def choropleth_map(dataframe,titre,index=False,year='2001',column='Income Group'):
    if index:
        countries = dataframe.index.tolist()
        z = dataframe[year].tolist()
        titre = titre + year
    elif not index:
        countries = dataframe['Country Code'].tolist()
        z = dataframe[column].tolist()
    layout = dict(geo={'scope': 'world'})
    scl = [[0.0, 'darkblue'],[0.2, 'cornflowerblue'],[0.4, 'cornflowerblue'],\
               [0.6, 'orange'],[0.8, 'orange'],[1.0, 'red']]
    data = dict(
        type='choropleth',
        locations=countries,
        locationmode='ISO-3',
        colorscale=scl,
        autocolorscale = False,
        marker = dict(line = dict (color = 'rgb(0,0,0)', width = 1)),z=z)
    map = go.Figure(data=[data], layout=layout)
    map.update_layout(
    title={
        'text': titre,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },    
        title_font_size=30)
    map.show()

def indicator_name_list(dataframe):
    index = dataframe['Indicator Name'].squeeze()
    variable_list = []
    for regex in INDEX:
        index_temp = index_str_contains(index,dataframe,regex)
        set_temp = set(dataframe[index_temp]['Indicator Name'].unique())
        for variable in variable_list:
            set_temp = set_temp - variable
        print("Pour le regex ",regex," : ",len(set_temp)," variables de trouvé")    
        variable_list.append(set_temp)
    return variable_list


def index_str_contains(index,dataframe,regex_var):
    new_index = index.str.contains(regex_var,case=False,regex=True,na=False)
    return new_index

def take_needed_rows(dataframe,list_values):
    new_dataframe = pd.DataFrame([])
    for value in list_values:
        new_dataframe = pd.concat([new_dataframe,dataframe.loc[dataframe['Indicator Name'] == value]])
    return new_dataframe

# def map_dataframe_list_func(dataframe_in,dataframes_out,list_values,func):
#     for data,elem in zip(dataframes_out,list_values):
#         data = func(dataframe_in,elem)


# def map_group_by(dataframes_in):
#     for dataframe_i in range(len(dataframes_in)):
#         dataframes_in[dataframe_i] = dataframes_in[dataframe_i].groupby(['Country Name']).sum()

       
def sns_graph(fichierESC3):
    sns.set(font_scale=5)
    sns.set_theme(style="darkgrid")
    ax = sns.countplot(x="Income Group",order = ["High","Upper \nmiddle","Lower \nmiddle","Low"],\
                   data = fichierESC3,palette=["tab:red","tab:orange","cornflowerblue","darkblue",]).\
                    set_title("Numbers of countries by income group")



def replace_ESC(dataframe, value_or_number=0):
    if value_or_number == 0:
        new_dataframe = dataframe.replace(["High income: nonOECD","Upper middle income","Lower middle income","High income: OECD","Low income"],["High","Upper \nmiddle","Lower \nmiddle","High","Low"])
    else:
        new_dataframe = dataframe.replace(["High income: nonOECD","Upper middle income","Lower middle income","High income: OECD","Low income"],[5,4,2,5,1])
    return new_dataframe

def to_keep(dataframe,columns_to_keep):
    reduct_dataframe = open_csv(dataframe)
    for column in reduct_dataframe.columns:
        if column not in columns_to_keep:
            reduct_dataframe = reduct_dataframe.drop([column],axis = 1)
    print("nouveau format du fichier : ",reduct_dataframe.shape[0]," lignes et ",reduct_dataframe.shape[1]," colonnes.")
    return reduct_dataframe

def open_csv(num_fichier,index_column="",column_list=""):
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
    print("\n",FICHIERS[num_fichier], " is open")
    print("fichier avec ",fichier_lu.shape[0]," lignes et ",fichier_lu.shape[1]," colonnes.")
    return fichier_lu

def garde_nombre(data_frame):
    df_years = pd.DataFrame()
    for column in data_frame.columns:
        if column.isdigit():
            df_years[column] = data_frame[column]
    return df_years

def tri_col_not_nombre(data_frame):
    df_not_numbers = pd.DataFrame()
    for column in data_frame.columns:
        if not column.isdigit():
            df_not_numbers[column]=data_frame[column]
    return df_not_numbers


def ratio_epuration(data_frame,ratio):
    nb_lignes = data_frame.shape[0]
    tab_isna = data_frame.isna().sum()
    list_index = tab_isna.index.tolist()
    df_epure = pd.DataFrame()
    for index,value in enumerate(tab_isna):
        if value <= nb_lignes * (1 - ratio):
            df_epure[list_index[index]] = data_frame[list_index[index]]
    return df_epure

def print_info_col(data_frame,col_names):
    for column in col_names:
        print('\n' + column)
        print(data_frame[column].nunique(), "n uniques")
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
