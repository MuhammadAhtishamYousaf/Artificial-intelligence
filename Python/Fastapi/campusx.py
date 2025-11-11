
import json
from fastapi import FastAPI, Path,HTTPException,Query
from fastapi.responses import JSONResponse
from typing import Annotated,Literal
from pydantic import BaseModel,Field,computed_field

app=FastAPI(
    title="Patient Management System",
    description="This Management System is created from campusx"
)


#Pydantic model
class PatientClass(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=["P001"])]
    name:Annotated[str,Field(...,description="Name of the patient",examples=["Ahtisham"])]
    city:Annotated[str,Field(...,description="City name of the patient",examples=["lahore"])]
    age:Annotated[int,Field(...,description="Age of the patient.",examples=[40,50],gt=0,lt=100)]
    gender:Annotated[Literal["male","female","other"],Field(...,description="Gender of the patient.")]
    height:Annotated[float,Field(...,description="Hieght of the patient in mtrs")]
    weight:Annotated[float,Field(...,description="Weight of the patient in kgs")]

    @computed_field
    @property
    # method 
    def bmi(self) ->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi <18.5:
            return "Underweight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"
    

@app.get("/")
def hello():
    return {"message": "Assalam-o-Alaikum, Welcome to Patient Management System!"}

@app.get("/about")
def about():
    return "This is a patient management system. It helps to manage the patients and their records."


def load_data():
    with open(file='./patients.json',mode="r") as f:
        data=json.load(f)
        return data 
    
def save_data(data):
    with open(file='./patients.json',mode='w') as f:
        json.dump(data,f)

#Get all patients
@app.get("/view")
def view():
    data=load_data()
    print(data)
    return data

# get patient with id 
@app.get("/view/{patient_id}")
def view_with_id(patient_id:str=Path(...,description="Enter Patient ID",example="P001")):
    patient_data=load_data()
    if patient_id in patient_data:
        specific_data=patient_data[patient_id]
        return specific_data
    else:
        raise HTTPException(status_code=404,detail="ID not found.")


@app.get("/sort")
def sort_patients(sort_by:str = Query(..., description="Sort on the basis of height, weight or bmi"), order_by:str =Query('asc',description='sort in asc or desc order')):
    valid_fields=["height","weight","bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Kindly selct valid field: {valid_fields}")
    
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"Kindly select valid order: ['asc','dsc']")
    
    data=load_data()
    print(data.values())
    sorted_order=True if order_by=='desc' else False
    sorted_data=sorted(data.values(),key= lambda x: x.get(sort_by,0),reverse=sorted_order)
    return sorted_data


@app.post("/create_patient")
def create_patient(patient:PatientClass):

    #load existing data 
    data=load_data()
    #check if patient id is already exist
    if patient.id in data.keys():
        raise HTTPException(status_code=400, detail="Patient is already exist.")
    #new patient data store
    data[patient.id]=patient.model_dump(exclude=["id"])

    #save into json
    save_data(data)

    return JSONResponse(status_code=201,content="Patient created successfully.")