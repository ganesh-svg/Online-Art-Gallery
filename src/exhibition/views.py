from django.http import request
from django.shortcuts import redirect, render
from .forms import add_update_art_form
from client.models import client, artist
from .models import exhibtion, art, auction as auc
from django.contrib.auth.models import User
from django.db.models import Max
from decimal import Decimal
# Create your views here.


def exhibition_hall(request):
    """
    This function is home for the exhibition hall
    """
    if(artist.objects.filter(user=request.user).first()):
        is_artist = True
    else:
        is_artist = False

    if(request.user.is_superuser):
        arts = art.objects.filter(is_approved=False).order_by('date_created')
    elif artist.objects.filter(user=request.user).first():
        arts = art.objects.filter(
            artist=artist.objects.filter(user=request.user).first())

    else:
        arts = art.objects.filter(is_approved=True)
    context = {
        "arts": arts,
        "is_artist": is_artist
    }
    return render(request, "exhibition/exhibition-hall.html", context)


def add_art(request):
    current_artist = artist.objects.filter(user=request.user).first()
    if(current_artist):
        form = add_update_art_form()
        if request.method == "POST":
            form = add_update_art_form(request.POST, request.FILES)
            current_art = form.save(commit=False)
            current_art.exhibtion = exhibtion.objects.first()
            current_art.artist = current_artist
            current_art.save()
            return redirect("exhibition:exhibition-hall")
        context = {
            "form": form
        }
        return render(request, "exhibition/add-update-art.html", context)

    else:
        return render(request, "exhibition/not-found.html", {"error": "this feature is only available to artist"})


def art_showcase(request, art_id):

    current_art = art.objects.filter(id=art_id).first()
    if(client.objects.filter(user=request.user)):
        is_client = True
    else:
        is_client = False
    print(current_art)
    context = {
        "art": current_art,
        "is_client": is_client
    }
    return render(request, "exhibition/art-showcase.html", context)


def approve_art(request):
    if(request.user.is_superuser and request.method == "POST"):
        art_id = request.POST.get('art_id')
        art_obj = art.objects.get(id=art_id)
        art_obj.is_approved = True
        art_obj.save()
        return redirect("exhibition:exhibition-hall")
    else:
        return render(request, "exhibition/not-found.html", {
            "error": "you are not the adminstrator user"
        })


def auction(request):
    current_client = client.objects.filter(user=request.user).first()
    if(current_client and request.method == "POST"):
        bid_amount = request.POST.get('bid_amount')
        art_id = request.POST.get('art_id')
        current_art = art.objects.filter(id=art_id).first()
        max_bid = auc.objects.filter(
            art=current_art).aggregate(Max('bid_amount'))["bid_amount__max"]
        if(max_bid):
            if (Decimal(bid_amount) > Decimal(current_art.minimum_price)):
                auc.objects.create(
                    art=current_art, client=current_client, bid_amount=Decimal(bid_amount))
                current_art.minimum_price = Decimal(bid_amount)
                current_art.save()
            else:
                return render(request, "exhibition/not-found.html", {
                    "error": "you must increase bid than current bid"
                })

        elif Decimal(bid_amount) > current_art.minimum_price:
            auc.objects.create(
                art=current_art, client=current_client, bid_amount=Decimal(bid_amount))
            current_art.minimum_price = Decimal(bid_amount)
            current_art.save()

        else:
            return render(request, "exhibition/not-found.html", {
                "error": "you must increase bid than current bid"
            })

    return redirect("exhibition:art-showcase", art_id)
