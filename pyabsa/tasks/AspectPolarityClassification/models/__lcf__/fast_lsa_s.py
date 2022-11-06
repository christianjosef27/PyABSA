# -*- coding: utf-8 -*-
# file: fast_lcf_s.py
# author: yangheng <hy345@exeter.ac.uk>
# Copyright (C) 2021. All Rights Reserved.

import torch
import torch.nn as nn
from transformers.models.bert.modeling_bert import BertPooler

from pyabsa.networks.sa_encoder import Encoder


class FAST_LSA_S(nn.Module):
    inputs = ['text_indices', 'spc_mask_vec', 'lcfs_vec', 'left_lcfs_vec', 'right_lcfs_vec']

    def __init__(self, bert, config):
        super(FAST_LSA_S, self).__init__()
        self.bert4global = bert
        self.config = config
        self.dropout = nn.Dropout(config.dropout)

        self.encoder = Encoder(bert.config, config)
        self.encoder_left = Encoder(bert.config, config)
        self.encoder_right = Encoder(bert.config, config)

        self.post_linear = nn.Linear(config.embed_dim * 2, config.embed_dim)
        self.linear_window_3h = nn.Linear(config.embed_dim * 3, config.embed_dim)
        self.linear_window_2h = nn.Linear(config.embed_dim * 2, config.embed_dim)

        self.post_encoder = Encoder(bert.config, config)
        self.post_encoder_ = Encoder(bert.config, config)
        self.bert_pooler = BertPooler(bert.config)

        self.dense = nn.Linear(config.embed_dim, config.output_dim)

    def forward(self, inputs):
        text_indices = inputs['text_indices']
        spc_mask_vec = inputs['spc_mask_vec'].unsqueeze(2)
        lcf_matrix = inputs['lcfs_vec'].unsqueeze(2)
        left_lcf_matrix = inputs['left_lcfs_vec'].unsqueeze(2)
        right_lcf_matrix = inputs['right_lcfs_vec'].unsqueeze(2)

        global_context_features = self.bert4global(text_indices)['last_hidden_state']
        masked_global_context_features = torch.mul(spc_mask_vec, global_context_features)

        # # --------------------------------------------------- #
        lcf_features = torch.mul(global_context_features, lcf_matrix)
        lcf_features = self.encoder(lcf_features)
        # # --------------------------------------------------- #
        left_lcf_features = torch.mul(masked_global_context_features, left_lcf_matrix)
        left_lcf_features = self.encoder_left(left_lcf_features)
        # # --------------------------------------------------- #
        right_lcf_features = torch.mul(masked_global_context_features, right_lcf_matrix)
        right_lcf_features = self.encoder_right(right_lcf_features)
        # # --------------------------------------------------- #

        if 'lr' == self.config.window or 'rl' == self.config.window:
            cat_features = torch.cat((lcf_features, left_lcf_features, right_lcf_features), -1)
            sent_out = self.linear_window_3h(cat_features)
        elif 'l' == self.config.window:
            sent_out = self.linear_window_2h(torch.cat((lcf_features, self.eta1 * left_lcf_features), -1))
        elif 'r' == self.config.window:
            sent_out = self.linear_window_2h(torch.cat((lcf_features, self.eta2 * right_lcf_features), -1))
        else:
            raise KeyError('Invalid parameter:', self.config.window)

        sent_out = torch.cat((global_context_features, sent_out), -1)
        sent_out = self.post_linear(sent_out)
        sent_out = self.dropout(sent_out)
        sent_out = self.post_encoder_(sent_out)
        sent_out = self.bert_pooler(sent_out)
        dense_out = self.dense(sent_out)

        return {'logits': dense_out, 'hidden_state': sent_out}
