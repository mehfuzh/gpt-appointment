BUILD_DIR=bin

all: init build

init:
	chmod +x build.sh

build:
	./build.sh tecsius agent