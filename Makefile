deploy:
	python -m pygbag ./src

clean:
	rm -rf ./src/build

run:
	python ./src/main.py

build:
	python -m pygbag --build ./src