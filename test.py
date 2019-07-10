
word = "(32.2217 -110.9258); (32.2217 -110.9258)"
list = word.split("; ")
print(list)
for s in list:
    oc = s[s.find("(")+1:s.find(")")]
    coord = oc.split(" ")
print(coord)