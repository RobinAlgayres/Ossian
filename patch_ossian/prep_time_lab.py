import sys

# Split a file containing all phone level alignments, eg :english_alignment_phones.txt
#0019_400020_0477 5.8975 5.9575  t
#0019_400020_0477 5.9575 6.0375  eh
# ....
#0089_400026_0400 6.0375 6.1175 l
#0089_400026_0400 6.1175 6.2175 th
#0089_400026_0400 6.2175 6.575 iy

# into the time_lab format for Ossian:
# one file for each sentence, eg : 0107_400123_0000.time_lab
#0 3875000 sil _POSS_PAUSE_
# 3875000 4575000 s2 b_DIGITONE_ b_DIGITONE_
# 700000 2800000 s3
# 2800000 2850000 s4
# 2850000 2900000 s5
# 2900000 2950000 s6
# 4575000 5975000 s2 ay ay
# 700000 2800000 s3
# 2800000 2850000 s4
# 2850000 2900000 s5
# 2900000 2950000 s6

def digit_to_str(digit):
	if digit=='0':
		digit='_DIGITZERO_'
	if digit=='1':
		digit='_DIGITONE_'
	if digit=='2':
		digit='_DIGITTWO_'
	if digit=='3':
		digit='_DIGITTHREE_'
	if digit=='4':
		digit='_DIGITFOUR_'
	if digit=='5':
		digit='_DIGITFIVE_'
	if digit=='6':
		digit='_DIGITSIX_'
	if digit=='7':
		digit='_DIGITSEVEN_'
	if digit=='8':
		digit='_DIGITEIGHT_'
	if digit=='9':
		digit='_DIGITNINE_'
	return digit

def safetext(unit):
	assert len(list(unit))==2, 'units must be composed of two characters, non trivial extension can be made to support longer units'
	digit1=digit_to_str(list(unit)[0])
	digit2=digit_to_str(list(unit)[1])
	return digit1+digit2

def create_state_line(start,end,unit):
# creating this format :
# 0 700000 s2 sil _PROB_PAUSE_
# 700000 2800000 s3
# 2800000 2850000 s4
# 2850000 2900000 s5
# 2900000 2950000 s6
	unit=safetext(unit)
	unit = unit+" "+unit # time_lab format
        start=int(start*10000000)
        end=int(end*10000000)
        assert end>start, "error : end time inf to start time"
        length_state=int((end-start)/5)
        line1=str(start+length_state*0)+" "+str(start+length_state*1)+" s2 "+unit+"\n"
        line2=str(start+length_state*1)+" "+str(start+length_state*2)+" s3\n"
        line3=str(start+length_state*2)+" "+str(start+length_state*3)+" s4\n"
        line4=str(start+length_state*3)+" "+str(start+length_state*4)+" s5\n"
        line5=str(start+length_state*4)+" "+str(end)+" s6\n"
        return line1+line2+line3+line4+line5


print("init raw text file:",sys.argv[1]," dest folder:",sys.argv[2])

FRAME_LENGTH=0.01 # State length is 10ms in Beer

txt_file=sys.argv[1]
dest_dir=sys.argv[2]
with open(txt_file, 'r') as myfile:
    data=myfile.read()
data_array=data.split('\n')

previous_sentence_id=''
current_sentence=''
text_corpora=''
new_data_array=''
for w in range(len(data_array)):
	w_split= data_array[w].split(' ')
	if w_split==['']:
		continue
        sentence_id =w_split[0]
	filename = sentence_id+'.time_lab'
	w_split=w_split[1:] # getting rid of sentence_id
	previous_state=''
	sentence=''
	start=0
	end=0
	length=FRAME_LENGTH
	previous_length=0
	previous_end=0
	previous_state=w_split[0].split('u')[1] #getting first element beforehand
	if len(previous_state)==1:
		previous_state+='x'
	w_split=w_split[1:]
	for i in range(len(w_split)):
		current_state=w_split[i].split('u')[1]
		if len(current_state)==1:
			current_state+='x'	
		if previous_state==current_state:
			length+=FRAME_LENGTH
			continue
		start=previous_end
		end=start+length
		sentence+= create_state_line(start,end,previous_state)
	#	sentence+=str(start)+" "+str(end)+" "+previous_state+"\n"
		previous_state=current_state
		length=FRAME_LENGTH
		previous_end=end
	# saving last symbol
	sentence+= create_state_line(end,end+length,current_state)
	#sentence+=str(end)+" "+str(end+length)+" "+current_state+"\n"
	
	with open(dest_dir+'/'+filename, 'w') as myfile:
   		myfile.write(sentence)	

