# DrumsFinder
This project aims to write the drums music sheet from an audio source.

I'm unsing neural network with TensorFlow to write the partition. The network is looking for features in the frequencies domain to label the drum part.

Creation of the dataset
- Music band kind enough to give the score of their music 
  - Atlantis Chronicles
- Generated audio with a drum machine (generates humanization)
  - Ezdrummer
- Online database
  - All chart
  - ultimate-guitar

TODO :
- Use a long short-term memory (LSTM) network to handle the evolution in time of a sample.
- Retreive the frequencies of the classes of a particular song to isolate the drums.
- Create an midi exporter.  


Questions :
- Faire une covolution 1D VS 2D ? Repérer des attributs indépendament du pitch -> nécessite une normalisation des l'espace des fréquences qui n'est pas linéaire
- Feeder une MFC plutôt qu'une DFT https://en.wikipedia.org/wiki/Mel-frequency_cepstrum ?
- Détecter les cas sans label: ajouter un label "sans label" ou mettre tous les labels à 0 ? 
