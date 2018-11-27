
# LSTM on Ossian from CSTR-Edinburgh

Some modification were brought to the initial project:
1) Getting two character at a time during parsing :
"scripts/processors/Phonetisers.py"

2) Updated Theano flags and removing bloking of gpu :

"scripts/util/submit.sh" 

3) LSTM config file :
"scripts/merlin_interface/feed_forward_dnn_ossian_acoustic_model.conf" 
4) LSTM were not implemented in original Ossian:
   a) Storage in Ossian format is now possible:
   "scripts/util/store_merlin_model.py" 
   b) Adding LSTM forward pass at test time
   "scripts/processors/NN.py"
5) Removing VSM features that did not show to be useful
"recipes/naive_01_nn.cfg" 

