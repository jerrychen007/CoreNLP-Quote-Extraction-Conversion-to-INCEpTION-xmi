# CoreNLP-Quote-Extraction-Conversion-to-INCEpTION-xmi </br>
This program is used to process and extract the quote extraction results from Stanford CoreNLP (https://stanfordnlp.github.io/CoreNLP/quote.html). Since the output file only contains the names of speakers and no index for the speaker location in text, this program can also search the nearest speaker position of the corresponding quote. </br>
</br>
INCEpTION is a rapid annotation platform available at https://inception-project.github.io. There is no direct way for CoreNLP to generate files in a format INCEpTION can recognize. The indirect method is to convert CoreNLP outputs to brat ann files, then to WebAnno-compatible XMI. </br>


Please refer to https://gist.github.com/reckart/306b8ffddd30bee1f3afd0468a9ad31d to configure your pipeline.groovy and TypeSystem.xml.
