import os.path
import re

print('Warning: just run this program for once after running groovy pipeline!\n')

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
groovy_outputs = []
for file in os.listdir(script_dir):
    if file.endswith(".xmi"):
        groovy_outputs.append(file)

def listToString(s):
    str = ""
    for ele in s:
        str += ele
    return str

def remove_last_N_lines(file_name):
    f=open(file_name,"r")
    d=f.read()
    f.close()
    l=d.split("\n")
    s="\n".join(l[:-4])
    f=open(file_name,"w+")
    for i in range(len(s)):
        f.write(s[i])
    f.close()

for file_name in groovy_outputs:
    n = 100000000
    speaker_ids = []
    quote_ids = []
    xmi_lines = []
    with open(file_name) as f_xmi:
        for line in f_xmi:
            xmi_lines.append(line)
        head = xmi_lines[:2]
        cas_sofa = xmi_lines[-3]
        cas_view = xmi_lines[-2]
        tail = xmi_lines[-1]
        xmi_lines = xmi_lines[3:-3]

    speaker_quote_relation = os.path.splitext(file_name)[0]
    speaker_quote_relation = os.path.splitext(speaker_quote_relation)[0] + ".txt.out.txt"
    if os.path.isfile(speaker_quote_relation):
        f = open(speaker_quote_relation, "r")
        while True:
            Speaker = f.readline()
            Quote = f.readline()
            if not Quote: break
            res = [i for i in Speaker.split() if i.isdigit()]
            speaker_start, speaker_end = res[0], res[1]
            res = [i for i in Quote.split() if i.isdigit()]
            quote_start, quote_end = res[0], res[1]
            matches = [speaker_start, speaker_end]
            for line in xmi_lines:
                if all(i in line for i in matches):
                    match = re.search('xmi:id="(\d+)', line)
                    if match:
                        id = match.group(1)
                        if id not in speaker_ids:
                           speaker_ids.append(id)

            matches = [quote_start, quote_end]
            for line in xmi_lines:
                if all(i in line for i in matches):
                    match = re.search('xmi:id="(\d+)', line)
                    if match:
                        id = match.group(1)
                        if id not in quote_ids:
                           quote_ids.append(id)

    remove_last_N_lines(file_name)

    cas_view = cas_view[:-4]
    for x, y in zip(speaker_ids, quote_ids):
        matched_line = [line for line in xmi_lines if ('xmi:id="'+str(y)+'"') in line]
        matched_line = listToString(matched_line)
        match = re.search('begin="(\d+)', matched_line)
        if match:
            begin = match.group(1)
        match = re.search('end="(\d+)', matched_line)
        if match:
            end = match.group(1)
        print('    <custom:Relation xmi:id="' + str(n) + '" sofa="2" begin="' + str(begin) + '" end="' + str(
            end) + '" Dependent="' + str(y)+ '" Governor="' + str(x) + '" value="Speak"/>', file=open(file_name, "a"))
        cas_view = cas_view + ' ' + str(n)
        n = n + 1
    cas_view = cas_view + '"/>'
    print(cas_sofa, file=open(file_name, "a"))
    print(cas_view, file=open(file_name, "a"))
    print(tail, file=open(file_name, "a"))

print("")
print("Relation annotations were created.")

