import pandas as pd
import re
import numpy as np

Address=pd.read_csv('Address.csv')

'''
Function takes input as:
1. Pandas dataframe
2. Column on dataframe that contains text that is to be indexed
3. Document ID

Extracts text data and document ID from pandas dataframe. Applies cleaning before splitting
by Term
'''
def DFCreateInd (InDF,DocStr,DocID):
	#Create a new dataframe with just Doc ID and contents of document
	ClnDF= InDF[[DocStr,DocID]]
	#Set the Doc ID as the index of the dataframe
	ClnDF.reset_index(inplace=True) 
	ClnDF.set_index(DocID, inplace=True)
	#Apply cleaning / processing to dataframe
	ClnDF=ClnDF[DocStr].str.replace('([.()]|\s$|^\s|"|\[|\])+','').str.replace('([,]|[\s]|&amp;)+',' ').str.replace('([.()]|\s$|^\s)+','')
	#Split contents of document by delimiter. Replace original dataframe with multicolumn dataframe returned
	ClnDF=ClnDF.str.split(' ',expand=True)
	#Loop through columns to append into single series
	ColList=ClnDF.columns.values
	Index= pd.Series()
	for i in ColList:
		Index=Index.append(ClnDF[i])

	#Convert series into dataframe while dropping null values
	Index= pd.DataFrame(Index, columns=['Term']).dropna()
	#Add dummy column to allow both DocID and Term to become index
	Index['ct'] = 1
	#Add Term to the dataframe index
	Index.set_index(['Term'], append=True, inplace=True)
	#De-duplicate Term to Doc ID association and sum the number of words - multiple addresses associated with one doc considered part of one document
	Index=Index.groupby(level=[DocID,'Term']).sum()

	#Calculate components of Okapi BM25 - formula taken from wikipiedia
	#fqi - f(qi,D) - qi term frequency in the document D - This is already calculated and present on Index dataframe
	DF=Index.groupby(level=['Term']).count() #n(qi) - the number of documents containing query term i
	N=Index.groupby(level=[DocID]).first().count().iloc[0] #N - is the total number of documents in the collection
	IDF=((N-DF+0.5)/(DF+0.5)).apply(np.log)

	k=2
	b=0.75
	DL=Index.groupby(level=[DocID]).sum() #|D| - is the length of the document D in words
	AvgDL=DL.mean().iloc[0] #avgdl - is the average document length in the text collection from which documents are drawn

	Index.reset_index(inplace=True) 
	Index.set_index(['Term'],inplace=True)
	Index.rename(columns = {'ct':'fqi'} ,inplace=True)
	Index=pd.merge(Index,IDF,left_index=True,right_index=True)
	Index.rename(columns = {'ct':'idf'} ,inplace=True)
	Index=pd.merge(Index,DL, left_on=DocID, right_index=True, how='left')
	Index.rename(columns = {'ct':'DL'} ,inplace=True)

	Index['TF']=(Index['fqi']*(k+1))/(Index['fqi']+(k*(1-b+(b*Index['DL']/AvgDL))))
	Index['Score']=Index['TF']*Index['idf']
	Index.drop(['fqi','idf','DL','TF'], axis=1, inplace=True)
	Index.set_index([DocID], append=True, inplace=True)
	return (Index)

AddInd=DFCreateInd(Address,'AddressEng','BuildingID')

'''
Function takes input as:
1. Pandas dataframe
2. Search string
3. Number of values to return

'''
def DFSrchInd (Index,srchstr,topX):
	srch_ret=AddInd.iloc[AddInd.index.get_level_values('Term').isin(srchstr.split(' '))]
	srch_ret.reset_index(inplace=True)
	srch_ret.set_index(['BuildingID'],inplace=True)
	srch_ret2=srch_ret.groupby(level='BuildingID').sum().sort_values('Score', ascending=False).iloc[0:topX]
	return (srch_ret2)

SrchRt=DFSrchInd(AddInd,'HO MAN TIN',2)

#Convert returned pandas dataframe into list
Srchlist=SrchRt.index.tolist()
Address[Address['BuildingID'].isin(Srchlist)]
