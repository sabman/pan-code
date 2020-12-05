#!/usr/bin/env python
# coding: utf-8

# Collect predictions of submitted systems:

# In[1]:


import pandas as pd
import json


# In[2]:


pair_id, same = [], []
for line in open('datasets/pan20-authorship-verification-test/truth.jsonl'):
    pair = json.loads(line)
    pair_id.append(pair['id'])
    same.append(int(pair['same']))


# In[3]:


df = pd.DataFrame(zip(pair_id, same), columns=('id', 'same'))
df


# In[4]:


from glob import glob
systems = []

for pred_file in sorted(glob('submissions/*/answers.jsonl')):
    print(pred_file)
    scores = {}
    for line in open(pred_file):
        res = json.loads(line)
        val = res['value']
        if isinstance(val, list):
            val = val[0]
        scores[res['id']] = val
    predictions = [scores[i] for i in df['id']]
    system = pred_file.split('/')[-2]
    df[system] = predictions
    systems.append(system)


# In[5]:


df.head()


# In[6]:


df.to_excel('predictions.xlsx')


# ## Evaluations

# In[7]:


from pan20_verif_evaluator import *


# In[8]:


evaluations = []
metrics = {'AUC': auc, 'c@1': c_at_1, 'F1': f1, 'F0.5u': f_05_u_score}
for system in systems:
    evaluations.append([metrics[m](df['same'], df[system]) for m in metrics])

evaluations = pd.DataFrame(evaluations, columns=list(metrics.keys()), index=systems)
evaluations


# In[9]:


evaluations['Overall'] = evaluations.mean(axis=1)
evaluations = evaluations.sort_values('Overall', ascending=False)
evaluations


# In[10]:


evaluations.to_excel('metrics.xlsx')

