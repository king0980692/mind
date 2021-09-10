# Mind news recommendations
using **Factorial Machine** to recommend the news.


## Dataset Review
### Input

#### behaviors.tsv
The behaviors.tsv file contains the impression logs and users' news click hostories. It has 5 columns divided by the tab symbol:

| Impression ID | User ID | Time                   |                                                      History                                                      | Impressions                                                                                                                                                               |
| ------------- | ------- | ---------------------- |:-----------------------------------------------------------------------------------------------------------------:| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1             | U87243  | 11/10/2019 11:30:54 AM | N8668 N39081 N65259 N79529 N73408 N43615 N29379 N32031 N110232 N101921 N12614 N129591 N105760 N60457 N1229 N64932 | N78206-0 N26368-0 N7578-0 N58592-0 N19858-0 N58258-0 N18478-0 N2591-0 N97778-0 N32954-0 N94157-1 N39404-0 N108809-0 N78699-1 N71090-1 N40282-0 N31174-1 N37924-0 N27822-0 |

---




#### news.tsv


| News ID | Category | SubCategory | Abstract | URL | Title Entities | Title Entities |
| ------- | -------- | ----------- | -------- | --- | -------------- | -------------- |
| N45436    | news | news science and technology |  Walmart Slashes Prices on Last-Generation iPads Apple's new iPad releases bring big deals on last year's models. |  https://assets.msn.com/labs/mind/AABmf2I.html   | [{"Label": "IPad", "Type": "J", "WikidataId": "Q2796", "Confidence": 0.999, "OccurrenceOffsets": [42], "SurfaceForms": ["iPads"]}, {"Label": "Walmart", "Type": "O", "WikidataId": "Q483551", "Confidence": 1.0, "OccurrenceOffsets": [0], "SurfaceForms": ["Walmart"]}] | [{"Label": "IPad", "Type": "J", "WikidataId": "Q2796", "Confidence": 0.999, "OccurrenceOffsets": [12], "SurfaceForms": ["iPad"]}, {"Label": "Apple Inc.", "Type": "O", "WikidataId": "Q312", "Confidence": 0.999, "OccurrenceOffsets": [0], "SurfaceForms": ["Apple"]}] 
                 
#### reduction

First look at the behaviors.tsv, the **Time column** we won't used, so just drop it, the previous table can be expanded as :


> Do **row_split** at impression , and indicate the row seperator=' '
```bash
python DataEncode.py --task 'dataSplit' -i ../data/behaviors.tsv  4 target '\t' --action row_split ' ' -o ../data/behaviors_split.tsv
```


| User ID | History | News ID - Target |
| ------- | ------- |:----------------:|
| U87243  | N64932  |     N78206-0     |
| U87243  | N64932  |    N26368- 0     |
| ...     | ...     |   ...      ...   |
| U87243  | N64932  |     N94157-1     |
| ...     | ...     |  ...     - ...   |
| U87243  | N64932  |     N27822-0     |

then,
> Do **col_split** at NewsID-target column , and indicate the col seperator='-'
```bash
python DataEncode.py --task 'dataSplit' -i  ../data/behaviors_split.tsv 4 target '\t' --action col_split '-' -o ../data/behaviors_split2.tsv
```



| User ID | History | News ID | Target |
| ------- | ------- |:------- |:------:|
| U87243  | N64932  | N78206  |   0    |
| U87243  | N64932  | N26368  |   0    |
| ...     | ...     | ...     |  ...   |
| U87243  | N64932  | N94157  |   1    |
| ...     | ...     | ...     |  ...   |
| U87243  | N64932  | N27822  |   0    |

> Do col_split at History column
```bash
python DataEncode.py --task 'dataSplit' -i ./test_ex.tsv 3 target '\t' --action col_split '-' -o ./test_ex2.tsv
```

| Target | User ID | His_1 | His_2 | ... | His_n | News ID |
| ------ | ------- | ----- | ----- | --- | ----- | --- |
| 0 | U87243 | N8668 | N39081 | ... | N64932 | N78206 |
| 0 | U87243 | N8668 | N39081 | ... | N64932 | N26368 |
|...|...|...|...| ... |...|...|
| **1** | U87243 | N8668 | N39081 | ... | N64932 | N94157 |
|...|...|...|...| ... |...|...|
| 0 | U87243 | N8668 | N39081 | ... | N64932 | N27822 |

> map the News ID into  news' related feature

---

| Target | User ID | His_1 | His_2 | ... | His_n | News ID |
| ------ | ------- | ----- | ----- | --- | ----- | --- |
| 0 | U87243 | N8668 | N39081 | ... | N64932 | ('lifestyle', 'lifestylehomeandgarden') |
| 0 | U87243 | N8668 | N39081 | ... | N64932 | ('news', 'newscrime') |
|...|...|...|...| ... |...|...|
| **1** | U87243 | N8668 | N39081 | ... | N64932 | ('finance', 'markets') |

then, encode those specifc columns and output to libsvm format

