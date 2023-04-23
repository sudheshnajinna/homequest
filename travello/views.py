from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Destination, Wishlist, Apartment
import json
from django.http import JsonResponse
import openai
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

openai.api_key = "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"
model_engine = "text-davinci-002"

@csrf_exempt
def chatbot(request):
    print(request.POST.get("message"))
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            prompt = f"{message}\nChatbot:"
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            chatbot_response = response.choices[0].text.strip()
        else:
            chatbot_response = "Please enter a message."
        
        return JsonResponse({"message": chatbot_response})


def index(request):
    if request.user.is_authenticated:
        abc = Wishlist()
        abc.apartmentID = 1
        abc.username = "rk"
        #abc.save()
        for x in Wishlist.objects.all():
            print(str(x.username) + " " + str(x.apartmentID))
        return render(request, "index.html", {'dests': dests,  'loggedIn':'true'})
    else:
        return render(request, "index.html", {'dests': dests})

def apartments(request):
    all_apartments = Apartment.objects.all()
    if request.method == 'POST':
        
        #selectedIds = json.loads(request.POST.get('selectedIds'))
        fields = request.POST.get('fields')
        bedrooms = request.POST.get('bedrooms')
        radius = request.POST.get('radius')
        propertyType = request.POST.get('propertyType')
        priceRange = request.POST.get('priceRange')
        fields_dict = json.loads(fields)
        # print(fields)
        # print(bedrooms)
        # print(radius)
        # print(propertyType)
        # print(fields_dict)
        

        apartments = Apartment.objects.filter(Beds__range=(int(bedrooms)-1, int(bedrooms)+1), Radius__range=(int(radius)-5, int(radius)+5))
        if propertyType and propertyType != "any":
            apartments = apartments.filter(Type=propertyType)
        else:
            apartments = apartments.all()

        if priceRange is not None:
            priceRange = int(priceRange)
            min_rent = priceRange - 500 if priceRange >= 500 else 0
            max_rent = priceRange + 500
            apartments = apartments.filter(Rent__range=(min_rent, max_rent))
        else:
            apartments = apartments.all()
        
        for apartment in apartments:
            print(apartment.ApartmentID, apartment.Address, apartment.Name, apartment.Rent)
        for field, value in fields_dict.items():
            if value == True:
                print("inside true")
                apartments = apartments.filter(**{field: True})
            # elif value == False:
            #     print("inside false")
            #     apartments = apartments.filter(**{field: False})
        for apartment in apartments:
            print(apartment.ApartmentID, apartment.Address, apartment.Name, apartment.Rent)
        if not apartments:
            print("No apartments found")
        else:
            for apartment in apartments:
                print("hello")
                print(apartment.Name)
        loggedIn = request.user.is_authenticated
        apts = []
        for y in Wishlist.objects.all():
                apts = apts + [x for x in all_apartments if int(x.ApartmentID) == int(y.apartmentID) and str(y.username) == str(request.user)]
        return render(request, "apartments.html", {'dests': apartments,'wishes': apts, 'loggedIn': loggedIn})
    else:
        if request.user.is_authenticated:
            apts = []
            loggedIn = True
            for y in Wishlist.objects.all():
                apts = apts + [x for x in all_apartments if int(x.ApartmentID) == int(y.apartmentID) and str(y.username) == str(request.user)]
            return render(request, "apartments.html", {'dests': all_apartments,'wishes': apts, 'loggedIn': loggedIn})
        else:
            # all_apartments = Apartment.objects.all()
            return render(request, "apartments.html", {'dests': all_apartments})

def logout(request):
    print("called before")
    if request.user.is_authenticated:
        print("called")
        auth.logout(request)
        return redirect('/')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        print("hello")
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            print("signed in user successfully")
            return render(request, "index.html", {'dests': dests})
        else:
            return redirect('/signup')
    else:
        return render(request,'signup.html')

def signup(request):
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(username)
        print(password)
        print(email)
        user=User.objects.create_user(username=username,password=password,first_name='',email=email,last_name='')
        return render(request, "signup.html")
    else:
        return render(request, "signup.html", {'dests': dests})

def wishlist(request):
    # if request.method == 'POST':       
    #     wishlistDestinationsjson = json.loads(request.POST.get('wishlistDestinations'))
    #     wishlistDestinations = []
    #     for destination_data in wishlistDestinationsjson:
    #         destination = Destination()
    #         destination.id=int(destination_data['id'])
    #         destination.name=destination_data['name']
    #         destination.description=destination_data['desc']
    #         destination.price=int(destination_data['price'])
    #         destination.image=destination_data['img']
    #         wishlistDestinations.append(destination)
    #     print(wishlistDestinations)
    #     print(dests)
        
    #     return render(request, "wishlistpage.html", {'wishes': wishlistDestinations})
    if request.user.is_authenticated:
        print("fetch data from db and serve")
        # get data from db
        apts = []
        all_apartments = Apartment.objects.all()
        for y in Wishlist.objects.all():
            apts = apts + [x for x in all_apartments if int(x.ApartmentID) == int(y.apartmentID) and str(y.username) == str(request.user)]
        print(apts)
        # map apartment objects 
        # send those apartmenmts and render
        return render(request, "wishlistpage.html", {'wishes': apts,'apartmentlist' :all_apartments,'loggedIn':'true'})
    else:
        return render(request, "signup.html")

def addToWishlist(request):
    #create new object save
    abc = Wishlist()
    abc.apartmentID =  request.POST.get('aptID')
    abc.username = request.user
    #abc.save()
    aptID = int(request.POST.get('aptID'))
    # print(type(Wishlist.objects.all()))
    #Wishlist.objects.all().first(x => x.apa)
    found = False
    for x in Wishlist.objects.all():
        if x.username == str(request.user) and x.apartmentID == aptID:
            #remove and break
            obj = Wishlist.objects.get(pk=x.id)
            obj.delete()
            print("remove")
            found = True
            break
    if(found == False):
        abc.save()
        print("saving")
    return JsonResponse("true", safe = False)







dest1 = Destination()
dest1.name = 'Apartment 1'
dest1.img = 'apartment_1.jpg'
dest1.id = '1'
dest1.desc = 'Apartment 1 Desc'
dest1.price = 1700
dest2 = Destination()
dest2.name = 'Apartment 2'
dest2.desc = 'Apartment 2 Desc'
dest2.img = 'apartment_2.jpg'
dest2.id = '2'
dest2.price = 1650
dest3 = Destination()
dest3.name = 'Apartment 3'
dest3.desc = 'Apartment 3 Desc'
dest3.img = 'apartment_3.jpg'
dest3.id = '3'
dest3.price = 1750
dest4 = Destination()
dest4.name = 'Apartment 4'
dest4.desc = 'Apartment 4 Desc'
dest4.img = 'apartment_4.jpg'
dest4.id = '4'
dest4.price = 1350

dest5 = Destination()
dest5.name = 'Apartment 5'
dest5.desc = 'Apartment 5 Desc'
dest5.img = 'apartment_5.jpg'
dest5.id = '5'
dest5.price = 1850
dest6 = Destination()
dest6.name = 'Apartment 6'
dest6.desc = 'Apartment 6 Desc'
dest6.img = 'apartment_6.jpg'
dest6.id = '6'
dest6.price = 1250
dest7 = Destination()
dest7.name = 'Apartment 7'
dest7.desc = 'Apartment 7 Desc'
dest7.img = 'apartment_7.jpg'
dest7.id = '7'
dest7.price = 1550
dest8 = Destination()
dest8.name = 'Apartment 8'
dest8.desc = 'Apartment 8 Desc'
dest8.img = 'apartment_8.jpg'
dest8.id = '8'
dest8.price = 1900
dest9 = Destination()
dest9.name = 'Apartment 9'
dest9.desc = 'Apartment 9 Desc'
dest9.img = 'apartment_9.jpg'
dest9.id = '9'
dest9.price = 2200
dests = [dest1, dest2, dest3, dest4, dest5, dest6, dest7, dest8, dest9]
emptywishlist = []