import os
import re

print('Warning: this program should be used to process the outputs generated from latest version CoreNLP.\n')

print('We have these files from CoreNLP:'+'\n')
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
CoreNLP_outputs = []
for file in os.listdir(script_dir):
    if file.endswith(".out"):
        CoreNLP_outputs.append(file)
for file_name in CoreNLP_outputs:
    print(file_name)
print('')

def find_all_in_text(text, str):
    index_list = []
    for match in re.finditer(r'\b('+str+r')\b', text):
        index_list.append(match.start())
    return index_list

for file_name in CoreNLP_outputs:
    file = open(file_name)
    text_file = file_name.replace(".out","")
    c = 0
    for line in file:
        c = c + 1
        if 'Extracted quotes:' in line:
            break
    original_text = open(text_file, "r").read()

    n = 1
    e = 1
    extracted_quotes = []
    brat_format_lines = []
    with open(file_name) as fp:
        for i, line in enumerate(fp):
            if i >= c:
                extracted_quotes.append(line)

    regex = re.compile(r"(?<=\bcharOffsetBegin=)\w+")
    for quote in extracted_quotes:
        Quote = quote.split('\t')[1:]
        Quote = Quote[0]
        len_Quote = len(Quote)
        match = regex.search(quote)
        if match:
            start_position = match.group()
            end_position = int(start_position) + len_Quote

        speaker = quote.split(':')[0]
        if speaker != 'Unknown':
            speaker_indexes = list(find_all_in_text(original_text, speaker))
        else:
            speaker_indexes = []

        indexes = [] # Algorithm finding the nearest speaker index to the quote
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
                print(speaker_pos, speaker_pos + len(speaker), file=open("xmi outputs/"+file_name+".txt", "a"))
                print(start_position, end_position, file=open("xmi outputs/"+file_name+".txt", "a"))
                n = n + 1

        T = "T" + str(n) + '\t' + 'Quote' + ' ' + str(start_position) + ' ' + str(end_position) + '\t' + Quote
        n = n + 1

        brat_format_lines.append(T)

        # if indexes: # Print out the relation between speaker and quote
        #     E = "E" + str(e) + '\t' + 'Speaker:T'+ str(n-2) + ' ' + 'Speak:T' + str(n-1)
        #     e = e + 1
        #     brat_format_lines.append(E)

        file_name_ann = os.path.splitext(file_name)[0]
        file_name_ann = os.path.splitext(file_name_ann)[0] + '.ann' # Remove the original file extension and add ann extension

        f = open(file_name_ann, 'w')
        for line in brat_format_lines:
            f.write(line + "\n")

print("Brat annotation files were generated.")

# os.system('cmd /c "groovy pipeline"')
#
# print("xmi annotations were generated in the xmi outputs folder.")
