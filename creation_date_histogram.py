import csv
import codecs
#=======================================================================#
#     Get frequency counts of Twitter account creation dates            #
#                Lawrence Alexander @LawrenceA_UK                       #
#=======================================================================#

datestamps=[]

# CSV input filename

csv_file= ""

# Read from input CSV file

with open(csv_file) as csv_input:
    reader=csv.DictReader(csv_input)
    for row in reader:
        datestamps.append(row['Creation Date'])

# Count frequency of creation dates

count = 0
creation_date_percentages = {}
creation_date_counts = {}
for the_datestamp in datestamps:
    for countdates in datestamps:
        if countdates == the_datestamp:
            count += 1 
    if count >= 1:                
        creation_date_percentages[the_datestamp] = 100.0 * count / len (datestamps) 
        creation_date_counts[the_datestamp]= count
    count =0
    
# Write out datestamp and percentage-count data as CSV 

outputfile = ""
outfile = codecs.open(outputfile, 'wb', 'utf-8')
outfile.write('Creation Date' + ',' + 'Percentage Count' + u"\n")   
for c_date, percentage in creation_date_percentages.iteritems():
    percentage=round(percentage,3)
    if percentage >= 0.40:
        outfile.write(str(c_date) + ',' + str(percentage) + u"\n")
outfile.close()    

print "[*] Successfully wrote data to %s" % outputfile 

# Same for raw counts
outputfile = ""
outfile = codecs.open(outputfile, 'wb', 'utf-8')
outfile.write('Creation Date' + ',' + 'Count' + u"\n")   
for c_date, count in creation_date_counts.iteritems():
    if count >= 4:
        outfile.write(str(c_date) + ',' + str(count) + u"\n")
outfile.close() 
print "[*] Successfully wrote data to %s" % outputfile        
