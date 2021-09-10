rm -f ./dev_*.txt
rm -f ./test_*.txt

rm -f prediction.txt
rm -f *.zip
rm -f ./train_dir/*.model
echo "finishing clean the environment"

echo "prepare the data for xlearn fm"

python prepare.py --train --users_id --news_id 
python prepare.py --dev --users_id --news_id 
python prepare.py --test  --users_id --news_id

~/xlearn/build/xlearn_train ./train_dir/train.txt -s 1 --disk 


~/xlearn/build/xlearn_predict ./dev_dir/dev.txt  ./train_dir/train.txt.model --sigmoid -o dev_output.txt --disk

echo "predict the model's outputs of dev set"
python predict.py --file ../dev/behaviors.tsv > dev_prediction.txt

echo "evaluate the score of dev set"
python evaluate.py ./dev_prediction.txt


~/xlearn/build/xlearn_predict ./test_dir/test.txt  ./train_dir/train.txt.model --sigmoid -o test_output.txt --disk

echo "predict the model's outputs of test set"
python predict.py --file ../test/behaviors.tsv > ./prediction.txt

zip prediction.zip prediction.txt
