#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pypsa
import pandas as pd


# In[2]:


n = pypsa.Network()


# In[3]:


n.import_from_csv_folder("./CSV")


# In[4]:


#ElmLne

df_ElmLne = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)', 'typ_id(p)',
       'chr_name(a:20)', 'dline(r)', 'fline(r)', 'outserv(i)', 'pStoch(p)',
       'nlnum'])

#fill each column with information from pypsa df
df_ElmLne['FID(a:40)'] = 'LNE_' + n.lines.index.astype(str)
df_ElmLne["OP(a:1)"] = "C"
df_ElmLne["loc_name(a:40)"] = df_ElmLne['FID(a:40)']
df_ElmLne["fold_id(p)"] = "Grid"
df_ElmLne["chr_name(a:20)"] = ['LNE' + str(i+1).zfill(5) for i in range(len(df_ElmLne))]
df_ElmLne["nlnum"] = n.lines.num_parallel.values
df_ElmLne['fline(r)'] = 1
df_ElmLne["outserv(i)"] = 0
df_ElmLne["dline(r)"] = n.lines.length.values
df_ElmLne["typ_id(p)"] = "TYP_" + df_ElmLne["FID(a:40)"]


# In[5]:


#TypLne

df_TypLne = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)',
       'chr_name(a:20)', 'Ithr(r)', 'aohl_(a:3)', 'cline(r)', 'cline0(r)',
       'nlnph(i)', 'nneutral(i)', 'rline(r)', 'rline0(r)', 'rtemp(r)',
       'sline(r)', 'uline(r)', 'xline(r)', 'xline0(r)'])

#fill each column with information from pypsa df
df_TypLne["FID(a:40)"] = df_ElmLne["typ_id(p)"]
df_TypLne["OP(a:1)"] = "C"
df_TypLne["loc_name(a:40)"] = df_TypLne['FID(a:40)']
#df_TypLne["fold_id(p)"] = "Grid"
#df_TypLne["chr_name(a:20)"] = ['LNE' + str(i+1).zfill(5) for i in range(len(df_TypLne))]
#df_TypLne["Ithr(r)"] = ?
#df_TypLne["aohl_a:3)"] = ? keine information, ob cable oder OHL
df_TypLne["cline(r)"] = n.lines.b.values
df_TypLne["nlnph(i)"] = 3
df_TypLne["nneutral(i)"] = 0
df_TypLne["rline(r)"] = n.lines.r.values
#df_TypLne["sline(r)"] = ? no rated current parameter in pypsa model
#df_TypLne["uline(r)"] = ? no rated voltage parameter in pypsa model
df_TypLne["xline(r)"] = n.lines.x.values


# In[6]:


#ElmTerm

df_ElmTerm = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)', 'typ_id(p)',
       'chr_name(a:20)', 'iUsage(i)', 'outserv(i)', 'phtech(i)', 'uknom(r)'])

#fill each column with information from pypsa df
df_ElmTerm['FID(a:40)'] = "BUS_" + n.buses.index.astype(str)
df_ElmTerm["OP(a:1)"] = "C"
df_ElmTerm["loc_name(a:40)"] = df_ElmTerm['FID(a:40)']
df_ElmTerm["fold_id(p)"] = "Grid"
df_ElmTerm["chr_name(a:20)"] = ['TERM' + str(i+1).zfill(5) for i in range(len(df_ElmTerm))]
df_ElmTerm[["iUsage(i)" , "outserv(i)" , "phtech(i)"]] = 0
df_ElmTerm['uknom(r)'] = n.buses.v_nom.values
df_ElmTerm["typ_id(p)"] = "TYP_" + df_ElmTerm["FID(a:40)"]


# In[7]:


#ElmLod

df_ElmLod = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)', 'typ_id(p)',
       'chr_name(a:20)', 'outserv(i)', 'plini(r)', 'qlini(r)', 'scale0(r)'])

#fill each column with information from pypsa df
df_ElmLod['FID(a:40)'] = "LOD_" + n.loads.index.astype(str)
df_ElmLod["OP(a:1)"] = "C"
df_ElmLod["loc_name(a:40)"] = df_ElmLod['FID(a:40)']
df_ElmLod["fold_id(p)"] = "Grid"
df_ElmLod["chr_name(a:20)"] = ['LOD' + str(i+1).zfill(5) for i in range(len(df_ElmLod))]
df_ElmLod["outserv(i)"] = 0
df_ElmLod['plini(r)'] = n.loads.p_set.values
df_ElmLod['qlini(r)'] = n.loads.q_set.values
df_ElmLod['scale0(r)'] = 1
df_ElmLod["typ_id(p)"] = "TYP_" + df_ElmLod["FID(a:40)"]
#ANMERKUNG: Stimmen plini(r) mit p_set und qlini(r) mit q_set überein? Müsste da nicht der Output p,q stehen? (siehe pypsa documentation)


# In[8]:


#TypLod

df_TypLod = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)', 'kpu(r)',
       'kqu(r)', 'phtech(i)', 'systp(i)'])

#fill each column with information from pypsa df
df_TypLod["FID(a:40)"] = df_ElmLod["typ_id(p)"]
df_TypLod["OP(a:1)"] = "C"


# In[17]:


#StaCubic

df_StaCubic = pd.DataFrame(columns = ['FID(a:40)', 'OP(a:1)', 'loc_name(a:40)', 'fold_id(p)',
       'chr_name(a:20)', 'obj_bus(i)', 'obj_id(p)'])

results_data_lines = []

# Iterate over the index of n.buses DataFrame
for bus in n.buses.index:
    # Check if the bus exists in bus0 or bus1 columns of n.lines DataFrame
    lines_with_bus = n.lines[(n.lines['bus0'] == str(bus)) | (n.lines['bus1'] == str(bus))]
    # If lines are found, extract line IDs and store the mapping in results_data
    if not lines_with_bus.empty:
        line_ids = lines_with_bus.index.tolist()
        for line_id in line_ids:
            results_data_lines.append({'Bus': bus, 'obj_id(p)': line_id})


# Create a DataFrame from the list of dictionaries
results_lines = pd.DataFrame(results_data_lines)

# define obj_bus(i): 0-> starting-bus , 1-> ending-bus
results_lines["obj_bus(i)"] = results_lines.duplicated(subset=["obj_id(p)"]).astype(int)

#rename obj_id(p) to differenciate between loads and lines
results_lines["obj_id(p)"] = "LNE_" + results_lines["obj_id(p)"]



results_data_loads = []

# Iterate over the index of n.buses DataFrame
for bus in n.buses.index:
    # Check if the bus exists in bus0 or bus1 columns of n.loads DataFrame
    loads_with_bus = n.loads[(n.loads['bus'] == str(bus))]
    # If loads are found, extract load IDs and store the mapping in results_data
    if not loads_with_bus.empty:
        load_ids = loads_with_bus.index.tolist()
        for loads_id in load_ids:
            results_data_loads.append({'Bus': bus, 'obj_id(p)': loads_id})

# Create a DataFrame from the list of dictionaries
results_loads = pd.DataFrame(results_data_loads)

# define obj_bus(i): 0-> loads are only connected to one bus
results_loads["obj_bus(i)"] = 0

#rename obj_id(p) to differenciate between loads and lines
results_loads["obj_id(p)"] = "LOD_" + results_loads["obj_id(p)"]

results_data_generators = []

# Iterate over the index of n.buses DataFrame
for bus in n.buses.index:
    # Check if the bus exists in bus0 or bus1 columns of n.generators DataFrame
    generators_with_bus = n.generators[(n.generators['bus'] == str(bus))]
    # If generators are found, extract generator IDs and store the mapping in results_data
    if not generators_with_bus.empty:
        gen_ids = generators_with_bus.index.tolist()
        for generators_id in gen_ids:
            results_data_generators.append({'Bus': bus, 'obj_id(p)': generators_id})

# Create a DataFrame from the list of dictionaries
results_generators = pd.DataFrame(results_data_generators)

# define obj_bus(i): 0-> loads are only connected to one bus
results_generators["obj_bus(i)"] = 0

#rename obj_id(p) to differenciate between loads and lines and generators
results_generators["obj_id(p)"] = "GEN_" + results_generators["obj_id(p)"]


#combine loads and lines into one df
stacked_df = pd.concat([results_loads, results_lines, results_generators], ignore_index=True)

# Function to apply the count logic
def assign_values(row):
    prev_value = None
    counter = 1
    value_to_counter = {}
    new_column_values = []
    for value in row:
        if value != prev_value:
            if value not in value_to_counter:
                value_to_counter[value] = counter
                counter += 1
            new_column_values.append(value_to_counter[value])
        else:
            new_column_values.append(value_to_counter[prev_value])
        prev_value = value
    return new_column_values


#fill each column with information from pypsa df lines
df_StaCubic["fold_id(p)"] = stacked_df.Bus.values
df_StaCubic["loc_name(a:40)"] = "Cub " + (df_StaCubic.groupby('fold_id(p)').cumcount() + 1).astype(str)
df_StaCubic = df_StaCubic.sort_values(by = "fold_id(p)")
df_StaCubic['FID(a:40)'] = assign_values(df_StaCubic['fold_id(p)'])
df_StaCubic["FID(a:40)"] = df_StaCubic["loc_name(a:40)"].astype(str) + "_" + df_StaCubic["FID(a:40)"].astype(str)
df_StaCubic["OP(a:1)"] = "C"
df_StaCubic["chr_name(a:20)"] = ['CUB' + str(i+1).zfill(5) for i in range(len(df_StaCubic))]
df_StaCubic["obj_bus(i)"] = stacked_df["obj_bus(i)"]
df_StaCubic["obj_id(p)"] = stacked_df["obj_id(p)"]


# In[10]:


#ElmGenstat

df_ElmGenstat = pd.DataFrame(columns= ['ID(a:40)', 'loc_name(a:40)', 'fold_id(p)', 'ngnum(i)', 'cCategory',
       'chr_name(a:20)', 'outserv(i)', 'sgn', 'cosn', 'pgini(r)', 'qgini(r)',
       'usetp(r)', 'Pmin_uc', 'Pmax_uc'])

# Function to apply the count logic
def enumerate_column(existing_column):
    # Initialize a dictionary to keep track of counts
    counts = {}

    # Function to update counts and format entries
    def update_count(entry):
        nonlocal counts
        if entry not in counts:
            counts[entry] = 1
        else:
            counts[entry] += 1
        return f"{entry}_{str(counts[entry]).zfill(4)}"

    # Apply the function to create the new column
    new_column = existing_column.apply(update_count)
    
    return new_column

#fill each column with information from pypsa df
df_ElmGenstat['ID(a:40)'] = "GEN_" + n.generators.index.astype(str)
df_ElmGenstat["loc_name(a:40)"] = df_ElmGenstat['ID(a:40)']
df_ElmGenstat["fold_id(p)"] = "Grid"
df_ElmGenstat["ngnum(i)"] = 1
df_ElmGenstat["cCategory"] = n.generators.carrier.values
df_ElmGenstat['chr_name(a:20)'] = enumerate_column(n.generators["carrier"]).values
df_ElmGenstat['outserv(i)'] = 0
df_ElmGenstat['sgn'] = n.generators.p_nom_opt.values
df_ElmGenstat['Pmax_uc'] = n.generators.p_max_pu.values
df_ElmGenstat['Pmin_uc'] = n.generators.p_min_pu.values


# In[11]:


#ChaVec

df_ChaVec = pd.DataFrame(columns=['ID(a:40)', 'loc_name(a:40)', 'fold_id(p)', 'scale(p)', 'usage(i)',
       'approx(i)', 'vector:SIZEROW(i)'])

#add time series data of dispatch to df
for i in range(n.generators_t.p.index.size):
    df_ChaVec[f'vector:{i}(r)'] = n.generators_t.p.iloc[i % len(n.generators_t.p)]

df_ChaVec["vector:SIZEROW(i)"] = n.generators_t.p.index.size
df_ChaVec["ID(a:40)"] = "ChaVec_" + df_ChaVec.index


# In[12]:


# ChaRef

df_ChaRef = pd.DataFrame(columns=["ID(a:40)", "loc_name(a:40)","fold_id(p)","typ_id(p)"])

df_ChaRef["typ_id(p)"] = df_ChaVec["ID(a:40)"]
df_ChaRef["ID(a:40)"] = "ChaRef_" + df_ChaRef.index

df_ChaRef


# In[19]:


# Erstelle einen ExcelWriter
with pd.ExcelWriter('output_DGS_format.xlsx', mode='w') as writer:
    # Schreibe jeden DataFrame in ein separates Sheet
    df_ElmTerm.to_excel(writer, sheet_name='ElmTerm', index=False)
    df_ElmLne.to_excel(writer, sheet_name='Elm_Lne', index=False)
    df_ElmLod.to_excel(writer, sheet_name='ElmLod', index=False)
    df_TypLod.to_excel(writer, sheet_name='TypLod', index=False)
    df_TypLne.to_excel(writer, sheet_name='TypLne', index=False)
    df_StaCubic.to_excel(writer, sheet_name='StaCubic', index=False)
    df_ElmGenstat.to_excel(writer, sheet_name='ElmGenstat', index=False)
    df_ChaVec.to_excel(writer, sheet_name='ChaVec', index=False)
    df_ChaRef.to_excel(writer, sheet_name='ChaRef', index=False)


# In[112]:


get_ipython().system('jupyter nbconvert --to script test_notebook.ipynb')

