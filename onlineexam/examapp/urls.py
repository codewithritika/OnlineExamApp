from django.urls import path

from examapp import views

urlpatterns = [
    path('startTest/',views.startTest),
    path('nextQuestion/',views.nextQuestion),   
    path('previousQuestion/',views.previousQuestion),   
    path('endExam/',views.endExam),
    path("giveMePage1",views.giveMePage1),
    path("giveMePage2",views.giveMePage2),
    path("giveMePage3",views.giveMePage3),
    path('showRemainingTime/',views.showRemainingTime),
    path('search/<pageno>/',views.search),
    path('search1/',views.search1),
    path('viewResult/',views.viewResult),
    path('addQuestion/',views.addQuestion),
    path('viewQuestion/',views.viewQuestion),
    path('updateQuestion/',views.updateQuestion),
    path('deleteQuestion/',views.deleteQuestion),
    
]
