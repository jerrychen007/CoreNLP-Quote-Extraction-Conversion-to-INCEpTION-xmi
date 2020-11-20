#!/usr/bin/env groovy
@Grab(group='org.dkpro.core', module='dkpro-core-io-brat-asl', version='2.1.0')
import org.dkpro.core.io.brat.*;
@Grab(group='org.dkpro.core', module='dkpro-core-io-xmi-asl', version='2.1.0')
import org.dkpro.core.io.xmi.*;
@Grab(group='org.slf4j', module='slf4j-nop', version='2.0.0-alpha1', scope='test')

import static org.apache.uima.util.CasCreationUtils.*; 
import static org.apache.uima.fit.pipeline.SimplePipeline.*;
import static org.apache.uima.fit.factory.CollectionReaderFactory.*;
import static org.apache.uima.fit.factory.AnalysisEngineFactory.*;
import static org.apache.uima.fit.factory.TypeSystemDescriptionFactory.*;

def ts = mergeTypeSystems([
  createTypeSystemDescription(),
  createTypeSystemDescriptionFromPath("TypeSystem.xml")]);

runPipeline(
  createReaderDescription(BratReader, ts,
    BratReader.PARAM_SOURCE_LOCATION, "*.ann",
    BratReader.PARAM_TEXT_ANNOTATION_TYPE_MAPPINGS, [
        "Speaker -> webanno.custom.Component",
        "Quote -> webanno.custom.Component",
		"Speak -> webanno.custom.Relation"],
    BratReader.PARAM_TEXT_ANNOTATION_TYPES, "webanno.custom.Component:value",
    BratReader.PARAM_RELATION_TYPES,  "webanno.custom.Relation:Governor:Dependent{A}:value"),
  
createEngineDescription(XmiWriter, ts,
    XmiWriter.PARAM_TARGET_LOCATION, "xmi outputs",
    XmiWriter.PARAM_STRIP_EXTENSION, true))