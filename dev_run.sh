echo "prepare the data for xlearn fm"

python3 ./encoderder/main.py -c ./encoderder/config/dev_wiz1.json

~/xlearn/build/xlearn_train ./train_dir/train.txt -s 1 --disk 


~/xlearn/build/xlearn_predict ./dev_dir/dev.txt  ./train_dir/train.txt.model --sigmoid -o ./dev_output.txt 

echo "predict the model's outputs of dev set"
python3 predict.py --file /tmp2/lychang/mind2/dev/behaviors.tsv > ./dev_prediction.txt

echo "evaluate the score of dev set"
python3 evaluate.py ./dev_prediction.txt
