.PHONY: all git-hooks pdf

GENERATED_ADOCS = generated/stf-records.adoc generated/stf-protocols.adoc

INCLUDES = include/*.adoc

DOC_DEPS = $(INCLUDES) $(GENERATED_ADOCS) LICENSE stf-spec.adoc

all: generated/stf-spec-github.adoc $(GENERATED_ADOCS)
 
.git/hooks/pre-commit: scripts/pre-commit
	cp scripts/pre-commit .git/hooks/pre-commit

.git/hooks/post-commit: scripts/post-commit
	cp scripts/post-commit .git/hooks/post-commit

git-hooks: .git/hooks/pre-commit .git/hooks/post-commit

generated/stf-records.adoc: records/*.yml scripts/gen-records.py .git/hooks/pre-commit .git/hooks/post-commit
	./scripts/gen-records.py
	touch .dirty

generated/stf-protocols.adoc: protocols/*.yml scripts/gen-protocols.py .git/hooks/pre-commit .git/hooks/post-commit
	./scripts/gen-protocols.py
	touch .dirty

scripts/flatten.sh: scripts/bundle-setup.sh

scripts/pdf.sh: scripts/bundle-setup.sh

generated/stf-spec-github.adoc: $(DOC_DEPS) scripts/flatten.sh
	./scripts/flatten.sh
	touch .dirty

generated/stf-spec.pdf: $(DOC_DEPS) scripts/pdf.sh
	./scripts/pdf.sh

pdf: generated/stf-spec.pdf
