import sys

# takes output from Ondel with and split it into separate text files
# format : 
# 0107_400123_0000 au12 au33 au33 au56 au56
# 0107_400123_0002 au18 au33 au55 au55 au58
# ...

print("init raw text file:",sys.argv[1]," dest folder:",sys.argv[2])
print("text_corpora file:",sys.argv[3])

txt_file=sys.argv[1]
dest_dir=sys.argv[2]
text_corpora_filename=sys.argv[3]
with open(txt_file, 'r') as myfile:
    data=myfile.read()
data_array=data.split('\n')

previous_sentence_id=''
current_sentence=''
text_corpora=''
new_data_array=''
for w in range(len(data_array)):
	w_split= data_array[w].split(' ')
        sentence_id =w_split[0]
	filename = sentence_id+'.txt'
	w_split=w_split[1:] # getting rid of sentence_id
	previous_state=''
	reduced_sentence=[]
	for i in range(len(w_split)):
		current_state=w_split[i].split('u')[1]
		if len(current_state)==1:
			current_state+='x'	
		if previous_state==current_state:
			continue
		reduced_sentence.append(current_state)
		previous_state=current_state
	sentence=''.join(reduced_sentence)
	text_corpora+=sentence+' '
	with open(dest_dir+'/'+filename, 'w') as myfile:
   		myfile.write(sentence+'\n')	

text_corpora+='\n'
with open(text_corpora_filename,'w') as myfile:
        myfile.write(text_corpora)
                                                            
