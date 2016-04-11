# DrumsFinder
This project aims to write the drums music sheet from an audio source.

I'm unsing neural network with Lasagne for Theano to predict the partition. The network is looking for features in the frequencies domain to predict the drum part.

Right now the project uses a Multi-Layer Perceptron (MLP) model, from Lasagne's tutoriel, to predict samples isolated in music files gathered around the web.
It has a precision of 80%, which is not really representative because of the low number of samples.

TODO :
- Use a long short-term memory (LSTM) network to handle the evolution in time of a sample.
- Classify overlaping samples.
- Classify samples following each other in the same file.
- Classify drums with other instruments playing above them. 
- Retreive the frequencies of the classes of a particular song to isolate the drums.
- Write the partition in D3js.
- Create an midi exporter.  
