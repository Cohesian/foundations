SCENE ?= scenes/lesson_01.py
CLASS ?= Lesson01

.PHONY: preview test prod

preview:  ## fast local preview
	loci-render $(SCENE) $(CLASS) -vq l -p

test:     ## quick render, no preview
	loci-render $(SCENE) $(CLASS) -vq l --no-preview

prod-hd:     ## higher quality export
	loci-render $(SCENE) $(CLASS) -vq h -vf 60 -as openai -ao voice=alloy,model=tts-1-hd