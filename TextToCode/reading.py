textfile = "area.txt"
textfile1 = "Wild Area Changes.txt"
places= []
areaNames = ["Route", "City", "Town", "Ranch", "Tower", "Shrine", "Bay", "Mountain", "Road", "Castle"]
with open(textfile) as file:  
    data = file.readlines()
    #print(data)
    for readLine in data:
        #check for --- lines
        if "- -" in readLine:
            data.remove(readLine)
        #get route name or area name
        for name in areaNames:
            if name in readLine:
                #documentation fucked, sometimes names city or area after surf spots
                if "Fish" in readLine or "Surf" in readLine or "Special Event" in readLine:
                    #print(f"found them in: {readLine}")
                    pass
                else:
                    routeName = readLine.replace("~", "").replace("\n", "") 
                    #TODO remove season from routeName
                    #save to parameter of area class
                    #if "-" in routeName:
                    #   routeName.splits("-")
                    if routeName in places:
                        print("is er al")
                        pass
                    else:
                        #convert to Area object
                        places.append(routeName)

                    
    
        if "Hidden Grotto Guide" in readLine:
            #no more encounter data after this
            #need logic for hidden grotto data
            break
    
    print(f'places: {places}')        
