# About
Quepy is a python framework to transform natural language questions to queries in a database query language. Quepy supports SPARQL and MQL. It was used to customize different kinds of questions in natural language and database queries.
Example: Who is Elon Musk?
This transformation is done using special form of regular expressions:
```
person_name = Group(Plus(Pos("NNP")), "person_name")
regex = Lemma("who") + Lemma("be") + person_name + Question(Pos("."))
```
then using a way to express semantic relations:
```
person = IsPerson() + HasKeyword(person_name)
definition = DefinitionOf(person)
```
Then rest of the transformation is handled automatically by the framework to produce following sparql:
```
	SELECT DISTINCT ?x1 WHERE {
	    	?x0 rdf:type foaf:Person.
	    	?x0 rdfs:label "Elon Musk"@en.
	    	?x0 rdfs:comment ?x1.
	}
```

# Executing
You have to have installed the following libraries:
quepy, refo, nltk.
```
  pip install quepy refo
```
## Example Usage
```
  python main.py "What is the capital of Nepal?"
```
# About the authors
This program is written by Sangam Sharma and Sajeet Pokharel as a Mini Project for Speech and Natural Language Processing course at Kathmandu University taught my Dr. Bal Krisna Bal.
