from nltk.corpus import wordnet as wn
"""Wordnet is an NLTK corpus reader, a lexical database for English. It can be used to find the meaning of words, 
synonym or antonym. One can define it as a semantically oriented dictionary of English."""
syns = wn.synsets("dog")
print(syns)
print(wn.synsets('dog', pos=wn.VERB))  #chase: kovalamak
print(wn.synset('dog.n.01').definition(), "\n")

print(len(wn.synset('dog.n.01').examples()))    #1
print(wn.synset('dog.n.01').examples()[0], "\n")      #the dog barked all night

print("lemmas: ", wn.synset('dog.n.01').lemmas() ) #[Lemma('dog.n.01.dog'), Lemma('dog.n.01.domestic_dog'), Lemma('dog.n.01.Canis_familiaris')]
[str(lemma.name()) for lemma in wn.synset('dog.n.01').lemmas()] #['dog', 'domestic_dog', 'Canis_familiaris']
print(wn.lemma('dog.n.01.dog').synset(), "\n")  #Synset('dog.n.01')

"""For example, pigeon, crow, eagle and seagull are all hyponyms of bird (their hypernym); which, in turn, is a hyponym of animal.[3]"""
dog = wn.synset('dog.n.01')
print("hypernyms : ", dog.hypernyms())  #[Synset('canine.n.02'), Synset('domestic_animal.n.01')]
print("hyponyms: ", dog.hyponyms() ) # doctest: +ELLIPSIS [Synset('basenji.n.01'), Synset('corgi.n.01'), Synset('cur.n.01'), Synset('dalmatian.n.02'), ...]
print("member_holonyms: ", dog.member_holonyms()) # [Synset('canis.n.01'), Synset('pack.n.06')]
print("root_hypernyms: ", dog.root_hypernyms()) #[Synset('entity.n.01')]
print("lowest_common_hypernyms cat/dog: ", wn.synset('dog.n.01').lowest_common_hypernyms(wn.synset('cat.n.01')))    #[Synset('carnivore.n.01')]


print("\n---------------------Zıtlık Derecesi------------------")
good = wn.synset('good.a.01')
# print(good.antonyms()) # Böyle bişi yok!
print(good.lemmas()[0].antonyms())
print(good.lemmas()[0].pertainyms())
print(good.lemmas()[0].derivationally_related_forms())

"""
* synset1.path_similarity(synset2): Return a score denoting how similar two word senses are, based on the shortest path 
that connects the senses in the is-a (hypernym/hypnoym) taxonomy. 
* (hipernym / hipnoym) taksonomisindeki duyuları
birleştiren en kısa yola dayalı olarak, iki kelime duyusunun ne kadar benzer olduğunu gösteren bir puan döndürür.
* The score is in the range 0 to 1. (1 kendisi demek :)
 """
dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')
hit = wn.synset('hit.v.01')
slap = wn.synset('slap.v.01')
print("\ndog and cat similarty: ", wn.path_similarity(dog, cat))
print("dog and cat similarty: ", dog.path_similarity(cat))


print()
print("\n---------------------synonyms / antonyms------------------")
synonyms = []
antonyms = []
for syn in wn.synsets("active"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
             antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))