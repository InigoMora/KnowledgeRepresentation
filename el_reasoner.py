#! /usr/bin/python

import sys
from py4j.java_gateway import JavaGateway
import random

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


































"""
EL-Completion Rules

⊤-rule: Add ⊤ to any individual.
⊓-rule 1: If d has C ⊓D assigned, assign also C and D to d. 
⊓-rule 2: If d has C and D assigned, assign also C ⊓D to d.
∃-rule 1: If d has ∃r.C assigned:
    1. If there is an element e with initial concept C assigned, make e the r-successor of d.
    2. Otherwise, add a new r-successor to d, and assign to it as initial concept C.
∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
⊑-rule: If d has C assigned and C ⊑ D ∈ T , then also assign D to d
"""

"""
EL-Completion Algorithm

1. Start with initial element d0, assign to C0 to it as initial concept 2. Set changed := true
3. While changed = true :
    3.1 Set changed := false
    3.2 For every element d in the current interpretation:
        3.2.1 Apply all the rules on d in all possible ways so that only concepts from the input get assigned
        3.2.2 If a new element was added or a new concept assigned, set changed = true
4. If D0 was assigned to d0, return YES, otherwise return NO
"""



















#Build Completion Algorithm

"""
EL Algorithm

1. Start with initial element d0, assign to C0 to it as initial concept 2. Set changed := true
3. While changed = true :
    3.1 Set changed := false
    3.2 For every element d in the current interpretation:
        3.2.1 Apply all the rules on d in all possible ways so that only concepts from the input get assigned
            ⊤-rule: Add ⊤ to any individual.
            ⊓-rule 1: If d has C ⊓D assigned, assign also C and D to d. 
            ⊓-rule 2: If d has C and D assigned, assign also C ⊓D to d.
            ∃-rule 1: If d has ∃r.C assigned:
                1. If there is an element e with initial concept C assigned, make e the r-successor of d.
                2. Otherwise, add a new r-successor to d, and assign to it as initial concept C.
            ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
            ⊑-rule: If d has C assigned and C ⊑ D ∈ T , then also assign D to d
        3.2.2 If a new element was added or a new concept assigned, set changed = true
4. If D0 was assigned to d0, return YES, otherwise return NO
"""



#tbox, from tbox = ontology.tbox() --> object, the box itself, contains axioms
#axioms, from axioms = tbox.getAxioms() --> list of all axioms in the tbox (axioms themselves)
#allConcempts, from allConcepts = ontology.getSubConcepts() --> all concepts in the ontology, including definitions, e.g. (∃contains.AnimalProduct ⊔ ∃contains.Meats) as a concept, and KewpieMayo and ∃contains.KewpieMayo
#conceptNames, from conceptNames = ontology.getConceptNames() --> all the defined concept names. e.g. KewpieMayo, (but NOT ∃contains.KewpieMayo)


#Finding axiom type --> for axiom in axioms:, axiomType = axiom.getClass().getSimpleName(), e.g. axiomType == "GeneralConceptInclusion"
#Finding concepts --> for concept in allConcepts:, conceptType = concept.getClass().getSimpleName(), e.g. ConceptName, -or- e.g. ConceptConjunction



# Creating EL concepts and axioms

elFactory = gateway.getELFactory()

conceptA = elFactory.getConceptName("A")
conceptB = elFactory.getConceptName("B")
conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
role = elFactory.getRole("r")
existential = elFactory.getExistentialRoleRestriction(role,conjunctionAB)
top = elFactory.getTop()
conjunction2 = elFactory.getConjunction(top,existential)

gci = elFactory.getGCI(conjunctionAB,conjunction2)

"""
print(conceptA)
print(conjunctionAB)
print(existential)
print(gci)
print(top)



print("I made the following GCI:")
print(formatter.format(gci))

"""


#New tBox, for use with elFactory
Tbox = []   #Not in use ****
Axioms = [] #Not in use *****
GCI = []
Concepts = []
ConceptNames = []
ConceptTop = []
ExistentialRoleRestrictions = []    #List of lists, [[role, conceptname]]

for axiom in axioms:
    axiomType = axiom.getClass().getSimpleName()
    if(axiomType == "GeneralConceptInclusion"):
        print("I found a general concept inclusion:")
        print(formatter.format(axiom))
        gci_temp=elFactory.getGCI(axiom.lhs(),axiom.rhs())
        GCI.append(gci_temp)
        print(gci_temp)
        #****handle******
    elif(axiomType == "EquivalenceAxiom"):
        concepts_temp = axiom.getConcepts()    #handle***** # If the TBox contains equivalence axioms C ≡ D, replace each such axiom by the two axioms C ⊑ D and D ⊑ C
        #append C ⊑ D
        gci_temp=elFactory.getGCI(concepts_temp[0],concepts_temp[1])
        GCI.append(gci_temp)
        #append D ⊑ C
        gci_temp=elFactory.getGCI(concepts_temp[1],concepts_temp[0])
        GCI.append(gci_temp)

#Handle TOP ******** all concepts should be allConcepts ⊑ TOP ***** get them all and iterate throgh them all******* *****maybe after done with everything*******

for concept in allConcepts:
  conceptType = concept.getClass().getSimpleName()
  if(conceptType == "ConceptName"):
    #Handle*******
    ConceptNames.append(elFactory.getConceptName(formatter.format(concept)))  #****replace A with concept
    
    #Check how to handle top (and if we need to), the previous top ⊤ and elFactory TOP are different, maybe if top concept found, add TOP (from elFactory)
    """
  elif(conceptType == "TopConcept$"):
    print("TOP CONCEWPOT WAS FOUND: !!!!!", formatter.format(concept) )
    ConceptTop.append(elFactory.getConceptName(formatter.format(concept)))
    #Handle*******
    print("I found the top concept: "+formatter.format(concept))
    print()
    """
  elif(conceptType == "ExistentialRoleRestriction"):
    #Handle*******
    print("I found an existential role restriction:"+formatter.format(concept))
    print("The role is: "+formatter.format(concept.role()))
    print("The filler is: "+formatter.format(concept.filler()))
    print()
  elif(conceptType == "ConceptConjunction"):
    #Handle*******
    #print("I found a conjunction: "+formatter.format(concept))
    #print("The conjuncts are: ")
    for conjunct in concept.getConjuncts():
      print(" - "+formatter.format(conjunct))
    print()




"""
# access the type of axioms:
foundGCI = False
foundEquivalenceAxiom = False
print()
print("Looking for axiom types in EL")
for axiom in axioms:
  axiomType = axiom.getClass().getSimpleName()
  #print(axiomType)
  if(not(foundGCI)
    and axiomType == "GeneralConceptInclusion"):
    print("I found a general concept inclusion:")
    print(formatter.format(axiom))
    print("The left hand side of the axiom is: ", formatter.format(axiom.lhs()))
    print("The right hand side of the axiom is: ", formatter.format(axiom.rhs()))
    print()
    foundGCI = True

  elif(not(foundEquivalenceAxiom) and axiomType == "EquivalenceAxiom"):
    print("I found an equivalence axiom:")
    print(formatter.format(axiom))
    print("The concepts made equivalent are: ")
    for concept in axiom.getConcepts():
      print(" - "+formatter.format(concept))
    print()
    foundEquivalenceAxiom = True

# accessing the relevant types of concepts:
foundConceptName=False
foundTop=False
foundExistential=False
foundConjunction=False
foundConceptTypes = set()

print()
print("Looking for concept types in EL")
for concept in allConcepts:
  conceptType = concept.getClass().getSimpleName()
  if(not(conceptType in foundConceptTypes)):
    print(conceptType)
    foundConceptTypes.add(conceptType)
  if(not(foundConceptName) and conceptType == "ConceptName"):
    print("I found a concept name: "+formatter.format(concept))
    print()
    foundConceptName = True
  elif(not(foundTop) and conceptType == "TopConcept$"):
    print("I found the top concept: "+formatter.format(concept))
    print()
    foundTop = True
  elif(not(foundExistential) and conceptType == "ExistentialRoleRestriction"):
    print("I found an existential role restriction:"+formatter.format(concept))
    print("The role is: "+formatter.format(concept.role()))
    print("The filler is: "+formatter.format(concept.filler()))
    print()
    foundExistential = True
  elif(not(foundConjunction) and conceptType == "ConceptConjunction"):
    print("I found a conjunction: "+formatter.format(concept))
    print("The conjuncts are: ")
    for conjunct in concept.getConjuncts():
      print(" - "+formatter.format(conjunct))
    print()
    foundConjunction=True


"""






elementDic = {} # Abox
changed = True
elementIDcounter = 0


def get_unique_id():
    global elementIDcounter
    id = elementIDcounter
    elementIDcounter += 1
    return id

# element[0] = assigned concepts
# element[1] = assigned concepts conjuctions
# element[2] = assigned relations
def create_element():
    return get_unique_id(), [[elFactory.getTop()],[],[]]

def create_initial_element():
    element_initial_id, element_initial = create_element()
    element_initial[0].append(elFactory.getConceptName(class_name))
    return element_initial_id, element_initial

#NOTE: All, the algorith makes all conjunctions binary (Only two, left and right)

#Create fist element
element_initial_id, element_initial = create_initial_element()  # Creates an element with concept class_name
elementDic[element_initial_id] = element_initial

while changed == True : # If a change was made, rerun the rules
    changed = False
    for element in elementDic:
        # Apply every rule to the element ***
        # If a rule is applied (makes a change), note as changed = True ******

        #⊤-rule: Add ⊤ to any individual.
        # When individuals are created, ⊤ is included

        #⊓-rule 1: If d has C⊓D assigned, assign also C and D to d. 
        #Check for all concept assigned to element, find C⊓D and 
        #If find something, check for conjuction in tbox
        #conceptNames = ontology.getConceptNames()
        #If it is conjuction then apply it
        #e.g. if C⊓D, add C and D
        # if C and D, check if C⊓D is in tbox, if it is, apply C⊓D
        for conjunction in elementDic[element][1]:
            break #******if the individual elements not in [element][0] add them

        #⊓-rule 2: If d has C and D assigned, assign also C ⊓D to d.    #***If in tbox****
        for concept in elementDic[element][0]:
            for other_concept in elementDic[element][0]:
                if concept != other_concept:
                    if not(elFactory.getConjunction(concept, other_concept) in elementDic[element][1]) and not(elFactory.getConjunction(other_concept, concept) in elementDic[element][1]): #If (A n B) and (B n A) are not in element[0] (the list of concepts for this element)
                        concept_conjunction = elFactory.getConjunction(concept, other_concept)
                        if concept_conjunction in axioms:
                            print("FOUND")
                            #IF IN TTHE TBOX**************
                            elementDic[element][1].append(concept_conjunction)
                            changed = True




        #∃-rule 1: If d has ∃r.C assigned:
            #1. If there is an element e with initial concept C assigned, make e the r-successor of d.
            #2. Otherwise, add a new r-successor to d, and assign to it asinitial concept C.
        #∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
        #⊑-rule: If d has C assigned and C ⊑ D ∈ T , then also assign D to d


        #at some point I have to check the axioms (tbox) to add subsumers, inclusion, etc ***(?)*****
        for axiom in axioms:
            axiom_type = axiom.getClass().getSimpleName()
            #print(axiom)
            #print(axiom_type)
            if axiom_type == 'GeneralConceptInclusion':
                # ⊑ ∃contains. is also GeneralConceptInclusion

                break
                # DO this
                #changed = True




















# what we have to do:
def get_subsumers(concept_name):
    return [1, 2, 3]









subsumers = get_subsumers(class_name)

# should only print "1 class name per line, no other output"
for concept in subsumers:
    # print(formatter.format(concept))
    print(concept)
