from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from events.models import Event, Participant, Category
from events.forms import EventModelForm,CateModelForm,ParticipantModelForm
from django.utils import timezone


def home(request):
    type = request.GET.get('type', 'all')
    
    # Get category count
    counts = Category.objects.aggregate(total=Count('id'))
    
    # Get categories with their events
    categories_with_events = Category.objects.prefetch_related('events').all()
    
    # Get events based on type
    if type == 'all':
        event_list = Event.objects.select_related('category').all()
    else:
        event_list = Event.objects.select_related('category').filter(
            category__name=type
        )
    
    context = {
        "categories_with_events": categories_with_events,
        "event_list": event_list,
        "counts": counts,
        "selected_type": type
    }
    return render(request, "events/home.html", context)

def event_details(request, event_id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=event_id)
    context = {
        'event': event
    }
    return render(request, 'events/event_details.html', context)

def participants(request):
    all_participants = Participant.objects.all()
    context = {"participants": all_participants}
    return render(request,"events/participants.html",context)

def categories(request):
    all_cate = Category.objects.all()
    context = {"category":all_cate}
    return render(request,"events/categories.html",context)




#Evant-Functions
def create_event(request):
    form = EventModelForm() #You don't have to menually provide employee
    print(form.fields)
    if request.method=="POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('successful')
            #return render(request,"events/create_event.html",{"form": form,"message": "New Event Created!!!"})
    return render(request,"events/create_event.html",{"form": form})

def update_event(request,id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)
    print(form.fields)
    if request.method=="POST":
        form = EventModelForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('successful')
    return render(request,"events/create_event.html",{"form": form})

def delete_event(request,id):
    if request.method=="POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted From The List')
        return redirect('successful')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('home')







#Category-Functions
def create_cate(request):
    form = CateModelForm() #You don't have to menually provide employee
    print(form.fields)
    if request.method=="POST":
        form = CateModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('successful')
    return render(request,"events/create_cate.html",{"form": form})

def update_cate(request,id):
    category = Category.objects.get(id=id)
    form = CateModelForm(instance=category)
    print(form.fields)
    if request.method=="POST":
        form = CateModelForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('successful')
    return render(request,"events/create_cate.html",{"form": form})

def delete_cate(request,id):
    if request.method=="POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, 'Category Deleted From The List')
        return redirect('categories')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('home')







#Add_Participants
def add_people(request):
    form = ParticipantModelForm() #You don't have to menually provide employee
    print(form.fields)
    if request.method=="POST":
        form = ParticipantModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Participant Added to the List")
            return redirect('successful')
    return render(request,"events/add_people.html",{"form": form})

def update_people(request,id):
    people = Participant.objects.get(id=id)
    form = ParticipantModelForm(instance=people)
    print(form.fields)
    if request.method=="POST":
        form = ParticipantModelForm(request.POST,instance=people)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant Details Updated Successfully")
            return redirect('successful')
    return render(request,"events/add_people.html",{"form": form})

def delete_people(request,id):
    if request.method=="POST":
        people = Participant.objects.get(id=id)
        people.delete()
        messages.success(request, 'Participant Removed From The List')
        return redirect('participants')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('home')





def dashboard(request):
    
    type = request.GET.get('type', 'today')
    today = timezone.now().date()
    data = Event.objects.filter(date=today)
    heading = "Today's Event"
    No_data = "There is no event today"
    counts = Category.objects.aggregate(
    total_categories=Count('id'),
    total_events=Count('events', distinct=True),
    total_participants=Count('events__participants', distinct=True),
    upcoming_events=Count('events', filter=Q(events__date__gte=today), distinct=True),
    past_events=Count('events', filter=Q(events__date__lt=today), distinct=True)
)

    if type == 'all':
        data = Event.objects.all()
        heading = "All Event"
        No_data = "No events has been added yet"
    elif type == 'upcoming':
        data = Event.objects.filter(date__gt=today)
        heading = "Upcoming Events"
        No_data = "No upcoming event on the list"
    elif type == 'past':
        data = Event.objects.filter(date__lt=today)
        heading = "Past Event"
        No_data = "No past event on the list"
    elif type == 'participants':
        data = Participant.objects.all()
        heading = "All Participants"
        No_data = "No participant has been added yet"

    
    context = {"counts":counts,"data":data,"type":type,"heading":heading,"no_data":No_data}
    return render(request,"events/dashboard.html",context)

def successful(request):
    return render(request,"events/success.html")



def search_events(request):
    search_query = request.GET.get('search', '')
    events = []
    
    if search_query:
        events = Event.objects.filter(
            Q(name__icontains=search_query) | 
            Q(location__icontains=search_query)
        )
    context = {
        'event_list': events,
        'search_query': search_query,
    }
    return render(request, 'events/search.html', context)