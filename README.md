# CoreNLP-Quote-Extraction-Conversion-to-INCEpTION-xmi </br>
This project is used to process and extract the quote extraction results from Stanford CoreNLP [Quote Extraction And Attribution](https://stanfordnlp.github.io/CoreNLP/quote.html). Since the output file only contains the names of speakers and no index for the speaker location in text, this program can also search the nearest speaker position of the corresponding quote. </br>
</br>
INCEpTION is a rapid annotation platform available at [INCEpTION - Welcome](https://inception-project.github.io). There is no direct way for CoreNLP to generate files in a format INCEpTION can recognize. The indirect method is to convert CoreNLP outputs to brat ann files, then to WebAnno-compatible XMI. </br>
</br>
Please install Groovy and DKPro Core before converting brat ann files. Tutorial available at [DKPro Core - Intro using Groovy](https://dkpro.github.io/dkpro-core/pages/groovy-intro/) </br>
Please refer to [Convert brat ann files to WebAnno-compatible XMI](https://gist.github.com/reckart/306b8ffddd30bee1f3afd0468a9ad31d) to configure your pipeline.groovy and TypeSystem.xml.

## Pipeline to process outputs from CoreNLP Quote Extraction

1. Export a random document on INCEpTION and choose UIMA CAS XMI format.

2. Unzip the document and copy the TypeSystem.xml to the same directory of Extract quotes - New.py.

3. Put the CoreNLP .out files and original text files under the same directory of Extract quotes - New.py. 

4. Run Extract quotes - New.py.

5. Open command prompt and run: groovy pipeline. (May need to install Java, [Groovy](http://www.groovy-lang.org/download.html) and [DKPro Core](https://dkpro.github.io/dkpro-core/pages/groovy-intro/))

6. Go into xmi outputs folder and run the Create Relation.py.

7. Upload the generated xmi files to INCEpTION.

You may need to adjust parameters in python programs and groovy.pipeline to match your Layers setting on INCEpTION/WebAnno.

