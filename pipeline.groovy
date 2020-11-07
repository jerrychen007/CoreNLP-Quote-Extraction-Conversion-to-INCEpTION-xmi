#!/usr/bin/env groovy
@Grab(group='de.tudarmstadt.ukp.dkpro.core', 
  module='de.tudarmstadt.ukp.dkpro.core.io.brat-asl', 
  version='1.9.3')
@Grab(group='de.tudarmstadt.ukp.dkpro.core', 
  module='de.tudarmstadt.ukp.dkpro.core.io.xmi-asl', 
  version='1.9.3')

import static org.apache.uima.util.CasCreationUtils.*; 
import static org.apache.uima.fit.pipeline.SimplePipeline.*;
import static org.apache.uima.fit.factory.CollectionReaderFactory.*;
import static org.apache.uima.fit.factory.AnalysisEngineFactory.*;
import static org.apache.uima.fit.factory.TypeSystemDescriptionFactory.*;

import de.tudarmstadt.ukp.dkpro.core.io.brat.*;
import de.tudarmstadt.ukp.dkpro.core.io.xmi.*;
import de.tudarmstadt.ukp.dkpro.core.io.webanno.tsv.*;

def ts = mergeTypeSystems([
  createTypeSystemDescription(),
  createTypeSystemDescriptionFromPath("TypeSystem.xml")]);

runPipeline(
  createReaderDescription(BratReader, ts,
    BratReader.PARAM_SOURCE_LOCATION, "*.ann",
    BratReader.PARAM_TYPE_MAPPINGS, [
		"Quote -> webanno.custom.Quote",
		"Speaker  -> webanno.custom.SpeakerofQuote"],
	BratReader.PARAM_TEXT_ANNOTATION_TYPES, [
	"webanno.custom.Quote:value",
	"webanno.custom.SpeakerofQuote:value"],
    BratReader.PARAM_RELATION_TYPES,  "webanno.custom.Speaker:Governor:Dependent{A}:value"),
  
  createEngineDescription(XmiWriter, ts,
    XmiWriter.PARAM_TARGET_LOCATION, "xmi outputs",
    XmiWriter.PARAM_STRIP_EXTENSION, true))