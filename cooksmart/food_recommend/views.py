from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import FoodMetadata, FoodAdding
from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient("vector-store")
collection = client.get_collection("NER_embed")
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Create your views here.
def home(request):
    user_infor = {"logged_in": False,
                "last_name":""}
    if request.user.is_authenticated:
        user_infor = {"logged_in": request.user.is_authenticated,
                    "last_name": request.user.last_name}
    return render(request, "home.html", context=user_infor)

def display(request):
    user_info = {"logged_in": False,
                 "last_name": ""}
    if request.user.is_authenticated:
        user_info = {"logged_in": request.user.is_authenticated,
                    "last_name": request.user.last_name}
    return render(request, "main_screen.html", context=user_info)

def String2List(paragraph: str):
    return paragraph[1:-1].split(", ")

def search(request):
    q = request.GET.get("q")
    limit = int(request.GET.get("limit"))

    q_embed = model.encode(q)
    results_embed = collection.query(
        query_embeddings=[q_embed],
        n_results=limit
    )

    dishes = FoodMetadata.objects.filter(index__in=results_embed['ids'][0])
    data = []
    for dish in dishes:
        data.append({
            "title": dish.title,
            "ingredients": String2List(dish.ingredients),
            "directions": dish.directions[1:-1]
        })
    return JsonResponse(data, safe=False)

@login_required
def add_food(request):
    if request.method == "POST":
        title = request.POST['title']
        ingredients = request.POST['ingredients']
        directions = request.POST['directions']
        ner = request.POST['ner']

        FoodAdding.objects.create(
            user=request.user,
            title=title,
            ingredients=ingredients,
            directions=directions,
            ner=ner
        )
        return redirect('adding')

    user_info = {"logged_in": False,
                 "last_name": ""}
    if request.user.is_authenticated:
        user_info = {"logged_in": request.user.is_authenticated,
                    "last_name": request.user.last_name}
    
    return render(request, 'adding.html', user_info)

@user_passes_test(lambda u: u.is_superuser)
def admin_func(request):
    """
    GET: hiển thị tất cả record trong food_adding
    POST: xử lý action 'delete' hoặc 'promote'
    """
    if request.method == "POST":
        action = request.POST.get("action")
        pk = request.POST.get("pk")  # primary key của FoodAdding
        if not pk:
            messages.error(request, "Không có bản ghi được chọn.")
            return redirect(reverse("admin_foods"))

        fa = get_object_or_404(FoodAdding, pk=pk)

        if action == "delete":
            fa.delete()
            messages.success(request, f'Đã xóa: {fa.title}')
            return redirect(reverse("admin_foods"))

        if action == "promote":
            try:
                # collection.metadata["id_counter"] += 1
                # index = collection.metadata.get("id_counter")
                index=100000
                with transaction.atomic():
                    fm = FoodMetadata.objects.create(
                        index=index,
                        title=fa.title,
                        ingredients=fa.ingredients,
                        directions=fa.directions,
                        ner=fa.ner
                    )
                    # embed = model.encode(fa.ner)
                    # collection.add(
                    #     ids=index,
                    #     embeddings=[embed],
                    #     metadatas={"title": fa.title, "NER": fa.ner},
                    #     documents=[fa.title]
                    # )
                    fa.delete()
                messages.success(request, f'Đã thêm vào metadata: {fm.title}')
            except Exception as e:
                messages.error(request, f'Lỗi khi thêm: {e}')
            return redirect(reverse("admin_food"))

        messages.error(request, "Action không hợp lệ.")
        return redirect(reverse("admin_food"))

    # GET: hiển thị tất cả record
    items = FoodAdding.objects.all()
    return render(request, "admin-food.html", {"items": items})