# -*- coding: utf-8 -*-
# file: run_apc_inference_set_generation.py
# time: 2021/5/21 0021
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

# This function coverts a ABSA datasets to inference set, try to convert every datasets found in the dir
# please do check the output file!
from pyabsa.utils.absa_utils.absa_utils import generate_inference_set_for_apc, convert_apc_set_to_atepc_set


def test_apc_inference_set_generation():
    generate_inference_set_for_apc('integrated_datasets')


def test_apc_inference_set_conversion():
    convert_apc_set_to_atepc_set('integrated_datasets')
