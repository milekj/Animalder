from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from mainApp.forms import SignUpForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainApp.models import Profile, Rating, Match, Message

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.dateOfBirth = form.cleaned_data['dateOfBirth']
            user.profile.profilePhoto = form.cleaned_data['profilePhoto']
            user.profile.sex = form.cleaned_data['sex']
            user.profile.lookingFor = form.cleaned_data['lookingFor']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/profile/' + user.username)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})    

@login_required
def rate(request, ratedUserID = 0):
    currentProfile = request.user.profile
    try:
        if request.POST['choice'] == 'True':
            choice = True
        else:
            choice = False

    except KeyError:
        try:
            alreadyRated = Rating.objects.all() \
                            .filter(ratingUser=currentProfile) \
                            .values('ratedUser')

            userToRate = Profile.objects.all() \
                            .exclude(id__in=alreadyRated) \
                            .exclude(id=currentProfile.id) \
                            .filter(sex=currentProfile.lookingFor) \
                            .filter(lookingFor=currentProfile.sex) \
                            .order_by('?') \
                            .first()

            return render(request, 'rate.html', {'user': userToRate.user})
        except AttributeError:
            return render(request, 'noProfilesToRate.html')
            
    else:
        ratedProfile = User.objects.get(id=ratedUserID).profile
        rating = Rating(ratingUser = currentProfile, ratedUser = ratedProfile, like = choice)
        rating.save()
        
        currentProfileLiked = Rating.objects \
                                .filter(ratedUser = currentProfile) \
                                .filter(ratingUser = ratedProfile) \
                                .filter(like=True) \
                                .exists()

        if rating.like and currentProfileLiked:
            match = Match(user1 = currentProfile, user2 = ratedProfile)
            match.save()
        return redirect('/rate/')

@login_required
def profile(request, username):
    return render(request, 'profile.html', {'user': User.objects.all().get(username=username)})

@login_required
def selfProfile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def matches(request):
    matchesList = getMatches(request.user.profile)
    return render(request, 'matches.html', {'matches': matchesList})

@login_required
def mailbox(request):
    matchesList = getMatches(request.user.profile)
    return render(request, 'mailbox.html', {'matches': matchesList})

@login_required
def message(request, username):
    currentProfile = request.user.profile
    otherProfile = User.objects.get(username=username).profile

    qr = Message.objects \
        .raw('SELECT id, sender_id, text, sentDate \
             FROM mainApp_message \
             WHERE sender_id = {0} AND recipient_id = {1} \
             UNION \
             SELECT id, sender_id, text, sentDate \
             FROM mainApp_message \
             WHERE sender_id = {1} AND recipient_id = {0} \
             ORDER BY sentDate'.format(currentProfile.id, otherProfile.id))
             
    messages = [ (Profile.objects.get(id=m.sender_id), m.text) for m in qr]

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(sender = currentProfile, recipient = otherProfile, text = form.cleaned_data['text'])
            message.save()
            return redirect(request.path)
    else:
        form = MessageForm()

    return render(request, 'message.html', {'messages': messages, 'form': form})


def menu(request):
    return render(request, 'menu.html')

def getMatches(currentProfile):
    matches1 = [ Profile.objects.get(id=e['user2']).user for e in Match.objects.filter(user1 = currentProfile).values('user2') ]
    matches2 = [ Profile.objects.get(id=e['user1']).user for e in Match.objects.filter(user2 = currentProfile).values('user1') ]
    return matches1 + matches2