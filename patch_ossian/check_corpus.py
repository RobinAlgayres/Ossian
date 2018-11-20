

import glob
from shutil import copyfile
import sys

corpus=sys.argv[1]
txt_dir=corpus+"/english/speakers/zs19_data/txt"
wav_dir=corpus+"/english/speakers/zs19_data/wav"

extension=".wav"
all_txt_files=glob.glob(txt_dir+"/*")
all_wav_files=glob.glob(wav_dir+"/*")

assert len(all_wav_files)==len(all_txt_files),"There should be as many wav and txt files in Ossian corpus"


