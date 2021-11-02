file = open("dorian.txt", 'r')
locc = {}
for line in file:
    line = line.strip().lower()
    for l in line:
        if not (l in locc):
            locc[l] = 1
        else:
            locc[l] += 1

rlocc = {}
for l, n in locc.items():
    rlocc[n] = [l]
else:
    rlocc[n].append(l)

for n, l in reversed(sorted(rlocc.items())):
    print(l, n)
wocc, wlen = {}, {}
file.close()
file2 = open("dorian.txt", 'r')
for line in file2:
    words = line.strip().lower().split()
    for w in words:
        w = w.strip(".,;:-'\"?!()")
        if not (w in wocc):
            wocc[w] = 1
            wlen[w] = len(w)
        else:
            wocc[w] += 1          
file2.close()
rwocc, rwlen = {}, {}
for key, value in wocc.items():
    if value not in rwocc:
        rwocc[value] = [key]
    else:
        rwocc[value].append(key)
most_common = max(rwocc.values())
print(most_common)
for key, value in wlen.items():
    if value not in rwlen:
        rwlen[value] = [key]
    else:
        rwlen[value].append(key)
print(rwlen.items())