# Mind news recommendations

using **Factorial Machine** to recommend the news.

## Dataset infomation 
https://github.com/msnews/msnews.github.io/blob/master/assets/doc/introduction.md

## Preprocess

0. Generate the **map file** using below instruction

``` bash
python ./preprocess/gen_map.py -i ../data/news.tsv -k 0 -t 1,2 -s '\t' -o ./map.json
```

1. **Row split** the impression column 

```bash
 python ./preprocess/row_split.py -i ../data/behaviors.tsv -t 4 -s '\t' -d ' ' -o ../data/beh_split.tsv
```

| User ID |   History   | Impression |
| ------- |:-----------:|:----------:|
| U0      |  N1 ... N9  |    N0-0    |
| U1      | N11 ... N19 |   N10-0    |
| ...     |     ...     |    ...     |
| U9      | N91 ... N99 |   N90-1    |



2. **Column split** the impression column

```bash
python ./preprocess/col_split.py -i ../data/beh_split.tsv -t 4 -s '\t' -d '-' -o ../data/beh_split2.tsv
```

| User ID |      History       | News ID | Target |
| ------- |:------------------:|:-------:| ------ |
| U0      |  N1  N2  ...  N9   |   N0    | 0      |
| U1      | N11  N12  ...  N19 |   N10   | 1      |
| ...     |        ...         |   ...   | ...    |
| U9      | N91  N92  ...  N99 |   N90   | 0      |




3. **Column map** the News ID column 

```bash
python ./preprocess/col_map.py -i ../data/beh_split2.tsv -t 4 -s '\t' -m ./map.json -o ../data/beh_split3.tsv
```


| User ID |      History       | News ID |       mapped column        | Target |
| ------- |:------------------:| ------- |:--------------------------:| ------ |
| U0      |  N1  N2  ...  N9   | N0      |        sports golf         | 0      |
| U1      | N11  N12  ...  N19 | N10     |      news  newsworld       | 1      |
| ...     |        ...         | ...     |            ...             | ...    |
| U9      | N91  N92  ...  N99 | N90     | lifestyle  lifestyleroyals | 0      |


4. **Column split** at the mapped column

```bash
python ./preprocess/col_split.py -i ../data/beh_split3.tsv -t 5 -s '\t' -d ' ' -o ../data/beh_split4.tsv
```


| User ID |      History       | News ID | news cat  |   news subcat   | Target |
| ------- |:------------------:| ------- |:--------- |:---------------:| ------ |
| U0      |  N1  N2  ...  N9   | N0      | sports    |      golf       | 0      |
| U1      | N11  N12  ...  N19 | N10     | news      |    newsworld    | 1      |
| ...     |        ...         | ...     | ...       |                 | ...    |
| U9      | N91  N92  ...  N99 | N90     | lifestyle | lifestyleroyals | 0      |





Now the mind dataset is the general csv-like file.

---

## Encoder

* Only support **category encoding**

* Based on the column to encode
    * :bulb: If the column is a list structure, it will be flatten before encoding.

* Unseen label will use the same index



| User ID |     History     | News ID | news cat | news subcat | Target |
|:-------:|:---------------:| ------- |:--------:|:-----------:|:------:|
|    0    | 10  11  ...  19 | 100     |   110    |     120     |   0    |
|    1    | 20  21  ...  29 | 101     |   111    |     121     |   1    |
|   ...   |       ...       | ...     |   ...    |     ...     |  ...   |
|    9    | 90  91  ...  99 | 109     |   119    |     129     |   0    |


> Generate the sparse libsvm format

```
0 0:1 10:1 11:1 ... 19:1 100:1 110:1 120:1
1 1:1 20:1 21:1 ... 29:1 101:1 111:1 121:1
...
0 9:1 90:1 91:1 ... 99:1 109:1 119:1 129:1

```
