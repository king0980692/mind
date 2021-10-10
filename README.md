# MIND news recommadation using FM

## Prerequisite
1. python3.6+
2. xlearn or other FM implementation

## Clone this repo
```bash
git clone --recurse-submodules git@github.com:king0980692/mind.git
```

## This Repo Structure
![Repo Structure](img.png)


## Usage
We collect the original dev set's impression results into `truth.txt`, so we split this experiment into **dev_part** and **test_part** .

### dev part 
Using the `result.txt` to evaulate the models result

### test part 
Using the **official test data** to evaulate the model result, you can upload your prediction to [here](https://competitions.codalab.org/competitions/24122#participate-get-data)

### Script
💡 For both part , I write two script to run the experiment :  `dev_run.sh` and `test_run.sh` 

Check them for detail !!
