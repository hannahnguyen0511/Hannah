import csv # imports the needed csv functions
'''
Author:      Vu Thuy Hanh Nguyen
Student ID:  1064289
Date:        31 May 2019
Course:      COMP90059 Introduction to Programming
Program:     Cleaning & analysing criminals' data
Description: This program repaired the corrupted values which
             has been hacked by criminals. Further more, this
             program also provides some basis tools in order to
             analysing current criminals situation such as the
             total number of crime from 2002 to 2012, defining the
             worst and best area of crime, and the type of crimes with
             the corresponded values as well.
'''
######################################
## COMP90059 - Assignment 2         ##
## This file and functions are      ##
## designed to support the needs    ##
## of assignemt 2.                  ##
##                                  ##
## read_data                        ##
## reads the data from the CSV file ##
######################################
def read_data(filename):
    data = {}
    new_data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ID = row["ID"]
            del row["ID"]
            for key in row:
                if not row[key]:
                    row[key] = None
            data[ID]=row
            new_data[ID] = dict(list(row.items()))
    return new_data


#####################################################################
## Main method                                                     ##
## Store and display:                                              ##
##  + The total number after repairing vandalished values          ##
##  + The worst year of crime & corresponded values                ##
##  + The number of subdivision along with teh worst and best area ##
##  + The information about the most active crime overall          ##
##  + The conclusion after analysing data                          ##
#####################################################################
filename = 'crimedata_large_dirty_mac.csv'
data = read_data(filename)

def main():
    repair_count = clean(data)[1]
    print("The total number of repaired values:", repair_count)
    total_rows = max(list(map(int, clean(data)[0].keys())))
    mostActiveCrime(data)
    report(datafile)
    def crime_worst_year():
        worst_year = {}
        for i in range(2002, 2012 + 1):
            worst_year[countCrimes(data, str(i))] = str(i)
        return worst_year[max(worst_year.keys())], max(worst_year.keys())
    print("The worst year of crime: {0:}, with the total of crimes is {1:}"\
          .format(crime_worst_year()[0], crime_worst_year()[1]))
    number_of_Subdivision = report(datafile)[3] #define subdivision and the worst and best area with the values
    worst_area = report(datafile)[7][0]
    worst_area_value = report(datafile)[7][1]
    best_area = report(datafile)[9][0]
    best_area_value = report(datafile)[9][1]
    print("The total number of Subdivision: {0:d}, with the worst area: {1:s} computed to {2:}\
, and the best area {3:s} computed to {4:}".format(number_of_Subdivision, worst_area\
                                                    , worst_area_value, best_area, best_area_value))
    total_type_of_crime = report(datafile)[5] #define the type of crimes and the most active crimes
    most_active_crime_overall = report(datafile)[11]
    most_active_crime_overall_value = max(mostActiveCrime(data).values())
    print("Most active crime overall: {0:s}, computed to {1:d}"\
          .format(most_active_crime_overall, most_active_crime_overall_value))
    return 'On behalf of the MUC (Made Up Company), I have analysed {0:d} units of the \
crime statistics data, over a 10-year period. I have repaired {1:d} corrupt data values. \
This data-set covered {2:d} Subdivisions and found {3:d} types of crimes. I conclude that \
the worst area for crime is {4:}, the safest area is {5:} and that the most active category\
 of crime is {6:s}. Sincerely, <Vu Thuy Hanh Nguyen:1064289>.'\
.format(total_rows, repair_count, number_of_Subdivision, total_type_of_crime, worst_area, \
        best_area, most_active_crime_overall)

#####################################################################
## Task 1                                                          ##
## Clean up the corrupted data.                                    ##
## Return the new data has been cleaned and the repaired values.   ##
#####################################################################

def clean(data):
    new_data_set = data.copy()
    summated_value = 0
    for x in new_data_set: #loop through data file in order to find the changed the corrupted subdivision data and repair and count
        if 'muc' in str(new_data_set[x]['Subcategory']).lower():
            new_data_set[x]['Subcategory'] = "Trepass"
            summated_value += 1
        for i in range(2002, 2012 + 1): # find and repair count the corrupted data
            if str(new_data_set[x][str(i)].lower()) == 'zero' or \
               str(new_data_set[x][str(i)].lower()) == '' or str(new_data_set[x][str(i)].lower()) == 'null':
                new_data_set[x][str(i)] = str(0)
                summated_value += 1
            elif int(new_data_set[x][str(i)]) < 0:
                new_data_set[x][str(i)] = str(abs(int(new_data_set[x][str(i)])))
                summated_value += 1
    return new_data_set, summated_value


#####################################################################
## Task 2                                                          ##
## Using the cleaned data to count the total                       ##
## number of crimes from 2002 to 2012.                             ##
#####################################################################

def countCrimes(data, key):
    data = clean(data)[0]
    year_statistics_data = {}
    for x in data: #count crime for each year
        for i in range(2002, 2012 + 1):
            if str(i) not in year_statistics_data:
                year_statistics_data[str(i)] = 0
            year_statistics_data[str(i)] += int(data[x][str(i)])
    return year_statistics_data[key]


#####################################################################
## Task 3                                                          ##
## Using the cleaned data to represent subdivision with the        ##
## summated total of all crimes within that area over all years.   ##
#####################################################################

def worstCrime(data):
    data = clean(data)[0]
    division_dict = {}
    for x in data: # count accumulated crime by using seperated subdivision
        for i in range(2002, 2012 + 1):
            if data[x]['Statistical Division or Subdivision'] not in division_dict:
                division_dict[data[x]['Statistical Division or Subdivision']] = 0
            division_dict[data[x]['Statistical Division or Subdivision']] += int(data[x][str(i)])
    return division_dict


#####################################################################
## Task 4                                                          ##
## Using the cleaned data to represent the type of crimes with     ##
## the number of how often those crimes were committed overall     ##
#####################################################################

def mostActiveCrime(data):
    data = clean(data)[0]
    crime_type_dict = {}
    for x in data: #create dictionary for type of crime
        if data[x]['Offence category'] not in crime_type_dict:
            crime_type_dict[data[x]['Offence category']] = 0
        for i in range(2002, 2012 + 1):
            crime_type_dict[data[x]['Offence category']] += int(data[x][str(i)])
    return crime_type_dict

#####################################################################
## Task 5                                                          ##
## Using the cleaned data to report on the final status and        ##
## crime situation                                                 ##
#####################################################################


datafile = filename
def report(datafile):
    datafile = clean(data)[0]
    def worst_area(): # find the max and min for worst and best area
        worst_crime_order = {}
        for key,value in worstCrime(datafile).items():
            worst_crime_order[value] = key
        return worst_crime_order[max(worst_crime_order.keys())], str(max(worst_crime_order.keys())), \
               worst_crime_order[min(worst_crime_order.keys())], str(min(worst_crime_order.keys()))
    def crime_type(): #find max type of crime with the value
        crime_type_order = {}
        for key,value in mostActiveCrime(datafile).items():
            crime_type_order[value] = key
        return crime_type_order[max(crime_type_order.keys())]
    return ['Total number of rows', max(list(map(int, datafile.keys()))), 'Total number of examined Subdivisions',
            len(worstCrime(datafile).keys()), 'Total number of Offence Categories',
            len(mostActiveCrime(datafile).keys()), 'Worst Area:', worst_area()[0:2],
            'Best Area:', worst_area()[2:4], 'Most active type of crime', crime_type()]

main()
############################
## Begins the application ##
############################


