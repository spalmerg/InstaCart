data/surprise.csv:
	python src/features/build_features.py
features:data/surprise.csv

models/rid_to_name.pkl:
	python src/features/build_key.py
key:models/rid_to_name.pkl

models/model.pkl:
	python src/models/model.py
model:models/model.pkl

clean:
	rm data/surprise.csv
	rm models/rid_to_name.pkl
	rm models/model.pkl

all: features model key