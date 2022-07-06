from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password
from datetime import datetime
from bson.json_util import dumps
from django.core.paginator import Paginator

# DJANGO + PYMONGO start ------------------------------------------------------------------------------------------

def createConnection():
    client = MongoClient()
    client = MongoClient('localhost', 27017)

    db = client.CRUDDashboard
    return db


def findData():
    db = createConnection()

    collection = db.login
    loginData = collection.find()
    loginCount = collection.find().count()

    collection = db.company
    companyData = collection.find()
    companyCount = collection.find().count()

    collection = db.plan
    planData = collection.find()
    planCount = collection.find().count()

    data = {
        'loginData': loginData,
        'loginCount': loginCount,
        'companyData': companyData,
        'companyCount': companyCount,
        'planData': planData,
        'planCount': planCount
    }

    return data


def home(req):
    data = findData()

    return render(req, "app/index.html", data)


def company(req):
    data = findData()

    return render(req, "app/companyDetails.html", data)


def plan(req):
    data = findData()

    return render(req, "app/planDetails.html", data)


def editPlan(req, data):
    if req.method == 'GET':
        print("editPlan=>", data)
        db = createConnection()
        collection = db.plan
        planData = collection.find_one({"id": int(data)})
        print("editPlan=>", planData['planName'])

        return render(req, "app/editPlan.html", {"planData": planData})

    if req.method == 'POST':
        planName = req.POST['planName']
        planValidity = req.POST['planValidity']
        planPrice = req.POST['planPrice']

        db = createConnection()
        collection = db.plan

        collection.update_one(
            {"id": int(data)},
            {"$set":
             {
                 "planName": planName,
                 "validity": planValidity,
                 "price": (int(planPrice))
             }
             })

        data = findData()

        return render(req, "app/planDetails.html", data)


def deletePlan(req, data):
    db = createConnection()
    collection = db.plan

    get = collection.delete_one({"id": int(data)})
    # print( get )

    data = findData()

    return render(req, "app/planDetails.html", data)


def addPlan(req):
    if req.method == 'GET':
        print("GET")
        return render(req, "app/addPlan.html")

    if req.method == 'POST':
        planName = req.POST['planName']
        planValidity = req.POST['planValidity']
        planPrice = req.POST['planPrice']
        print("POST=>", planName, planValidity, planPrice)

        db = createConnection()
        collection = db.plan

        # To keep track of count
        countCollection = db.planCount
        data = countCollection.find_one()
        count = data['IdCount']

        planData = {
            "id": count+1,
            "planName": planName,
            "validity": planValidity,
            "price": (int(planPrice))
        }
        collection.insert_one(planData)

        countCollection.update_one(
            {"collection": "plan"},
            {"$set": {"IdCount": count+1}
             })

        return render(req, "app/addPlan.html", {"val": True})

# Adding data to database using this function below
def addDetails(req):
    db = createConnection()

    countCollection = db.companyCount
    data = countCollection.find_one()
    count = data['IdCount']

    countCollection.update_one(
        {"collection": "company"},
        {"$set": {"IdCount": count+1}
         })

    # collection = db.login
    # loginData = {
    #     "id": count+1,
    #     "email": "sample@mail.com",
    #     "password": make_password("1234")
    # }
    # now = datetime.now()
    # date_format = now.strftime("%d/%m/%Y %H:%M:%S")

    # collection = db.plan
    # planData = {
    #    "id":collection.find().count()+1,
    #    "planName":"Basic",
    #    "validity":date_format,
    #    "price":567,
    # }

    collection = db.company
    companyData = {
        "id": count+1,
        "userId": "333",
        "userName": "dummyUser"

    }

    # collection = db.companyCount
    # companyCountData = {
    #     "collection":"company",
    #     "IdCount":0
    # }

    # data = collection.find_one()
    # print( data['IdCount'] )

    collection.insert_one(companyData)

    # get = collection.delete_one({"id":4})
    # print( get )

    return HttpResponse("Added")
# DJANGO + PYMONGO end --------------------------------------------------------------------------------------------------


# DJANGO + DJONGO-ENGINE start ------------------------------------------------------------------------------------------

# def findCount():
#     loginCount = CustomerData.objects.count()
#     companyCount = Company.objects.count()
#     planCount = PlanDetails.objects.count()

#     data = {
#         "loginCount": loginCount,
#         "companyCount": companyCount,
#         "planCount": planCount
#     }

#     return data


# def home(req):
#     count = findCount()

#     data = CustomerData.objects.all()

#     return render(req, "app/index.html", {"data": data, "count": count})


# def company(req):
#     count = findCount()
#     data = Company.objects.all()

#     return render(req, "app/companyDetails.html",  {"data": data, "count": count})


# def plan(req):
#     count = findCount()
#     data = PlanDetails.objects.all()

#     return render(req, "app/planDetails.html",  {"data": data, "count": count})


# def editPlan(req, data):
#     if req.method == 'GET':
#         print("editPlan=>", data)

#         planData = PlanDetails.objects.get(planId=data)
#         # print(planData.validity)

#         return render(req, "app/editPlan.html", {"planData": planData})
#         # return HttpResponse("Edit")

#     if req.method == 'POST':
#         planName = req.POST['planName']
#         planValidity = req.POST['planValidity']
#         planPrice = req.POST['planPrice']

#         planData = PlanDetails.objects.get(planId=data)
#         planData.planName = planName
#         planData.validity = planValidity
#         planData.price = planPrice
#         planData.save()

#         count = findCount()
#         data = PlanDetails.objects.all()

#         return render(req, "app/planDetails.html", {"data": data, "count": count})


# def deletePlan(req, data):
#     # print("deletePlan=>", data)
#     form = PlanDetails.objects.get(planId=data)
#     form.delete()

#     count = findCount()
#     data = PlanDetails.objects.all()

#     return render(req, "app/planDetails.html", {"data": data, "count": count})


# def addPlan(req):
#     if req.method == 'GET':
#         print("GET")
#         return render(req, "app/addPlan.html")

#     if req.method == 'POST':
#         planName = req.POST['planName']
#         planValidity = req.POST['planValidity']
#         planPrice = req.POST['planPrice']
#         print("POST=>", planName, planValidity, planPrice)

#         form = PlanDetails(planName=planName,
#                            validity=planValidity, price=planPrice)
#         form.save()
#         return render(req, "app/addPlan.html", {"val": True})


# def addDetails(req):
#     form = CustomerData(First_Name="Akshay", Last_Name="Kumar", Email="Akshay@mail.com", Contact_number="1234567899",
#                  Address="Delhi", Gender="Male", Password=make_password("456789"), PlanDetails="Silver", Status=1)

#     form.save()

#     return HttpResponse("Added")

# DJANGO + DJONGO-ENGINE end ------------------------------------------------------------------------------------------
