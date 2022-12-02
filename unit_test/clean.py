# -*- coding: utf-8 -*-
# file: clean.py
# time: 06/11/2022 11:07
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# GScholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# ResearchGate: https://www.researchgate.net/profile/Heng-Yang-17/research
# Copyright (C) 2022. All Rights Reserved.
import os

import findfile

from pyabsa.utils.pyabsa_utils import fprint

for f in findfile.find_cwd_files(or_key=['.zip', '.cache', '.mv', '.json', '.txt'], exclude_key='glove', recursive=1):
    os.remove(f)
fprint('Cleaned all files in the current directory.')
