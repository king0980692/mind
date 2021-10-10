echo "prepare the data for xlearn fm"

python3 ./encoderder/main.py -c ./encoderder/config/test_wiz1.json

~/xlearn/build/xlearn_train ./train_dir/train.txt -s 1 --disk 

~/xlearn/build/xlearn_predict ./test_dir/test.txt  ./train_dir/train.txt.model --sigmoid -o ./test_output.txt  --disk

echo "predict the model's outputs of test set"
python3 predict.py --file /tmp2/lychang/mind2/test/behaviors.tsv > ./prediction.txt

zip prediction.zip prediction.txt
