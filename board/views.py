from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from hitcount.models import HitCount

from accounts.models import User
from .models import Board, Category, Comment, Portfolio
from .forms import BoardForm, CommentForm, PortfolioPostForm
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

    popular_boards = Board.objects.order_by('-views')[:5]

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
            board.pw = form.cleaned_data['pw']
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()
    return render(request, 'board/board_write.html', {'form': form, 'username': request.session.get('user')})

def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = Comment.objects.filter(board=board)
    comment_edit_id = None
    comment_edit_form = None
    form = CommentForm()  # Initialize the form variable

    board.views += 1
    board.save()

    if request.method == 'POST':
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('delete_comment')
            comment = Comment.objects.get(id=comment_id)
            if comment.author == request.user:
                comment.delete()
        elif 'edit_comment' in request.POST:
            comment_id = request.POST.get('edit_comment')
            comment = Comment.objects.get(id=comment_id)
            if comment.author == request.user:
                comment_edit_id = comment.id
                comment_edit_form = CommentForm(instance=comment)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.board = board
                comment.author = request.user
                comment.save()
                return redirect('board_detail', pk=pk)

    return render(request, 'board/board_detail.html', {'board': board, 'form': form, 'comments': comments, 'comment_edit_id': comment_edit_id, 'comment_edit_form': comment_edit_form})


def comment_edit(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('board_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'board/board_detail.html', {'form': form, 'comment': comment})

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

    board_results = None
    if keyword and len(keyword) >= 2:
        board_results = Board.objects.filter(
            Q(title__icontains=keyword) | Q(contents__icontains=keyword)
        )

    portfolio_results = None
    if keyword and len(keyword) >= 2:
        portfolio_results = Portfolio.objects.filter(
            Q(p_title__icontains=keyword) | Q(p_content__icontains=keyword)
        )

    context = {
        'board_results': board_results,
        'portfolio_results': portfolio_results,
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

    popular_boards = Board.objects.order_by('-views')[:5]

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


def create_portfolio_post(request):
    if request.method == 'POST':
        form = PortfolioPostForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.writer = request.user
            image = form.cleaned_data['image']
            if image:
                portfolio.image = image
            form.save()
            return redirect('portfolio_list')  # 리스트 페이지로 리디렉션
    else:
        form = PortfolioPostForm()
    context = {
        'form': form
    }
    return render(request, 'board/portfolio_write.html', context)


def portfolio_list(request):
    portfolio_list = Portfolio.objects.all()
    return render(request, 'board/portfolio_list.html', {'portfolios': portfolio_list})

def portfolio_detail(request,portfolio_id):
    portfolio_detail = Portfolio.objects.filter(id=portfolio_id)
    return render(request, 'board/portfolio_detail.html', {'portfolio': portfolio_detail})

def update_portfolio_post(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.method == 'POST':
        form = PortfolioPostForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            portfolio = form.save()
            return redirect('portfolio_detail', portfolio_id=portfolio.id)
    else:
        form = PortfolioPostForm(instance=portfolio)
    context = {
        'form': form,
        'portfolio_id': portfolio_id
    }
    return render(request, 'board/portfolio_write.html', context)


def delete_portfolio_post(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if request.method == 'POST':
        portfolio.delete()
        return redirect('portfolio_list')
    context = {
        'portfolio': portfolio
    }
    return render(request, 'board/portfolio_list.html', context)