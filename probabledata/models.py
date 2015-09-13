from django.db import models
#so far so good. but can this count the number of persons contributing to a prediction without double counting?

#class Person(models.Model):
    #name = models.CharField(max_length=128)
    #date_created = models.DateField()
    #friends = models.ManyToManyField("self")
    #likes = models.ManyToManyField("self",symmetrical=False)
    #living location (MAKE INTO A NEW MODEL)
    #male/female
    #where live(ish)
    #password
    #number of questions and predictions completed (should I save this or render a new one every time?)
    
    #def __unicode__(self):
    #    return self.name

class Answer(models.Model):
    #name = models.IntegerField()
    name = models.CharField(max_length=128)
    #answer = models.DecimalField(decimal_places=1,max_digits=3)
    def __unicode__(self):
        return self.name
#class Answer(models.Model):
    #name = models.CharField(max_length=128)
    #date_created = models.DateField()
    #person = models.ForeignKey(Person)
    #question = models.ForeignKey(Question)
    #answer = models.DecimalField(max_digits=3) #true/false represented by +1 and -1
    #two types: query and answer
    #actual answer: in some form, not sure what yet... could it be in unicode or something? (Could be the name...)
    def __unicode__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=128)
    #date_created = models.DateField()
    #person = models.ManyToManyField(Person, through='Answer')
    #predictions = models.ManyToManyField(Prediction)
    answers = models.ManyToManyField(Answer) #temporary, until i make 'person' logins
    #the answer's data type
    #answer distributions: mean, 1st standard dev, 2nd standard dev (I KNOW we don't want to count this every time)
    #average answer age (for relevancy)
    def __unicode__(self):
        return self.name

class Prediction(models.Model):
    name = models.CharField(max_length=128)
    questions = models.ManyToManyField(Question)
    qualifiers = models.ManyToManyField(Question, related_name='qualifier')
    results = models.ManyToManyField(Question, related_name='result') #results are the specific answer that matches with each question.
    coefs = models.ManyToManyField(Question, related_name='coef') #this doesn't seem right... i just want some data stored for each question (for each prediction)...
    StDev2Above = models.CharField(max_length=128)
    StDev2Below = models.CharField(max_length=128)
    highest = models.CharField(max_length=128)
    lowest = models.CharField(max_length=128)
    average = models.CharField(max_length=128)
    #qualifyQ = models.CharField(max_length=128)
    #qualifyQ = models.ForeignKey(Question)
    #date_created = models.DateField()
    #changing factors for each question (must be stored here b/c questions might be used multiple times)
    #correlations
    #get all answers (from those who answered every question) to each question in this prediction (BIG ONE, both in importance and time)
    #question order? 
    #who has answered all questions? person = models.ManyToManyField(Person)
    #who answered what percent of which question?
    #image of current answer distribution (or just count the distribution and plot)
    #image of current query disribution (or just count the query and plot)
    #who created what?
    def __unicode__(self):
        return self.name