#!bin/bash

# exemple : bash train_ossian.sh /mnt/zeroresources2019/ small_corpus_phones dur

DIR="$(cd "$(dirname -- "$0")" && pwd)"
OSSIAN=$DIR
HTK_USERNAME="robinalgayres"
HTK_PASSWORD="qt9vAh8m"
echo $OSSIAN

#checking parameters
if [ "$#" -ne 4 ]; then
    echo "bash run.sh /mnt/zeroresources2019/ small_corpus_phones nodur use_gpu"
    exit 1
fi

# getting corpus
CORPUS_PATH="$1"
CORPUS_NAME="$2"
SPEAKER="0107"
MODE="$3" #if "nodur", do not predict duration and use user provided time_lab
	  # if "novsm", do not add VSM to the linguistic features

#cp "$CORPUS_PATH/patch_ossian/feed_forward_dnn_ossian_acoustic_model.conf" "scripts/merlin_interface/feed_forward_dnn_ossian_acoustic_model.conf" # custom config for acoustic model (LSTM, DNN,...)

if [ "$MODE" = "nodur" ]; then	
	cp "$CORPUS_PATH/patch_ossian/Tokenisers.py" "scripts/processors/Tokenisers.py"
	cp "$CORPUS_PATH/patch_ossian/Aligner.py" "scripts/processors/Aligner.py"
	cp "$CORPUS_PATH/patch_ossian/speak.py" "scripts/speak.py"
	cp "$CORPUS_PATH/patch_ossian/Voice.py" "scripts/main/Voice.py" 
	cp "$CORPUS_PATH/patch_ossian/naive_nodur_01_nn.cfg" "recipes/naive_01_nn.cfg" 
fi

if [ ! -d "corpus" ]; then
	cp -r "$CORPUS_PATH/$CORPUS_NAME" "corpus/"
	find "corpus/" -type f -not -name $SPEAKER* -not -name "text.txt" -delete
fi

# getting merlin and htk
if [ ! -d "tools/merlin" ]; then
	./scripts/setup_tools.sh $HTK_USERNAME $HTK_PASSWORD
fi

cp "./patch_ossian/run_merlin.py" "tools/merlin/src/run_merlin.py" # best model is not saved if validation error increase before epoch 5

# training Ossian front end (aligning data and getting lexicon)
if [ ! -d "train" ]; then
	python ./scripts/train.py -s zs19_data -l english naive_01_nn || exit 1
fi

if [ $4 = 'use_gpu' ]; then
	PYTHON_CMD="./scripts/util/submit.sh"
else
	export THEANO_FLAGS=""
	PYTHON_CMD="python"
fi

if [ ! "$MODE" = "nodur" ]; then	
	# training Merlin's duration model
	$PYTHON_CMD ./tools/merlin/src/run_merlin.py $OSSIAN/train/english/speakers/zs19_data/naive_01_nn/processors/duration_predictor/config.cfg || exit 1

	# converting Merlin's duration model to Ossian's format
	python ./scripts/util/store_merlin_model.py $OSSIAN/train/english/speakers/zs19_data/naive_01_nn/processors/duration_predictor/config.cfg $OSSIAN/voices/english/zs19_data/naive_01_nn/processors/duration_predictor || exit 1

fi

# training Merlin's acoustic model
$PYTHON_CMD ./tools/merlin/src/run_merlin.py $OSSIAN/train/english/speakers/zs19_data/naive_01_nn/processors/acoustic_predictor/config.cfg || exit 1

# converting Merlin's acoustic model to Ossian's format
python ./scripts/util/store_merlin_model.py $OSSIAN/train/english/speakers/zs19_data/naive_01_nn/processors/acoustic_predictor/config.cfg $OSSIAN/voices/english/zs19_data/naive_01_nn/processors/acoustic_predictor || exit 1

echo " Training of OSSIAN is over "
