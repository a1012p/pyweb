from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    return render(request,'pybo/index.html')

def profile(request):
    return render(request,'pybo/profile.html')

def board(request):
    #질문 목록
    #127.0.0.1:8000/pybo/?page=1
    page = request.GET.get('page','1')
    so = request.GET.get('so','recent')
    kw = request.GET.get('kw','')
    lc = request.GET.get('lc','10')
    qa = request.GET.get('qa','')


    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter','-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer','-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')  # '-'기호는 내림차순

    if qa =='que':
        # 유저가 작성한 글만 가져오기 구현못함
        question_list = question_list.filter(
            Q(author__id__icontains=kw)
        ).distinct()
    elif qa == 'as':
        question_list = question_list.filter(
            Q(answer__author__id__icontains=kw)
        ).distinct()
    else:
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw) |
                Q(answer__content__icontains=kw)
            ).distinct()

    paginator = Paginator(question_list,int(lc))
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj , 'page' : page , 'kw': kw ,'so': so , 'lc': lc}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    question.views += 1;
    question.save()
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

