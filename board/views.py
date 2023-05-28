from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from hitcount.models import HitCount

from accounts.models import User
from .models import Board, Category
from .forms import BoardForm
from django.core.paginator import Paginator


def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_boards, 10)
    boards = pagenator.get_page(page)
    username = None
    if request.session.get('user'):
        user_id = request.session.get('user')
        username = User.objects.get(pk=user_id)

    hit_counts = HitCount.objects.order_by('-hits')[:5]
    board_ids = [hit_count.object_pk for hit_count in hit_counts]
    popular_boards = Board.objects.filter(id__in=board_ids)

    return render(request, 'board/board_list.html', {
        "boards": boards,
        "popular_boards": popular_boards,
        'username': username
    })

@login_required
def board_write(request):
    if request.method == "POST":
        form = BoardForm(request.POST, request.FILES)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.user.id
            member = User.objects.get(pk=user_id)

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.image = form.cleaned_data['image']
            board.writer = member
            board.category = form.cleaned_data['category']
            board.recruitment_start_date = form.cleaned_data['recruitment_start_date']
            board.recruitment_end_date = form.cleaned_data['recruitment_end_date']
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()
    return render(request, 'board/board_write.html', {'form': form, 'username': request.session.get('user')})

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    #board.views += 1  # 조회수 증가
    #board.save()  # 변경된 조회수 저장

    username = None
    if request.session.get('user'):
        user_id = request.session.get('user')
        username = User.objects.get(pk=user_id)

    is_owner = False
    if board.writer == username:
        is_owner = True

    return render(request, 'board/board_detail.html', {'board':board, 'is_owner':is_owner})

def board_modify(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    if request.method == "POST":
        form = BoardForm(request.POST, request.FILES)

        if form.is_valid():
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            if 'image' in request.FILES and request.FILES['image']:
                board.image = request.FILES['image']
            board.save()
            return redirect('/board/detail/' + str(board.id))

    else:
        form = BoardForm(initial={'title': board.title, 'contents': board.contents})
        if board.image:
            form.fields['image'].initial = board.image
    context = {'form': form, 'board': board}

    return render(request, 'board/board_write.html', context)

def board_delete(request, pk):
    #if not request.session.get('user'):
    #    return redirect('/accounts/login/')
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    #if board.writer.user_id != request.session.get('user'):
    #    return redirect('/board/detail/'+str(pk))

    board.delete()
    return redirect('/board/list/')

def search_view(request):
    keyword = request.GET.get('keyword')

    results = None
    if keyword and len(keyword) >= 2:
        results = Board.objects.filter(
            Q(title__icontains=keyword) | Q(contents__icontains=keyword)
        )

    context = {
        'results': results,
        'keyword': keyword
    }

    return render(request, 'board/search.html', context)

def board_posts(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    pagenator = Paginator(all_boards, 10)
    boards = pagenator.get_page(page)
    username = None
    if request.session.get('user'):
        user_id = request.session.get('user')
        username = User.objects.get(pk=user_id)

    hit_counts = HitCount.objects.order_by('-hits')[:5]
    board_ids = [hit_count.object_pk for hit_count in hit_counts]
    popular_boards = Board.objects.filter(id__in=board_ids)

    selected_category = request.GET.get('category')
    if selected_category:
        boards = all_boards.filter(category__name=selected_category)
    else:
        boards = all_boards

    # Paginate the filtered boards
    pagenator = Paginator(boards, 10)
    boards_page = pagenator.get_page(page)

    # Get category list
    category_list = Category.objects.all()

    return render(request, 'board/board_post.html', {
        "boards": boards,
        "popular_boards": popular_boards,
        "category_list": category_list,
        "selected_category": selected_category,
        'username': username
    })


def like_post(request, board_id):
    board = Board.objects.get(pk=board_id)
    user = request.user
    if user in board.likes.all():
        board.likes.remove(user)
    else:
        board.likes.add(user)
    return redirect('/board/detail/' + str(board.id), board_id=board_id)
