REPOSITORY := djmitche
TAG := $(shell date --utc +%Y%m%d%H%M%S)

docker:
	docker build --no-cache -t $(REPOSITORY)/build-scope-tests:$(TAG) .
	docker tag -f $(REPOSITORY)/build-scope-tests:$(TAG) $(REPOSITORY)/build-scope-tests:latest
	docker push $(REPOSITORY)/build-scope-tests:$(TAG)
	docker push $(REPOSITORY)/build-scope-tests:latest
