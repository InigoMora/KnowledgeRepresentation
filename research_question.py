#! /usr/bin/python

from py4j.java_gateway import JavaGateway
import time
import numpy as np
from matplotlib import pyplot as plt
import os

printResults = True
printSubsumers = True
time_iterations = 100

# Tests:

# amino acid ontology
# ontology_path = "amino acid.amino-acid-ontology.2.owl.xml"
# getSubsumersOfConcept = '"TinyPolarAminoAcid"'

# basic formal ontology
# ontology_path = "bfo.basic-formal-ontology.2.owl.xml"
# getSubsumersOfConcept = 'BFO_0000019'

# clinical trials ontology
# ontology_path = "cto.clinical-trials-ontology.1.owl.xml"
# getSubsumersOfConcept = 'Multicentered_Trials'

# human disease ontology
# ontology_path = "doid.human-disease-ontology.589.owl.xml"
# getSubsumersOfConcept = 'DOID_6284'

# foodon ontology
# ontology_path = "foodon.foodon.1.owl.xml"
# getSubsumersOfConcept = 'FOODON_03500028'

# evidence and conclusion ontology
# ontology_path = "eco.evidence-and-conclusion-ontology.49.owl.xml"
# getSubsumersOfConcept = 'ECO_0000246'

ontology_path = "eco.evidence-and-conclusion-ontology.49.owl.xml"
getSubsumersOfConcept = 'ECO_0000246'

ontology_name = ontology_path.split('.')[0]
ontology_name = "evidence and conclusion"

save_directory = f"part3_results/{ontology_name}"
# if path doesn't exist, create directory
if not os.path.exists(f"part3_results/{ontology_name}"):
    os.makedirs(f"part3_results/{ontology_name}")

# dl4python stuff
gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
ontology = parser.parseFile(f"ontologies/{ontology_path}")
gateway.convertToBinaryConjunctions(ontology)

tbox = ontology.tbox()
axioms = tbox.getAxioms()

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

foundGCI = False
foundEquivalenceAxiom = False
for axiom in axioms:
    axiomType = axiom.getClass().getSimpleName()
    if (not (foundGCI)
            and axiomType == "GeneralConceptInclusion"):
        foundGCI = True
    elif (not (foundEquivalenceAxiom)
          and axiomType == "EquivalenceAxiom"):
        for concept in axiom.getConcepts():
            foundEquivalenceAxiom = True

foundConceptName = False
foundTop = False
foundExistential = False
foundConjunction = False
foundConceptTypes = set()

for concept in allConcepts:
    conceptType = concept.getClass().getSimpleName()
    if (not (conceptType in foundConceptTypes)):
        foundConceptTypes.add(conceptType)
    if (not (foundConceptName) and conceptType == "ConceptName"):
        foundConceptName = True
    elif (not (foundTop) and conceptType == "TopConcept$"):
        foundTop = True
    elif (not (foundExistential) and conceptType == "ExistentialRoleRestriction"):
        foundExistential = True
    elif (not (foundConjunction) and conceptType == "ConceptConjunction"):
        foundConjunction = True

elFactory = gateway.getELFactory()
conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role, conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top, existential)
gci = elFactory.getGCI(conjunctionAB, conjunction2)

# main part of the scientific question

elk = gateway.getELKReasoner()
hermit = gateway.getHermiTReasoner()

target = elFactory.getConceptName(getSubsumersOfConcept)

elk_results = []
elk_subsumers = None

# time results and save them to elk_results
for _ in range(time_iterations):
    elk.setOntology(ontology) # important to reset the ontology or else he retrieves the previous result
    elk_start_time = time.time()
    elk_subsumers = elk.getSubsumers(target)
    elk_end_time = time.time()
    elk_total_time = elk_end_time - elk_start_time
    elk_results.append(elk_total_time)

if printSubsumers:
    print("ELK subsumers result:")
    for concept in elk_subsumers.toArray():
        print(" - ", formatter.format(concept))
    print("(", len(elk_subsumers), " in total)")

# save results to file
with open(f'{save_directory}/{ontology_name}-elk-results.txt', 'w') as file:
    for result in elk_results:
        file.write(f"{result}\n")

hermit_results = []
hermit_subsumers = None

# time results and save them to hermit_results
for _ in range(time_iterations):
    hermit.setOntology(ontology) # important to reset the ontology or else he retrieves the previous result
    hermit_start_time = time.time()
    hermit_subsumers = hermit.getSubsumers(target)
    hermit_end_time = time.time()
    hermit_total_time = hermit_end_time - hermit_start_time
    hermit_results.append(hermit_total_time)

if printSubsumers:
    print("Hermit subsumers result:")
    for concept in hermit_subsumers.toArray():
        print(" - ", formatter.format(concept))
    print("(", len(hermit_subsumers), " in total)")

with open(f'{save_directory}/{ontology_name}-hermit-results.txt', 'w') as file:
    for result in hermit_results:
        file.write(f"{result}\n")

#################
# data analysis #
#################

# boxplots
# create boxplot
plt.boxplot(elk_results, labels=(["ELK"]))
plt.title(f'{ontology_name} ontology (with {time_iterations} iterations)')
plt.xlabel('')
plt.ylabel('Time in seconds')
# save plot
plt.savefig(f'{save_directory}/{ontology_name}-elk-boxplot.png')
# show the plot
plt.show()

# create boxplot
plt.boxplot(hermit_results, labels=(["Hermit"]))
plt.title(f'{ontology_name} ontology (with {time_iterations} iterations)')
plt.xlabel('')
plt.ylabel('Time in seconds')
# save plot
plt.savefig(f'{save_directory}/{ontology_name}-hermit-boxplot.png')
# show the plot
plt.show()

# stats calc
# for elk
elk_min = np.min(elk_results)
elk_max = np.max(elk_results)
elk_mean = np.mean(elk_results)
elk_std = np.std(elk_results)

if printResults:
    print("ELK stats:")
    print(f"min: {elk_min}, max: {elk_max}, mean: {elk_mean}, std: {elk_std}")

# for Hermit
hermit_min = np.min(hermit_results)
hermit_max = np.max(hermit_results)
hermit_mean = np.mean(hermit_results)
hermit_std = np.std(hermit_results)

if printResults:
    print("Hermit stats:")
    print(f"min: {hermit_min}, max: {hermit_max}, mean: {hermit_mean}, std: {hermit_std}")

with open(f'{save_directory}/{ontology_name}-results-analysis.txt', 'w', encoding='utf-8') as file:

    file.write(f"These results are for the ontology: {ontology_path}\n")
    file.write(f"Search for subsumers of the concept: {getSubsumersOfConcept}\n")
    file.write(f"Tested on {time_iterations} iterations\n")

    file.write(f"\nELK stats:\n")
    file.write(f"min: {elk_min}, max: {elk_max}, mean: {elk_mean}, std: {elk_std}\n")
    file.write(f"\nHermit stats:\n")
    file.write(f"min: {hermit_min}, max: {hermit_max}, mean: {hermit_mean}, std: {hermit_std}\n")

    file.write(f"\n\nSAME RESULTS ROUNDED UP/DOWN\n")
    file.write(f"\nELK stats:\n")
    file.write(f"min: {np.round(elk_min, 5)}, max: {np.round(elk_max, 5)}, mean: {np.round(elk_mean, 5)}, std: {np.round(elk_std, 5)}\n")
    file.write(f"\nHermit stats:\n")
    file.write(f"min: {np.round(hermit_min, 5)}, max: {np.round(hermit_max, 5)}, mean: {np.round(hermit_mean, 5)}, std: {np.round(hermit_std, 5)}\n")

    file.write(f"\n\nRESULTS OF THE REASONERS:\n")

    file.write("\nELK subsumers result:\n")
    for concept in elk_subsumers.toArray():
        file.write(f" - {formatter.format(concept)}\n")
    file.write(f"({len(elk_subsumers)} in total)\n")

    file.write("\nHermit subsumers result:\n")
    for concept in hermit_subsumers.toArray():
        file.write(f" - {formatter.format(concept)}\n")
    file.write(f"({len(hermit_subsumers)} in total)\n")

