
clean: ## clean useless documents
	rm -rfv *.egg-info/
	rm -rfv .pytest_cache/
	rm -rfv dist/
	rm -rfv **/__pycache__

push: clean ## upload changes to github repo
	git add .
	git commit -m $m
