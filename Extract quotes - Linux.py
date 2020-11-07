import os
import re
import shutil

print('Warning: this program should be used to process the outputs generated from Linux version.\n')

print('We have these files from CoreNLP:'+'\n')
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
CoreNLP_outputs = []
for file in os.listdir(script_dir):
    if file.endswith(".out"):
        CoreNLP_outputs.append(file)
for file_name in CoreNLP_outputs:
    print(file_name)
print('')

def listToString(s):
    str = ""
    for ele in s:
        str += ele
    return str

def find_all_in_text(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

for file_name in CoreNLP_outputs:
    file = open(file_name)
    text_file = file_name.replace(".out","")
    c = 0
    for line in file:
        c = c + 1
        if 'Extracted quotes:' in line:
            break
    text = open(text_file, "r")
    text = text.read()

    n = 1
    quotes = []
    brat_format_lines = []
    with open(file_name) as fp:
        for i, line in enumerate(fp):
            if i >= c:
                quotes.append(line)
    regex = re.compile(r"(?<=\bCharacterOffsetBegin=)\w+")
    spl_word = 'Speaker='
    for quote in quotes:
        Quote = re.findall('"([^"]*)"', quote)
        Quote = listToString(Quote)
        Quote = '"' + Quote + '"'
        len_Quote = len(Quote)
        match = regex.search(quote)
        if match:
            start_position = match.group()
            end_position = int(start_position) + len_Quote
        speaker = quote.partition(spl_word)[2].replace(']\n','').replace(' ','  ')
        speaker_indexes = list(find_all_in_text(text, speaker))

        indexes = [] # Finding the nearest speaker index to the quote
        for i in speaker_indexes:
            indexes.append(int(start_position)-i)
            indexes.append(i-int(end_position))
        if indexes:
            if any(ele > 0 for ele in indexes):
                nearest_pos = min([x for x in indexes if x > 0])
                minpos = indexes.index(nearest_pos)
                if (minpos % 2) == 0:
                    speaker_pos = int(start_position) - nearest_pos
                else:
                    speaker_pos = int(end_position) + nearest_pos
                T= "T" + str(n) + '\t' + 'Speaker' + ' ' + str(speaker_pos) + ' ' + str(speaker_pos+len(speaker)) + '\t' + speaker
                brat_format_lines.append(T)
                n = n + 1

        T = "T" + str(n) + '\t' + 'Quote' + ' ' + str(start_position) + ' ' + str(end_position) + '\t' + Quote
        n = n + 1
        brat_format_lines.append(T)

        file_name = os.path.splitext(file_name)[0]
        file_name = os.path.splitext(file_name)[0] + '.ann' # Remove the original file extension

        f = open(file_name, 'w')
        for line in brat_format_lines:
            f.write(line + "\n")

print("Brat annotation files were generated.")

# os.system('cmd /c "groovy pipeline"')
#
# print("xmi annotations were generated in the xmi outputs folder.")
