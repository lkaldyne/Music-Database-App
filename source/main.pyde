class Artist:
    def __init__(self,Name,Title,Label,Format,Rating,Released,Release_id):
        self.Name = Name
        self.Title = Title
        self.Label = Label
        self.Format = Format
        self.Rating = int(Rating)
        self.Released = int(Released)
        self.Release_id = int(Release_id)
    def showinfo(self,x,y,howbig):
        textSize(howbig)
        text("%s   %s   %s   %s   %s   %s   %s" %(self.Name,self.Title,self.Label,self.Format,str(self.Rating),str(self.Released),str(self.Release_id)),x,y)
class Database:
    #Stores and Manages all artists and their information
    def __init__(self):
        self.tempsearched = []
        self.startingPT = 200
        self.artists = []
    def add_artist(self,tempinfo):
        self.artists.append(Artist(tempinfo[0], tempinfo[1], tempinfo[2], tempinfo[3], tempinfo[4], tempinfo[5], tempinfo[6]))
    def showData(self,kind):
        if kind == 1:
            for i in range(len(self.artists)):
                self.artists[i].showinfo(50,self.startingPT+(30*i),15)
        elif kind == 2:
            for i in range(len(self.tempsearched)):
                self.tempsearched[i].showinfo(50,self.startingPT+(30*i),15)
    def sort_by_name(self):
        thing = mergesort(self.artists[:], 0)
        return thing
    def sort_by_year(self):
        thing = mergesort(self.artists[:], 1)
        return thing
    def search_by_name(self,name):
        presorted = self.sort_by_name()
        matches = []
        while True:
            temp = binarysearch(presorted,name,0)
            if temp != False:
                matches.append(temp)
                presorted.remove(temp)
            else:
                break
        self.tempsearched = matches
    def search_by_year(self,year):
        presorted = self.sort_by_year()
        matches = []
        while True:
            temp = binarysearch(presorted,year,1)
            if temp != False:
                matches.append(temp)
                presorted.remove(temp)
            else:
                break
        self.tempsearched = matches
def binarysearch(array,item,kind):
    if kind == 0:
        if array[len(array)/2].Name == item:
            return array[len(array)/2]
        elif len(array) > 1:
            if array[len(array)/2].Name > item:
                return binarysearch(array[0:len(array)/2],item,0)
            else:
                return binarysearch(array[(len(array)/2):],item,0)
        else:
            return False
    elif kind == 1:
        if array[len(array)/2].Released == item:
            return array[len(array) / 2]
        elif len(array) > 1:
            if array[len(array)/2].Released > item:
                return binarysearch(array[0:len(array)/2],item,1)
            else:
                return binarysearch(array[(len(array)/2):],item,1)
        else:
            return False
def flip(thing):
        temp = thing[0]
        thing[0] = thing[1]
        thing[1] = temp
        return thing
def reorganize(list1,list2,type):
    finallist = []
    i = 0
    j = 0
    constnum = Artist("zzzzzzzzzzzzzzz","zzzzzzzzzzzzzz","zzzzzzzzzzzzzzz","zzzzzzzzzzzzzzz",999999999999,999999999,9999999999)
    list1.append(constnum)
    list2.append(constnum)
    while True:
        if type == 0:
            if list1[i].Name == constnum.Name and list2[j].Name == constnum.Name:
                break
            if list1[i].Name < list2[j].Name:
                finallist.append(list1[i])
                i+=1
            else:
                finallist.append(list2[j])
                j+=1
        elif type == 1:
            if list1[i].Released == constnum.Released and list2[j].Released == constnum.Released:
                break
            if list1[i].Released < list2[j].Released:
                finallist.append(list1[i])
                i+=1
            else:
                finallist.append(list2[j])
                j+=1
    return finallist
def mergesort(numlist,type):
    if len(numlist) > 2:
        lefthalf = numlist[:(len(numlist) / 2)]
        righthalf = numlist[(len(numlist) / 2):]

        lefthalf = mergesort(lefthalf,type)
        righthalf = mergesort(righthalf,type)

        numlist = reorganize(lefthalf,righthalf,type)

    else:
        try:
            if type == 0:
                if numlist[0].Name > numlist[1].Name:
                    numlist = flip(numlist)
            elif type == 1:
                if numlist[0].Released > numlist[1].Released:
                    numlist = flip(numlist)
        except:
            pass
    return numlist

def setup():
    size(1100,700)
    global collection,searchtxt,phase,shiftpressed
    infofile = open("data.tsv","r")
    collection = Database()
    for line in infofile:
        tempinfo = line.strip().split("\t")
        collection.add_artist(tempinfo)
    searchtxt = "Search: "
    phase = 1
    shiftpressed = False
    infofile.close()
def draw():
    global collection,searchtxt,phase
    background(0)
    fill(255)
    if phase == 1:
        collection.showData(1)
    elif phase == 2:
        collection.showData(2)
    fill(0)
    noStroke()
    rect(0,0,1100,150)
    stroke(255)
    rect(900,10,100,50)
    rect(900,75,100,50)
    fill(255)
    text("A - Z",925,35)
    text("YEAR",925,105)
    line(135,65,800,65)
    textSize(25)
    text(searchtxt,50,50)

def keyPressed():
    global searchtxt,collection,phase,shiftpressed
    if key == BACKSPACE:
        if len(searchtxt) > 8:
            searchtxt = searchtxt[:len(searchtxt)-1]
    elif key == ENTER:
        if phase == 1:
            try:
                temp = int(searchtxt[8:])
                collection.search_by_year(temp)
            except:
                temp = searchtxt[8:]
                collection.search_by_name(temp)                
            phase = 2
        elif phase == 2:
            collection.tempsearched = ""
            phase = 1
    elif keyCode == 16:
        shiftpressed = True
    else:
        if shiftpressed == True:
            if key == "9":
                searchtxt = searchtxt + "("
            elif key == "0":
                searchtxt = searchtxt + ")"
            else:
                searchtxt = searchtxt + key.upper()                                
            shiftpressed = False
        else:
            searchtxt = searchtxt + key
        
def mouseReleased():
    global collection
    if (mouseX >= 900 and mouseX <= 1000) and (mouseY >= 10 and mouseY < 60):
        temp = collection.sort_by_name()
        collection.artists = temp
    if (mouseX >= 900 and mouseX <= 1000) and (mouseY >= 75 and mouseY < 125):
        temp = collection.sort_by_year()
        collection.artists = temp
        
        
def mouseWheel(event):
    global collection
    if event.count == 1:
        collection.startingPT -= 25
    if event.count == -1:
        if collection.startingPT < 200:
            collection.startingPT += 25
        
    