
from concurrent import interpreters
from dataclasses import dataclass
from typing import List



@dataclass
class User:
    name: str
    age: int
    skills: List[str]


 # ------ Liste von Benutzern mit ihren Eigenschaften -----
 # ------ ohne Klasse -----
users = [
        {
            "name": "Alice",
            "age": 25,
            "skills": ["Python", "c#", "SQL"]
    
        },
        {
            "name": "Bob",
            "age": 30,
            "skills": ["Java", "JavaScript", "Docker"]
        },
        {
            "name": "Charlie",
            "age": 22,
            "skills": ["HTML", "CSS", "React"]
        },
        {
            "name": "David",
            "age": 28,
            "skills":["Go","Kubernetes", "AWS"]
        },
        { 
            "name": "Eve",
            "age": 23,
            "skills": ["Ruby", "Rails", "PostgreSQL"]
       
        },
        {
             "name":"Luisa",
             "age": 26,
             "skills":["Js", "Angular", "TypeScript"]
        }
    
 ]


kunden: List[User]= [   
    User(name ="Max Mustermann", 
        age=30, 
        skills=["Py","C#","SQL"]
        ),
    User(
        name="Erika Mustermann",
        age=28,
        skills=["Java", "JavaScript", "Docker"]),
    User(name="Lukas Weber", 
         age=31, 
         skills=["JS","Py","React"]),
    User(name="Sophie Müller", 
         age=27, 
         skills=["Go","Kubernetes", "AWS"]),
     User(name="Tim Schmidt",
            age=29, 
            skills=["Ruby", "Rails", "PostgreSQL"]),

     User(name="Laura Fischer",
            age=26, 
            skills=["Js", "Angular", "TypeScript"]),
     User(name="Anna Becker",
            age=24, 
            skills=["Python", "Django", "Flask"]),
     User(name="Paul Wagner",
              age=32, 
            skills=["Java", "Spring", "Hibernate"]),

       User(name="Lisa Hoffmann",
            age=27, 
            skills=["C#", ".NET", "Azure"]),

    ]




print("Alle Kunden:")
for k in kunden:
    print(f"{k}")

print("\n")
print("Alle Kunden mit ihren Skills:")
for k in kunden:
    print(f"{k.name} ist {k.age} Jahre alt und hat folgende Skills: {', '.join(k.skills)}")

print("\n")
# Kunden die älter als 28 Jahre alt sind
older_than_28 = [k for k in kunden if k.age > 28]

print("Kunden die älter als 28 Jahre alt sind:")
for kunden in older_than_28:
    print(f"{kunden.name} ist {kunden.age} Jahre alt und hat folgende Skills: {', '.join(kunden.skills)}")



