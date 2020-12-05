#!/usr/bin/env python
# coding: utf-8

# # Preprocess

# In[31]:


import shutil
import os
import glob
import random
import json

rnd_seed = 1234
random.seed(rnd_seed)

import spacy


# In[16]:


def clean_dir(dirname):
    try:
        shutil.rmtree(dirname)
    except FileNotFoundError:
        pass
    os.mkdir(dirname)


# In[17]:


allowed = set('ADJ NOUN VERB'.split())


# In[18]:


nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
nlp.max_length = 10000000


# In[27]:


def plain_text(infile, outdir, max_pairs=None):
    clean_dir(outdir)
    
    with open(infile) as inf:
        for line_idx, line in enumerate(inf):
            if max_pairs and line_idx >= max_pairs:
                break
            pair = json.loads(line)
            pair_id = pair['id']
            for idx, text in enumerate(pair['pair']):
                text_idx = pair_id + '_' + str(idx)
                tokens = nlp(text)
                if not tokens:
                    continue
                new_fn = f'{outdir}/{text_idx}.txt'
                with open(new_fn, 'w') as f:
                    for t in tokens:
                        if t.pos_ in allowed and t.is_alpha and not t.is_stop:
                            w = t.text.lower()
                            if len(w) > 1:
                                f.write(w + ' ')


# In[30]:


plain_text(infile='datasets/pan20-authorship-verification-training-small/pairs.jsonl',
           outdir='plain_text_train_small',
           max_pairs=None)

