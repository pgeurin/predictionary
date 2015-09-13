# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404
from probabledata.models import Prediction, Question, Answer
#from django.utils import timezone
from django.db import models
import numpy as np
import scipy as sp
from scipy.stats.stats import pearsonr
import time
from django.core.urlresolvers import reverse

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            predictions = Prediction.objects.filter(name__icontains=q)
            return render_to_response('prediction/search_results.html',
                {'predictions': predictions, 'query': q})
    return render_to_response('prediction/search_results.html',{'errors': errors})

def newQuiz(request):
    #return HttpResponse(request.POST.getlist('q')[1])
    errors = []
    if 'title' in request.POST:
        title = request.POST['title']
        if not title:
            errors.append('You still need a title! This is how others will see your prediction.')
        else:
            if len(title) > 50:
                errors.append('Sorry, no more than 50 characters')
            #if title[-1] != '?':
            #    errors.append("Your question title must end with a question mark. (It's a look thing)")
    
    if 'result' in request.POST:
        result = request.POST['result']
        if not result:
            errors.append('Enter a result-question.')#DON'T YOU DARE PUBLISH THIS WITHOUT CHANGING
        else:
            if len(result) > 50:
                errors.append('Please enter at most 50 characters.') #I can edit this change in the form itself
            #if result[-1] != '?':
            #    errors.append("Your question '" + str(result) + "' must end with a question mark. (It's just a look thing)")
    
    if 'q' in request.POST:
        questionlist = request.POST.getlist('q')
        for q in questionlist:
            if not q:
                errors.append('Enter question.')
            else:
                if len(q) > 50:
                    errors.append('Please enter at most 50 characters.')
                #if q[-1] != '?':
                #    errors.append("Your question '" + str(q) +"' must end with a question mark. (It's just a look thing)")
    if errors!=[]:
        return render_to_response('prediction/create.html', {'errors': errors}, context_instance=RequestContext(request))
    p=Prediction(name=request.POST['title'])
    questionlist=request.POST.getlist('q')
    p.save()
    result=Question(name=request.POST['result'])
    result.save()
    p.results.add(result.id)
    for num in range(0,len(questionlist)):
        q=Question(name=questionlist[num])
        q.save(force_insert=True)
        p.questions.add(q.id)
        #add a coef for each question
        c=Question(name=0)
        c.save(force_insert=True)
        p.coefs.add(c.id)
    #add one more for the constant
    c=Question(name=0)
    c.save(force_insert=True)
    p.coefs.add(c.id)
    p.save()
    #return HttpResponse(str(request.POST['names']) + " " + str(request.POST['q1']) + " " + str(request.POST['q2']) ) #redirect to the actual quiz once created... or maybe a 'congradulations' site with forwarding address.
    return HttpResponseRedirect('/' + str(p.id) + '/') #redirect to the actual quiz once created... or maybe a cragradulations site with forwarding address.
    
    
def vote(request, prediction_id):
    errors = []
    if 'result' in request.POST:
        result = request.POST['result']
        if not result:
            errors.append('Enter a result-question.')#DON'T YOU DARE PUBLISH THIS WITHOUT CHANGING
        else:
            if not is_number(result):
                errors.append('Must be a number.')
            if len(result) > 50:
                errors.append('Please enter at most 50 characters.') #I can edit this change in the form itself

    if 'answer' in request.POST:
        answerlist = request.POST.getlist('answer')
        for answer in answerlist:
            if not answer:
                errors.append('Enter answer.')
            else:
                if not is_number(answer):
                    errors.append('All answers must be numbers.')
                if len(answer) > 50:
                    errors.append('Please enter at most 50 characters.')
                    
    p = get_object_or_404(Prediction, pk=prediction_id)
    if errors!=[]:
        #return render_to_response('prediction/takequiz.html', {'errors': errors, 'prediction':prediction}, context_instance=RequestContext(request))
        #return render_to_response('prediction/takequiz.html', {'errors': errors, 'pk':prediction_id}, context_instance=RequestContext(request))
        #return render_to_response('prediction/takequiz.html', {'errors': errors, 'prediction_id':prediction_id}, context_instance=RequestContext(request))
        #t = loader.get_template('prediction/takequiz.html')
        #c = Context({'errors': errors})
        #return HttpResponse(t.render(c))
        #return HttpResponseRedirect('/' + str(p.id) + '/')#HOW DO I INCLUDE ERRORS HERE?!
        #HttpResponseRedirect(reverse('prediction.views.vote', args=(p.id,)))
        return render_to_response('prediction/takequiz.html', {
            'prediction': p,
            'errors': errors
        }, context_instance=RequestContext(request))
    questions=p.questions.all()
    results=p.results.all()
    for r in results:
        a=Answer(name=request.POST['result'])
        a.save(force_insert=True)
        r.answers.add(a.id)
    
    
    #for num in range(0,len(answers)):
    #    answer=Answer(name=answers[num])
    #    answer.save(force_insert=True)
    #    q.questions.add(a.id)
        
    answers=request.POST.getlist('answer')
    i=-1
    for q in questions:
        i=i+1
        a=Answer(name=answers[i])
        #a=Answer(name=request.POST['answer' + str(i)])
        a.save(force_insert=True)
        q.answers.add(a.id)
    q.save()
    
    #return HttpResponse(str(request.POST['answer'+str(1)]) + " " + request.POST['answer'+str(2)] + " " + request.POST['answer'+str(3)]) #p.objects.filter(name__icontains="now").get() #p.name
    #return HttpResponse(p.questions.all()[2].answers.all())
    return HttpResponseRedirect('/' + str(p.id) + '/votecomplete/')

def results(request, prediction_id): 
    p = get_object_or_404(Prediction, pk=prediction_id)
    questions = p.questions.all()
    results = p.results.all()
    #return HttpResponse(str(len(list(p.questions.all()))) + ' ' + str(len(p.questions.all()[0].answers.all())))
    #return HttpResponse(questions)
    #return HttpResponse(questions[0].answers.get())
    html1=''
    #len(list(questions[0].answers.all()))
    #len(list(questions))
    numA=questions[0].answers.count()
    numQ=questions.count()
    A=sp.ones((numA,numQ+1))#287 => num of questions, 10 => num of datapoints
    y=sp.ones((numA,1)) #287 => num of 
    t0=time.clock()
#load all answers to the one result
    i1=-1
    for result in results:
        i1=i1+1
        for answer in result.answers.all():
            y[i1]=answer.name
#load all answers to all questions
    i1=-1
    for question in questions:
        i1=i1+1
        i2=-1
        for answer in question.answers.all():
            i2=i2+1
            html1=html1+ str(answer.name) + ' '
            A[i2][i1]=answer.name
    timeToImport=time.clock() - t0
    #return HttpResponse(str(A))
#do the math
    (coeffs, residuals, rank, sing_vals) = np.linalg.lstsq(A, y)
    i1=-1
#load all coefficients
    for coef in p.coefs.all():
        i1=i1+1
        coef.name=coeffs[i1]
        coef.save()
    r2 = 1 - residuals / (y.size * y.var())
    http='coeffs = ' + str(coeffs) + '<br/>'
    http=http + ' last values = ' + str(A[i2]) + '<br/>'
    http=http + ' prediction =' + str( sp.dot(A[i2],coeffs)) + '<br/>'
    http=http + ' actual value =' + str(y[0]) + '<br/>'
    http=http + ' residuals =' + str(residuals) + '<br/>'
    http=http + ' R^2 =' + str(r2) + '<br/>'
    http=http + ' A =' + str(A) + '<br/>'
    http=http + ' y =' + str(y) + '<br/>'
    #return HttpResponse(http)
    
    #this is where I save all the useful stuff before redirecting, isn't it? 
    return HttpResponseRedirect('/' + str(p.id) + '/results/')

    #return HttpResponse(timeToImport)
    #return HttpResponse(A)
    #return HttpResponse(str(numA) + ' ' + str(numQ) + ' ' + str(i1) + ' ' + str(i2))
    #return HttpResponse(html1)
    #return HttpResponse(list(questions))
    #return HttpResponse(str(list(p.questions.all())) + ' ' + str(p.questions.all()[0].answers.all()))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False