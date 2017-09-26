
dict={"a":6,"b":5,"c":4,"d":3}
for key,value in dict.items():
    print key,value
print sorted(dict.items())
print("---")
print sorted(dict.keys())
print("----")
for x in sorted(dict.keys(),reverse=True):
     dict[x]
#print sorted(dict.items(),key)
