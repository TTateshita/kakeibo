import base64
from io import BytesIO
from wordcloud import WordCloud


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from app.models import Posts
from app.forms import PostsForm


# Create your views here.
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "GET":
        form = PostsForm()#フォームを生成
        posts = Posts.objects.all()
        wordcloud_image = _generate_wordcloud(posts)
        print(type(wordcloud_image))
        
        context = {
            "form":form,        #formをテンプレートに返す
            "posts":posts,
            "wordcloud_image": wordcloud_image,
        }                       
        return render(request, "app/index.html", context)
    
    elif request.method == "POST":
            #フォームから投稿が送信されたときの処理
        form = PostsForm(request.POST)
        if form.is_valid():
            form.save()#これだけでフォームの情報がデータベースに登録される！
            
            return redirect(index)
        #登録された投稿を一覧に反映させるため、再度アクセスさせる
        
        
def delete(request, pk):
    learn = get_object_or_404(Posts, id=pk)
    learn.delete()
    return redirect("index")


def _generate_wordcloud(posts):
    if len(posts) == 0:
        return
    skill_names = [post.skill_name for post in posts]
    text = " ".join(skill_names)
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
    ).generate(text)
    return _to_image(wordcloud)

def _to_image(wordcloud):
    # ワードクラウドを画像に変換
    image = wordcloud.to_image()
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_png = buffer.getvalue()
    buffer.close()

    # 画像データをBase64エンコードしてバイナリ型にする
    image_base64_binary = base64.b64encode(image_png)
    # UTF-8で文字列にデコードしてHTMLに埋め込める形式にする
    image_base64_string = image_base64_binary.decode("utf-8")
    return image_base64_string