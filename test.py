import formulas
'''
word = "(32.2217 -110.9258); (32.2217 -110.9258)"
list = word.split("; ")
print(list)
for s in list:
    oc = s[s.find("(")+1:s.find(")")]
    coord = oc.split(" ")
print(coord)
'''

print(formulas.haversine(37.9375, -107.8117, 40.7975, -81.165))