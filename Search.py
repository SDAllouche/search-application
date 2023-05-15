import urllib3
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF

# define the end point
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

autors = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:  <http://purl.org/dc/elements/1.1/>

Select distinct ?birthdate ?thumbnail ?author ?name ?description  WHERE {
?author rdf:type dbo:Writer ;
        dbo:birthDate ?birthdate ;
        rdfs:label ?name ;
        rdfs:comment ?description 
 FILTER ((lang(?name)="en")&&(lang(?description)="en")&&(STRLEN(STR(?birthdate))>6)&&(SUBSTR(STR(?birthdate),6)=SUBSTR(STR(bif:curdate('')),6))) .
 OPTIONAL { ?author dbo:thumbnail ?thumbnail . }
} ORDER BY ?birthdate"""

celebrities = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:  <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?name ?birthdate ?description WHERE {
  ?person rdf:type dbo:Person ;
          dbo:occupation ?occupation ;
          dbo:birthDate ?birthdate ;
          rdfs:label ?name ;
          rdfs:comment ?description .
  FILTER ((lang(?name)="en")&&(lang(?description)="en")&&
          (STRLEN(STR(?birthdate))>6)&&
          (SUBSTR(STR(?birthdate),6)=SUBSTR(STR(bif:curdate('')),6))&&
          (REGEX(?occupation, "celebrity", "i")))
} ORDER BY ?birthdate"""

costume_date = """PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?person ?name ?birthdate ?thumbnail
WHERE {{
    ?person rdf:type dbo:Person .
    ?person dbo:birthDate ?birthdate .
    ?person foaf:name ?name .
    OPTIONAL {{ ?person dbo:thumbnail ?thumbnail . }}
    FILTER (
        MONTH(?birthdate) = 5 &&
        DAY(?birthdate) = 12 &&
        YEAR(?birthdate) = 1990 &&
        lang(?name) = "en"
    )
}}
ORDER BY ?birthdate
LIMIT 100"""

natioanlity = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:  <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT DISTINCT ?name ?birthdate ?description ?nationality WHERE {
  ?person rdf:type dbo:Person ;
          dbo:occupation ?occupation ;
          dbo:birthDate ?birthdate ;
          rdfs:label ?name ;
          rdfs:comment ?description ;
          dct:subject ?subject .
  ?subject a dbo:Nationality ;
           rdfs:label "American"@en .
  OPTIONAL {?person dbo:nationality ?nationality}
  FILTER ((lang(?name)="en")&&(lang(?description)="en")&&
          (STRLEN(STR(?birthdate))>6)&&
          (SUBSTR(STR(?birthdate),6)=SUBSTR(STR(bif:curdate('')),6))&&
          (REGEX(?occupation, "celebrity", "i")))
} ORDER BY ?birthdate"""

sparql.setQuery(autors)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Create HTML output
html = '<html><head><title>Literary Birthdays of Today</title></head>'

# extract Weekday %A / Month %B / Day of the Month %d by formatting today's date accordingly
datum = datetime.today().strftime("%A  %B %d")
html += '<body><h1>Literary Birthdays of {}</h1>'.format(datum)

html += '<ul>'

for result in results["results"]["bindings"]:
    if ("author" in result):
        # Create Wikipedia Link
        wikiurl = "http://en.wikipedia.org/wiki/" + \
            result["author"]["value"].split('/')[-1]
    else:
        wikiurl = 'NONE'
    if ("name" in result):
        name = result["name"]["value"]
    else:
        name = 'NONE'
    if ("birthdate" in result):
        date = result["birthdate"]["value"]
    else:
        date = 'NONE'
    if ("description" in result):
        description = result["description"]["value"]
    else:
        description = ' '
    if ("thumbnail" in result):
        pic = result["thumbnail"]["value"]
    else:
        pic = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Question_mark2.svg/71px-Question_mark2.svg.png'

    # parse date as datetime
    dt = datetime.strptime(date, '%Y-%m-%d')
    html += '<li><b>{}</b> -- <img src="{}" height="60px"> <a href="{}">{}</a>, {} </li>'.format(
        dt.year, pic.replace("300", "60"), wikiurl, name, description)

html += '</ul>'
html += '</body></html>'

# Save HTML file
with open('Result.html', 'w', encoding='utf-8') as f:
    f.write(html)


# print(results.toxml())
