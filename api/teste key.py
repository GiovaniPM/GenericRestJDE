# Python3 code to demonstrate working of 
# Check for Key in Dictionary Value list 
# Using any() 

def findWord(dictseq, txt):
    for word in dictseq:
        if word == txt:
            return True
    return False

def findValue(dictseq,txt):
    for word in dictseq:
        if dictseq[word] == txt:
            return True
    return False
	
# initializing dictionary 
test_dict = {'Gfg' : [{'CS' : 5}, {'GATE' : 6}], 'for' : 2, 'CS' : 3} 
	
# printing original dictionary 
print("The original dictionary is : " + str(test_dict)) 
	
# initializing key 
key = "GATE"
	
# Check for Key in Dictionary Value list 
# Using any() 
res = any(key in ele for ele in test_dict['Gfg']) 
	
# printing result 
print("Is key present in nested dictionary list ? : " + str(res)) 

test_dict = {'operator': '=', 'term1': 'TAB.IMITM', 'term2': 123}

print(str(findWord(test_dict, 'term1')))
print(str(findWord(test_dict, 'term2')))
print(str(findWord(test_dict, 'Term2')))
print(str(findWord(test_dict, '=')))
print(str(findWord(test_dict, 'operator')))
print(str(findValue(test_dict, '=')))
print(str(findValue(test_dict, '123')))
print(str(findValue(test_dict, 123)))
print(str(findValue(test_dict, None)))