.PHONY: all

all: generated/stf-records.adoc

.git/hooks/pre-commit: scripts/pre-commit
	cp scripts/pre-commit .git/hooks/pre-commit

.git/hooks/post-commit: scripts/post-commit
	cp scripts/post-commit .git/hooks/post-commit

git-hooks: .git/hooks/pre-commit .git/hooks/post-commit

generated/stf-records.adoc: records/*.yml scripts/gen-records.py .git/hooks/pre-commit .git/hooks/post-commit
	./scripts/gen-records.py
	touch .dirty
