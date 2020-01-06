#!/bin/bash

conda env create -f ds-env.yml

# Spell checking
jupyter contrib nbextension install --user
#jupyter nbextension enable spellchecker/main


# Configure notebook theme
jt -t monokai -f fira -fs 13 -nf ptsans -nfs 11 -N -kl -cursw 5 -cursc r -cellw 95% -T



