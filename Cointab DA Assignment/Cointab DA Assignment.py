#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # Importing X company data and analyzing it.

# In[2]:


X_COD = pd.read_excel("K:\Major project\cointab\Assignment details\\X-Order Report.xlsx")
X_COD.info()


# In[3]:


X_COD["Total Order Price (rs.)"] = X_COD["Order Qty"]*X_COD["Item Price(Per Qty.)"]
X_COD.head()


# In[4]:


#Calculating COD charge.

charge = []
for x in X_COD["Payment Mode"]:
    if x == "COD":
        for y in X_COD["Total Order Price (rs.)"]:
        
            if y<=300:
                charge.append(15)
            else:
                charge.append(y*0.05)
    else:
        charge.append(0)
charge[0:400]


# In[5]:


X_COD["COD Charge (Rs.)"] = charge[0:400]
X_COD["COD Charge (Rs.)"] = np.where(X_COD["Payment Mode"]=='Prepaid', 0 ,X_COD["COD Charge (Rs.)"] )
X_COD.head(10)


# In[6]:


X_COD.shape


# In[7]:


X_COD.rename(columns = {"ExternOrderNo":"Order ID"} , inplace = True)


# In[8]:


#Importing weight table.

X_weight = pd.read_excel("K:\Major project\cointab\Assignment details\\X-weight.xlsx")
X_weight.info()


# In[9]:


#conerting weight in gms to KG
X_weight["Weight (g)"] = X_weight["Weight (g)"]/1000


# In[10]:


X_weight.rename(columns = {"Weight (g)":"Total weight as per X (KG)"} , inplace = True)
X_weight.head(10)


# In[11]:


X_comp = pd.merge(X_COD, X_weight , on= "SKU")
X_comp.head()


# In[12]:


X_comp.shape


# # Importing courier data and merging to X company data.

# In[13]:


courier = pd.read_excel("K:\Major project\cointab\Assignment details\\Courier-Invoice.xlsx")


# In[14]:


X_zone = pd.read_excel("K:\Major project\cointab\Assignment details\\X-Zones.xlsx")


# In[15]:


courier.info()


# In[16]:


df = courier.merge(X_zone , on = ["Warehouse Pincode","Customer Pincode"])
df.shape


# In[17]:


df.head()


# In[18]:


data = df.merge(X_comp , on = 'Order ID')
data.shape


# In[19]:


data.head()


# In[21]:


data = data.drop(columns=["Warehouse Pincode", "Customer Pincode", "SKU","Order Qty", "Item Price(Per Qty.)"])


# In[22]:


data.head()


# In[23]:


data.rename(columns= {"Charged Weight":"Total weight as per Courier Company (KG)"}, inplace = True)


# In[24]:


data.rename(columns= {"Billing Amount (Rs.)":"Charges Billed by Courier Company (Rs.)"}, inplace = True)


# In[25]:


data1 = data.drop_duplicates()


# In[26]:


data1.shape


# In[27]:


data1["Delivery Zone as per X"].unique()


# # Calculating Weight slab as per X, according to different zone.

# In[28]:


Xzone_b = data1[data1["Delivery Zone as per X"] == 'b']


# In[29]:


Xzone_b.shape


# In[30]:


Xzone_d = data1[data1["Delivery Zone as per X"] == 'd']


# In[31]:


Xzone_d.shape


# In[32]:


Xzone_e = data1[data1["Delivery Zone as per X"] == 'e']
Xzone_e.shape


# In[34]:


#Weight slab as per X for b zone.

def weight_slab(weight):
    i = round(weight % 1, 1)
    if i == 0.0:
        return weight
    elif i > 0.5:
        return int(weight)+1
    else:
        return int(weight)+0.5
    
Xzone_b["Weight slab as per X (KG)"] = Xzone_b["Total weight as per X (KG)"].apply(weight_slab)
Xzone_b.head()


# In[35]:


#Weight slab as per X for d zone.

def weight_slab(weight):
    i = round(weight % 1.25, 2)
    if i == 0.00:
        return weight
    elif weight<1.25:
        return 1.25 
    else: 
        return (weight//1.25)*1.25+1.25
    
Xzone_d["Weight slab as per X (KG)"] = Xzone_d["Total weight as per X (KG)"].apply(weight_slab)
Xzone_d.head()


# In[36]:


#Weight slab as per X for e zone.

def weight_slab(weight):
    i = round(weight % 1.5, 2)
    if i == 0.00:
        return weight
    elif weight<1.5:
        return 1.55 
    else: 
        return (weight//1.5)*1.5+1.5
    
Xzone_e["Weight slab as per X (KG)"] = Xzone_e["Total weight as per X (KG)"].apply(weight_slab)
Xzone_e.head()


# # Calculating Expected charge as per X, according to different zone.

# In[37]:


#Expected charge as per X for b zone.

fwd_fixed = 33
fwd_additional = 28.3
rto_fixed = 20.5
rto_additional = 28.3
weight_slab = Xzone_b["Weight slab as per X (KG)"]
additional_weight = (weight_slab - 0.5)/0.5
Xzone_b['Expected Charge as per X (Rs.)'] = 0
Xzone_b['Expected Charge as per X (Rs.)']= np.where(Xzone_b['Type of Shipment'] == 'Forward charges', (fwd_fixed + additional_weight * fwd_additional) ,Xzone_b['Expected Charge as per X (Rs.)'] )
Xzone_b['Expected Charge as per X (Rs.)']= np.where(Xzone_b['Type of Shipment'] == 'Forward and RTO charges', (fwd_fixed + rto_fixed + additional_weight * (fwd_additional + rto_additional)) ,Xzone_b['Expected Charge as per X (Rs.)'] )
Xzone_b.head()


# In[38]:


#Expected charge as per X for d zone.

fwd_fixed = 45.4
fwd_additional = 44.8
rto_fixed = 41.3
rto_additional = 44.8
weight_slab = Xzone_d["Weight slab as per X (KG)"]
additional_weight = (weight_slab - 1.25)/1.25
Xzone_d['Expected Charge as per X (Rs.)'] = 0
Xzone_d['Expected Charge as per X (Rs.)']= np.where(Xzone_d['Type of Shipment'] == 'Forward charges', (fwd_fixed + additional_weight * fwd_additional) ,Xzone_d['Expected Charge as per X (Rs.)'] )
Xzone_d['Expected Charge as per X (Rs.)']= np.where(Xzone_d['Type of Shipment'] == 'Forward and RTO charges', (fwd_fixed + rto_fixed + additional_weight * (fwd_additional + rto_additional)) ,Xzone_d['Expected Charge as per X (Rs.)'] )
Xzone_d


# In[39]:


#Expected charge as per X for e zone.

fwd_fixed = 56.6
fwd_additional = 55.5
rto_fixed = 50.7
rto_additional = 55.5
weight_slab = Xzone_e["Weight slab as per X (KG)"]
additional_weight = (weight_slab - 1.5)/1.5
Xzone_e['Expected Charge as per X (Rs.)'] = 0
Xzone_e['Expected Charge as per X (Rs.)']= np.where(Xzone_e['Type of Shipment'] == 'Forward charges', (fwd_fixed + additional_weight * fwd_additional) ,Xzone_e['Expected Charge as per X (Rs.)'] )
Xzone_e['Expected Charge as per X (Rs.)']= np.where(Xzone_e['Type of Shipment'] == 'Forward and RTO charges', (fwd_fixed + rto_fixed + additional_weight * (fwd_additional + rto_additional)) ,Xzone_e['Expected Charge as per X (Rs.)'] )
Xzone_e


# In[41]:


data_Xslab = pd.concat([Xzone_d , Xzone_b , Xzone_e])


# In[42]:


data_Xslab.shape


# In[43]:


data_Xslab.head()


# In[44]:


data_Xslab["Delivery Zone charged by Courier Company"].unique()


# # Calculating Weight slab as per courier company, according to different zone.

# In[45]:


cou_b = data_Xslab[data_Xslab["Delivery Zone charged by Courier Company"] == 'b']
cou_b.shape


# In[46]:


cou_d = data_Xslab[data_Xslab["Delivery Zone charged by Courier Company"] == 'd']
cou_d.shape


# In[47]:


cou_e = data_Xslab[data_Xslab["Delivery Zone charged by Courier Company"] == 'e']
cou_e.shape


# In[48]:


def weight_slab(weight):
    i = round(weight % 1, 1)
    if i == 0.0:
        return weight
    elif i > 0.5:
        return int(weight)+1
    else:
        return int(weight)+0.5
    
cou_b["Weight slab charged by Courier Company (KG)"] = cou_b["Total weight as per Courier Company (KG)"].apply(weight_slab)
cou_b.head()


# In[49]:


def weight_slab(weight):
    i = round(weight % 1.25, 2)
    if i == 0.00:
        return weight
    elif weight<1.25:
        return 1.25 
    else: 
        return (weight//1.25)*1.25+1.25
cou_d["Weight slab charged by Courier Company (KG)"] = cou_d["Total weight as per Courier Company (KG)"].apply(weight_slab)
cou_d.head()


# In[50]:


def weight_slab(weight):
    i = round(weight % 1.5, 2)
    if i == 0.00:
        return weight
    elif weight<1.5:
        return 1.5 
    else: 
        return (weight//1.5)*1.5+1.5
    
cou_e["Weight slab charged by Courier Company (KG)"] = cou_e["Total weight as per Courier Company (KG)"].apply(weight_slab)
cou_e.head()


# In[51]:


final = pd.concat([cou_b , cou_d , cou_e])


# In[52]:


final


# # Total Expected Charge as per X including COD charge.

# In[53]:


final["Expected Charge as per X (Rs.)"] = final["Expected Charge as per X (Rs.)"]+final["COD Charge (Rs.)"]


# In[54]:


final


# # Difference Between Expected Charges and Billed Charges.

# In[55]:


final["Difference Between Expected Charges and Billed Charges (Rs.)"] = final["Charges Billed by Courier Company (Rs.)"] - final["Expected Charge as per X (Rs.)"]
final


# In[56]:


final = final.drop(columns=["Type of Shipment" , "Payment Mode" , "Total Order Price (rs.)" , "COD Charge (Rs.)"])
final


# In[57]:


final.reset_index(drop=True, inplace=True)


# In[58]:


#Rearranging coloumn order

final = final.iloc[:, [0,1,6,7,2,9,5,3,8,4,10]]
final


# # Creating Summary Table.

# In[59]:


# Calculate the total orders in each category
total_correctly_charged = len(final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] == 0])
total_overcharged = len(final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] > 0])
total_undercharged = len(final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] < 0])

# Calculate the total amount in each category
amount_overcharged = abs(final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] > 0]['Difference Between Expected Charges and Billed Charges (Rs.)'].sum())
amount_undercharged = final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] < 0]['Difference Between Expected Charges and Billed Charges (Rs.)'].sum()
amount_correctly_charged = final[final['Difference Between Expected Charges and Billed Charges (Rs.)'] == 0]['Expected Charge as per X (Rs.)'].sum()

# Create a new DataFrame for the summary
summary_data = {'Description': ['Total Orders where X has been correctly charged',
                                'Total Orders where X has been overcharged',
                                'Total Orders where X has been undercharged'],
                'Count': [total_correctly_charged, total_overcharged, total_undercharged],
                'Amount (Rs.)': [amount_correctly_charged, amount_overcharged, amount_undercharged]}

df_summary = pd.DataFrame(summary_data)

print(df_summary)


# # Conclusion : Total amount where X is overcharged is Rs. 19692.9.

# #Exporting data to workbook

# In[60]:


with pd.ExcelWriter("K:\Major project\cointab\Assignment details\processed files\\Cointab_DA_assignment.xlsx") as writer:
    final.to_excel(writer, sheet_name='Output Data 1', index=False)
    df_summary.to_excel(writer, sheet_name='Output Data 2', index=False)


# In[ ]:




