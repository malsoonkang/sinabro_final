from django.contrib.auth.hashers import check_password

from django import forms
from django.core.validators import RegexValidator

from .models import Board, Category, Comment, Portfolio
from ckeditor.widgets import CKEditorWidget

class BoardForm(forms.Form):
    # 입력받을 값 두개
    title = forms.CharField(error_messages={
        'required': '제목을 입력하세요.'
    }, max_length=100, label="게시글 제목")
    contents = forms.CharField(error_messages={
        'required': '내용을 입력하세요.'
    }, widget=forms.Textarea, label="게시글 내용")
    image = forms.ImageField(label='이미지 파일',required=False, error_messages={
        'required': '이미지를 첨부해주세요.'
    })
    pw = forms.CharField(
        min_length=4,
        max_length=4,
        label='채팅방 비밀번호 설정 (4자리 숫자)',
        error_messages={'required': '4자리 숫자를 입력해주세요.'},
        validators=[RegexValidator(r'^[0-9]{4}$', '숫자만 입력해주세요.')]
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    recruitment_start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="모집 시작일")
    recruitment_end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="모집 마감일")

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('recruitment_start_date')
        end_date = cleaned_data.get('recruitment_end_date')

        if start_date and end_date and end_date < start_date:
            self.add_error('recruitment_end_date', '모집 마감일은 모집 시작일보다 빠를 수 없습니다.')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class PortfolioPostForm(forms.ModelForm):
    p_title = forms.CharField(label='제목')
    p_content = forms.CharField(widget=CKEditorWidget(),label='')
    image = forms.ImageField(label='포트폴리오 대표 이미지를 골라주세요.', required=False, error_messages={
        'required': '이미지를 첨부해주세요.'
    })
    def clean(self):
        cleaned_data = super().clean()
    class Meta:
        model = Portfolio
        fields = ('p_title', 'p_content', 'image')
        exclude = ['published_date']