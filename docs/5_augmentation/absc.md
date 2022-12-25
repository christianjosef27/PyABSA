﻿### Aspect-based Sentiment Classification

```python3
import random

from pyabsa.tasks.AspectPolarityClassification import APCDatasetList

from pyabsa import AspectPolarityClassification as APC
from pyabsa.augmentation import auto_aspect_sentiment_classification_augmentation
import warnings

warnings.filterwarnings('ignore')

for dataset in [
    APCDatasetList.Laptop14,
    # APCDatasetList.Restaurant14,
    # APCDatasetList.Restaurant15,
    # APCDatasetList.Restaurant16,
    # APCDatasetList.MAMS
]:
    for model in [
        APC.APCModelList.FAST_LSA_T_V2,
        # APC.APCModelList.FAST_LSA_S_V2,
        # APC.APCModelList.BERT_SPC_V2
    ]:
        config = APC.APCConfigManager.get_apc_config_english()
        config.model = model
        config.pretrained_bert = 'microsoft/deberta-v3-base'
        config.evaluate_begin = 5
        config.max_seq_len = 80
        config.num_epoch = 30
        config.log_step = 10
        config.dropout = 0
        config.cache_dataset = False
        config.l2reg = 1e-8
        config.lsa = True
        config.seed = [random.randint(0, 10000) for _ in range(3)]

        # this code will automatically augment the dataset and train the model
        auto_aspect_sentiment_classification_augmentation(config=config, dataset=dataset, device='cuda')
    
```