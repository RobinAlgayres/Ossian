#!bin/bash
for filename in $1/*.txt; do
	wav_filename=$(basename "$filename" .txt)".wav"
	echo "Synthesizing $2/$wav_filename"
	python ./scripts/speak.py -l english -s zs19_data -o $2/$wav_filename naive_01_nn $filename > log
done
