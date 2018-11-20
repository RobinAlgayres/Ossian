#!bin/bash
#python ./scripts/speak.py -l english -s zs19_data -o ./test/wav/output.wav naive_01_nn /mnt/zeroresources2019/corpus_phone_nospace/english/speakers/zs19_data/txt/0107_400123_0000.txt

for filename in $1/*.txt; do
	wav_filename=$(basename "$filename" .txt)".wav"
	python ./scripts/speak.py -l english -s zs19_data -o ./test/wav/"synth_"$wav_filename naive_01_nn $filename
done
