from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials=None
credentials = service_account.Credentials.from_service_account_file('core/keys.json', scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
# Call the Sheets API
sheet = service.spreadsheets()

def home(request):
    user=request.user 
    return render(request,'core/index.html')
    
def countdata(user):    
    result = sheet.values().get(spreadsheetId="1ovD41uW0qV8qBnjSnSspQo2uCg26_MafNUPwctE1Ipc", range=user.username+"!A2:B").execute()
    values = result.get('values', [])
    counturl=len(values)
    return counturl


def enterdata(request):
    url="https://docs.google.com/spreadsheets/d/"
    full=url
    counturl=0
    if request.user.is_authenticated:
        user=request.user  
        counturl=countdata(request.user)
        if request.method=='POST':
            url=request.POST['url']
            data=[url, user.username]
            req=sheet.values().append(spreadsheetId="1ovD41uW0qV8qBnjSnSspQo2uCg26_MafNUPwctE1Ipc", range=user.username+"!A2:B", valueInputOption="USER_ENTERED", body={"values":[data]} ).execute()
            messages.success(request,'Data has been submitted successfully')
            return redirect('/enterdata/')
    else:
        return render(request,'core/enter.html')
    return render(request,'core/enter.html',{'full':url+"1ovD41uW0qV8qBnjSnSspQo2uCg26_MafNUPwctE1Ipc",'counturl':counturl})


#Register

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already taken')
                return redirect('/register/')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email has already taken')
                return redirect('/register/')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email, username=username, password=password1)
                user.save()
                messages.success(request,'User has been created successfully')
                return redirect('/')
        else:
            messages.warning(request,'password not matched')
            return redirect('/register/')
    return render(request,'account/register.html')
#login
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'User not found')
            return redirect('/login/')
        else:
            auth.login(request,user)
            return redirect('/')    
    return render(request,'account/login.html')

#logout
def logout(request):
    auth.logout(request)
    return redirect('/')