import urllib.request
import zipfile
import pandas

filename = "data.zip"

#downloads all FRS data from the epa
infile, headers = urllib.request.urlretrieve("https://ordsext.epa.gov/FLA/www3/state_files/national_combined.zip",filename)

#creates unzip instance
unzip = zipfile.ZipFile(filename, "r")

#this pulls both needed files from the FRS zip for later use
outfile = unzip.extract("NATIONAL_FACILITY_FILE.CSV")
outfile2 = unzip.extract("NATIONAL_ENVIRONMENTAL_INTEREST_FILE.CSV")


program_acronyms = ["CA_ENVIROVIEW",
"KY-TEMPO",
"LUST-ARRA",
"MN-TEMPO",
"NM-TEMPO",
"NPDES",
"SFDW",
"CWNS",
"TRIS",
"TSCA"
]

#turns national environmental interest file
interest_df = pandas.read_csv('NATIONAL_ENVIRONMENTAL_INTEREST_FILE.CSV')
#print(interest_df.size)

#picks out facilities with relevant interests
ids = interest_df[interest_df["PGM_SYS_ACRNM"].isin(program_acronyms)]
#removes duplicate facility ids
ids = ids.drop_duplicates("REGISTRY_ID")
#print(ids.size)
#print(ids["REGISTRY_ID"].head())

#onto facility csv
facility_df = pandas.read_csv("NATIONAL_FACILITY_FILE.CSV")

#merges the ids we've picked out with the full facility information
merged_df = ids[["REGISTRY_ID","PGM_SYS_ACRNM"]].merge(facility_df,left_on="REGISTRY_ID", right_on="REGISTRY_ID")

merged_df = merged_df[['REGISTRY_ID',"PGM_SYS_ACRNM","LATITUDE83","LONGITUDE83","LOCATION_ADDRESS","COUNTY_NAME","STATE_NAME"]]

merged_df.to_csv('merged.csv',index=False)
