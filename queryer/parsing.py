from refo import Plus, Question
from quepy.parsing import Lemma,Lemmas, Pos, QuestionTemplate, Token, Particle
from quepy.dsl import HasKeyword, IsRelatedTo, HasType
from dsl import DefinitionOf,IsCountry, IncumbentOf, CapitalOf, LabelOf, LanguageOf, PopulationOf, PresidentOf,IsBook, HasAuthor, AuthorOf, IsPerson, NameOf,IsPopulatedPlace,IsTvShow, ReleaseDateOf, StarsIn, HasShowName, NumberOfEpisodesIn, HasActor, ShowNameOf, CreatorOf

nouns1 = Pos("DT") | Pos("IN") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS")
nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class TvShow(Particle):
    regex = Plus(Question(Pos("DT")) + nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsTvShow() + HasShowName(name)

class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)

class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)

class Book(Particle):
    regex = Plus(nouns1)

    def interpret(self, match):
        name = match.words.tokens
        return IsBook() + HasKeyword(name)


class Author(Particle):
    regex = Plus(nouns1 | Lemma("."))

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)

class Thing(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |\
            Pos("VBN")

    def interpret(self, match):
        return HasKeyword(match.words.tokens)




class ReleaseDateQuestion(QuestionTemplate):
    """
    Ex: when was Friends release?
    """

    regex = Lemmas("when be") + TvShow() + Lemma("release") + \
        Question(Pos("."))

    def interpret(self, match):
        release_date = ReleaseDateOf(match.tvshow)
        return release_date, "literal"


class EpisodeCountQuestion(QuestionTemplate):
    """
    Number of episodes of Seinfeld"
    """

    regex = ((Lemmas("how many episode do") + TvShow() + Lemma("have")) |
             (Lemma("number") + Pos("IN") + Lemma("episode") +
              Pos("IN") + TvShow())) + \
            Question(Pos("."))

    def interpret(self, match):
        number_of_episodes = NumberOfEpisodesIn(match.tvshow)
        return number_of_episodes, "literal"

class WhoWroteQuestion(QuestionTemplate):
    """
        "who is the author of A Game Of Thrones?"
    """

    regex = ((Lemmas("who write") + Book()) |
             (Question(Lemmas("who be") + Pos("DT")) +
              Lemma("author") + Pos("IN") + Book())) + \
            Question(Pos("."))

    def interpret(self, match):
        author = NameOf(IsPerson() + AuthorOf(match.book))
        return author, "literal"

class CapitalOfQuestion(QuestionTemplate):
    """
     "What is the capital of Bolivia?"
    """

    opening = Lemma("what") + Token("is")
    regex = opening + Pos("DT") + Lemma("capital") + Pos("IN") + \
        Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        capital = CapitalOf(match.country)
        label = LabelOf(capital)
        return label, "enum"


class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is a blowtorch
    Ex: "What is a car"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + \
        Thing() + Question(Pos("."))

    def interpret(self, match):
        label = DefinitionOf(match.thing)

        return label, "define"
