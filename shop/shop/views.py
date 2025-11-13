from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, CartItem, Feedback
from .forms import AddToCartForm
import numpy as np

from cy_recommender import cosine_similarity_matrix

RECOMMENDER_STATE = {"item_index": None, "item_vectors": None, "similarity": None}

def build_dummy_model():
    products = list(Product.objects.all()[:200])
    if not products:
        return
    ids = [p.id for p in products]
    feats = []
    prices = np.array([float(p.price) for p in products], dtype=np.float64)
    if prices.ptp() == 0:
        prices_norm = np.ones_like(prices)
    else:
        prices_norm = (prices - prices.min()) / (prices.ptp())
    for i, p in enumerate(products):
        cat_val = float(hash(p.category) % 100) / 100.0 if p.category else 0.0
        title_len = len(p.title)
        feats.append([prices_norm[i], cat_val, float(title_len) / 100.0])
    mat = np.array(feats, dtype=np.float64)
    sim = cosine_similarity_matrix(mat)
    RECOMMENDER_STATE["item_index"] = ids
    RECOMMENDER_STATE["item_vectors"] = mat
    RECOMMENDER_STATE["similarity"] = sim

def recommend_for_user(user, top_k=6):
    if RECOMMENDER_STATE["similarity"] is None:
        build_dummy_model()
    ids = RECOMMENDER_STATE["item_index"]
    if ids is None:
        return Product.objects.all()[:top_k]
    id_to_pos = {pid: pos for pos, pid in enumerate(ids)}
    sim = RECOMMENDER_STATE["similarity"]
    user_feedback = Feedback.objects.filter(user=user)
    liked_positions = [id_to_pos[f.product_id] for f in user_feedback if f.liked and f.product_id in id_to_pos]
    disliked_positions = [id_to_pos[f.product_id] for f in user_feedback if (not f.liked) and f.product_id in id_to_pos]

    scores = np.zeros(len(ids), dtype=np.float64)
    for pos in liked_positions:
        scores += sim[pos]
    for pos in disliked_positions:
        scores -= 0.5 * sim[pos]

    for f in user_feedback:
        if f.product_id in id_to_pos:
            scores[id_to_pos[f.product_id]] = -9999

    top_idx = np.argsort(-scores)[:top_k]
    top_ids = [ids[i] for i in top_idx]
    qs = Product.objects.filter(id__in=top_ids)
    ordered = sorted(qs, key=lambda p: top_ids.index(p.id))
    return ordered

def index(request):
    products = Product.objects.all()[:30]
    recs = []
    if request.user.is_authenticated:
        recs = recommend_for_user(request.user, top_k=6)
    return render(request, "shop/index.html", {"products": products, "recommendations": recs})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recs = []
    if request.user.is_authenticated:
        recs = recommend_for_user(request.user, top_k=6)
    return render(request, "shop/product_detail.html", {"product": product, "recommendations": recs})

@login_required
def add_to_cart(request):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            pid = form.cleaned_data["product_id"]
            qty = form.cleaned_data["quantity"]
            product = get_object_or_404(Product, pk=pid)
            ci, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                ci.quantity += qty
            else:
                ci.quantity = qty
            ci.save()
    return redirect("shop:cart")

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum([item.product.price * item.quantity for item in items])
    return render(request, "shop/cart.html", {"items": items, "total": total})

@login_required
def checkout(request):
    CartItem.objects.filter(user=request.user).delete()
    return render(request, "shop/checkout.html")

@login_required
def feedback_view(request):
    if request.method == "POST":
        pid = int(request.POST.get("product_id"))
        liked = request.POST.get("liked") == "true"
        product = get_object_or_404(Product, pk=pid)
        Feedback.objects.update_or_create(user=request.user, product=product, defaults={"liked": liked})
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def recommendations_api(request):
    recs = recommend_for_user(request.user, top_k=8)
    data = [{"id": p.id, "title": p.title, "price": str(p.price)} for p in recs]
    return JsonResponse({"recommendations": data})
