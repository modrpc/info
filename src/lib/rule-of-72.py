#!/usr/bin/python

# present value
pv = 10000

# annual interst rate (as proportion)
interest = 0.152

print("* Present value:     %.1f" % pv)
print("* Compound interest: %.1f %%" % (interest*100))

compound = pv
for i in range(1, 30):
	compound = compound * (1 + interest)
	print("* Year %2d:  %.1f" % (i, compound))
