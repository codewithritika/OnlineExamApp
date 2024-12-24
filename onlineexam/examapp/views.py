
from django.http import HttpResponse
from django.shortcuts import render
from examapp.models import Question,Result
from django.db import connection
from django.contrib import auth
# Create your views here.


def giveMePage1(request):
    return render(request,'examapp/questionmanagement.html')

def giveMePage2(request):
    return render(request,'examapp/resultanalysis.html')

def giveMePage3(request):
    return render(request,'examapp/admindashboard.html')



def showRemainingTime(request):

       request.session['duration'] =   request.session['duration'] - 1
       return HttpResponse(request.session['duration'])

# path('search/<pageno>',views.search),
# <a href="/examapp/search/1">1</a>
# 0 
# 1=> 0 3
# 2=> 3 6
# 3=> 6 9
def search(request,pageno):
       
    endindex=int(pageno)*3
    startindex=endindex-3

    queryset=Result.objects.filter(subject=request.session['subject'])[startindex:endindex]

    print(queryset)

    count=request.session['count']

    list=[]

    for i in range(0,count):
        list.append(i+1)

    print(list)

    return render(request,'examapp/search.html',{'results':queryset,'listofint':list})
        
    
def search1(request):

     subject=request.GET["subject"]
     request.session['subject']=subject
     noofrecords=Result.objects.filter(subject=subject).count()
     i=noofrecords
     count=0

     while i>0:
         count=count+1
         i=i-3
    
     print(f"noofrecords is {noofrecords} and noofpages is {count}")

     request.session['count']=count

     queryset=Result.objects.filter(subject=subject)[0:3]
     print(queryset)

     l=[]
     for i in range(0,count):
        l.append(i+1)
     print(l)

     return render(request,'examapp/search.html',{'results':queryset,'listofint':l})
 
 
def startTest(request):
    subjectname=request.GET['subject']
    request.session['subject']=subjectname
    queryobj=Question.objects.filter(subject=subjectname)
    questionobj=queryobj[0]
    return render(request,'examapp/question.html/',{'question':questionobj})        


def nextQuestion(request):
    dictionary=request.session['answer']
    if "op" in request.GET:
        dictionary[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        print(dictionary)
    listoflist=dictionary.values()
    sessionlist = (list(listoflist))
    request.session['sessionlist'] = sessionlist
    allquestions=Question.objects.filter(subject=request.session['subject'])
    if (request.session['qindex']<len(allquestions)-1):
        request.session['qindex']+=1
        currentques = allquestions[request.session['qindex']]
        qno = currentques.qno
        qno = str(qno)
        if(qno in dictionary):
            mylist = dictionary[qno]
            previousanswer = mylist[3]
            print(f"previous answer is {previousanswer}")
        else:
            previousanswer = ""    
        return render(request,'examapp/question.html',{'question':currentques,'previousanswer':previousanswer})
    else:
        return render(request,'examapp/question.html',{'question':allquestions[len(allquestions)-1]})   
    
def previousQuestion(request):
    dictionary=request.session['answer']
    if "op" in request.GET:
        dictionary[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        print(dictionary)
    listoflist=dictionary.values()
    sessionlist = (list(listoflist))
    request.session['sessionlist'] = sessionlist
    allquestions=Question.objects.filter(subject=request.session['subject'])
    if request.session['qindex']>0:
        request.session['qindex']=request.session['qindex']-1
        currentques = allquestions[request.session['qindex']]
        qno = currentques.qno
        qno = str(qno)
        if(qno in dictionary):
            mylist = dictionary[qno]
            previousanswer = mylist[3]
            print(f"previous answer is {previousanswer}")
        else:
            previousanswer = ""    
        return render(request,'examapp/question.html',{'question':currentques,'previousanswer':previousanswer})
    else:
        return render(request,'examapp/question.html',{'question':allquestions[0]}) 
         

def endExam(request):
    dictionary=request.session['answer']
    dictionary[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
    listoflist=dictionary.values()
    sessionlist = (list(listoflist))
    request.session['sessionlist'] = sessionlist
    for mylist in listoflist:
        if mylist[2]==mylist[3]:
            request.session['score']=request.session['score']+1
    
    finalscore=request.session['score']
    username=request.session['username']
    subject = request.session['subject']
    Result.objects.create(username=username, subject=subject, score=finalscore)
    print(connection.queries)
    # auth.logout(request)   
    return render(request,'examapp/score.html',{'username':username,'score':finalscore,'listoflist':listoflist})     

def viewResult(request):
    sessionlist = request.session['sessionlist']
    finalscore=request.session['score']
    auth.logout(request)   
    return render(request,'examapp/result.html', {'listoflist':sessionlist,'score':finalscore})

def addQuestion(request):

    Question.objects.create(qno=request.GET["qno"],subject=request.GET["subject"],answer=request.GET["answer"],qtext=request.GET["qtext"],op1=request.GET["op1"],op2=request.GET["op2"],op3=request.GET["op3"],op4=request.GET["op4"])
    
    # questionobject=Question(qno=request.GET["qno"],subject=request.GET["subject"],answer=request.GET["answer"],qtext=request.GET["qtext"],op1=request.GET["op1"],op2=request.GET["op2"],op3=request.GET["op3"],op4=request.GET["op4"])
    # questionobject.save()

    return render(request,"examapp/questionmanagement.html",{'message':'question added'})


def viewQuestion(request):
   
    question=Question.objects.get(qno=request.GET["qno"],subject=request.GET["subject"])

    print(connection.queries)

    return render(request,"examapp/questionmanagement.html",{'question':question})


def updateQuestion(request):

    question=Question.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"])

    question.update(qtext=request.GET["qtext"],answer=request.GET["answer"],op1=request.GET["op1"],op2=request.GET["op2"],op3=request.GET["op3"],op4=request.GET["op4"])
    
    print(connection.queries)

    return render(request,"examapp/questionmanagement.html",{'message':"Record Updated"})


def deleteQuestion(request):

    queryset=Question.objects.filter(qno=request.GET["qno"],subject=request.GET["subject"])
    
    queryset.delete()

    print(connection.queries)

    return render(request,"examapp/questionmanagement.html",{'message':"Record Deleted"})