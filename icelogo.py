# Code by Martijn Kleiweg
# Phenotyping Core, University of Arizona

# Function to find the complete sequence in the Uniprot data

def findstring(substr, character, mouse):

    # Set cleaned Uniprot data to variable

    file = 'uniprotdata.txt'

    # Initialize variables

    strings = []
    n = 49
    indexlist = []
    startstring = ""
    findmouse = False
    dict = {}
    mouse1 = ""
    key = ""
    value = ""
    none = ""

    if character == 0:
        return none

    with open(file) as input:
        lines = list(input)  # Slurps all lines from file

    keylist = []
    valuelist = []

    # Append all the different Accession types to the keylist

    for i in lines:
        if i[0] == ">":
            keylist.append(i)

    # Append all the sequences to the valuelist

    for i, lines in enumerate(lines):
        start = lines[0]
        if start[0] != ">":
            startstring = startstring + lines
        else:
            str3 = startstring.replace("\n", "")
            valuelist.append(str3)
            startstring = ""

    # Create a dictionary of the keylist and the valuelist

    a = 1
    while a < len(valuelist):
        dict.update({keylist[a-1] : valuelist[a]})
        a = a +1


    resultstring = []

    # Get the correct sequence for the current Accession (mouse) and add to the resultstring

    for key in dict:
        if mouse in key:
            finalstring = dict.get(key)

    resultstring.append(finalstring)


    # Find the right part of the found sequence

    findmouse = False

    # print(resultstring)

    str2 = ""
    str3 = ""

    # If data is not available

    if len(resultstring) == 0:
        return("Could not find phosphosite")

    # If phosphosite is not unique

    if len(resultstring) > 2:
        return("Phosphosite is not unique")

    # Clean both lines and to variables

    if len(resultstring) == 2:
        str2 = resultstring[0].replace("\n", "")
        str3 = resultstring[1].replace("\n", "")

    # Clean line and add to variable

    if len(resultstring) == 1:
        str2 = resultstring[0].replace("\n", "")

    # Add X-es if sequence is not long enough

    str2 = 50 * "X" + str2 + 50 * "X"

    result = 0

    #Determine lenghts of left and right arm

    left = n-character+1
    right = n-len(substr)+character

    result = str2.find(substr)
    leftarm = result-left

    resultstring1 = str2[leftarm:]

    rightarm = len(str2)-(result+len(substr)+right)

    # Create sequence of the correct length

    finalstring = resultstring1[:-rightarm]

    # If sequence is on two lines instead of one:

    if len(resultstring) == 2:
        str3 = 50 * "X" + str3 + 50 * "X"

        #Determine lenghts of left and right arm

        left = n-character+1
        right = n-len(substr)+character

        result2 = str3.find(substr)
        leftarm2 = result2-left

        resultstring2 = str3[leftarm2:]

        rightarm2 = len(str3)-(result2+len(substr)+right)

        finalstring2 = resultstring2[:-rightarm2]

        finalstring = finalstring + " OR " + finalstring2


    return(finalstring)





def readcsv():

    import csv

    # Read cleaned file that includes the column with all the subsequences

    with open('icelogo6.csv', newline='') as f:
        reader = csv.reader(f)
        string_list = list(reader)

        # Add all the subsequences to a list

        flat_strlist = []
        for sublist in string_list:
            for item in sublist:
                flat_strlist.append(item)

    # Read cleaned file that includes all the character positions


    with open('fifth.csv', newline='') as g:
        reader = csv.reader(g)
        character_list = list(reader)

        # Add all the character positions to a list

        flat_charlist = []
        for sublist in character_list:
            for item in sublist:
                flat_charlist.append(item)


        flat_charlist = [int(i) for i in flat_charlist]


    # Read cleaned file that includes all the Accessions

    with open('icelogo4.csv', newline='') as h:
        reader = csv.reader(h)
        mouse_list = list(reader)

        flat_mouselist = []
        for sublist in mouse_list:
            for item in sublist:
                flat_mouselist.append(item)

    #Initialize variables

    finalstring_list = []
    i = 0

    # Iterate over the three lists and find the long sequences

    while i < len(flat_charlist):

        str01 = (flat_strlist[i])
        int01 = (flat_charlist[i])
        str02 = (flat_mouselist[i])

        h = findstring(str01, int01, str02)
        finalstring_list.append(h)
        i = i+1

    # Write final result to CSV-file

    with open('result.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(finalstring_list)



# Start function
readcsv()
