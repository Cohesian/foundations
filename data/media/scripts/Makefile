SCENE ?= scenes/lesson_01.py
CLASS ?= Lesson01

.PHONY: preview test prod

preview:  ## fast local preview
	loci-render $(SCENE) $(CLASS) -vq l -p

test:     ## quick render, no preview
	loci-render $(SCENE) $(CLASS) -vq l --no-preview

prod:     ## higher quality export
	loci-render $(SCENE) $(CLASS) -vq h --no-preview
