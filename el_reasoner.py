#! /usr/bin/python

import sys
from py4j.java_gateway import JavaGateway

# arguments:
# INPUT: PROGRAMM_NAME ONTOLOGY_FILE CLASS_NAME
# i.e.: el_reasoner.py SushiOntology.rdf Maki
if len(sys.argv) >= 2:
    ontology_file = sys.argv[1]
    class_name = sys.argv[2]
else:
    ontology_file = "SushiOntology.rdf"
    class_name = "Maki"

# JAVA connection stuff, make sure to run java file first using:
# java -jar dl4python-0.1-jar-with-dependencies.jar
gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()

# load an ontology from a file
ontology = parser.parseFile(ontology_file)

# change all conjunctions to at most two conjuncts
gateway.convertToBinaryConjunctions(ontology)

# get the TBox axioms
tbox = ontology.tbox()
axioms = tbox.getAxioms()

# get all concepts occurring in the ontology
allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

# access the type of axioms:
foundGCI = False
foundEquivalenceAxiom = False

for axiom in axioms:
    axiomType = axiom.getClass().getSimpleName()
    if (not foundGCI
            and axiomType == "GeneralConceptInclusion"):
        foundGCI = True
    elif (not foundEquivalenceAxiom
          and axiomType == "EquivalenceAxiom"):
        foundEquivalenceAxiom = True

# accessing the relevant types of concepts:
foundConceptName = False
foundTop = False
foundExistential = False
foundConjunction = False
foundConceptTypes = set()

for concept in allConcepts:
    conceptType = concept.getClass().getSimpleName()
    if not (conceptType in foundConceptTypes):
        foundConceptTypes.add(conceptType)
    if not foundConceptName and conceptType == "ConceptName":
        foundConceptName = True
    elif not foundTop and conceptType == "TopConcept$":
        foundTop = True
    elif not foundExistential and conceptType == "ExistentialRoleRestriction":
        foundExistential = True
    elif not foundConjunction and conceptType == "ConceptConjunction":
        foundConjunction = True

# Creating EL concepts and axioms
elFactory = gateway.getELFactory()

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role, conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top, existential)

gci = elFactory.getGCI(conjunctionAB, conjunction2)


# what we have to do:
def get_subsumers(concept_name):
    return [1, 2, 3]


subsumers = get_subsumers(class_name)

# should only print "1 class name per line, no other output"
for concept in subsumers:
    # print(formatter.format(concept))
    print(concept)
