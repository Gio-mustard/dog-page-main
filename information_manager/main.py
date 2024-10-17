if __name__ == '__main__':
    from groq_use import get_schema
else:
    from .groq_use import get_schema
import json

def get(description:str,pattern:str)->dict:
    if (
        description==""
        or
        len(description)<20
        or 
        description==None
        ):
        raise ValueError("description is required and the min lenght is 20 characters")
    
    return get_schema(description=description,pattern=pattern) # es la description eh!

if __name__ == '__main__':
    pet = get("Es una perrita cafe que al acercarse mucho a ella te muerde o chupa la mano come mucho y es de raza pitbul")
    pet_pattern = "race, color, name"
    import json
    """
    'name': 'John Doe',
    'address': '123 Main St',
    'phone_number': '555-1234',
    'email': 'john@example.com',
    'extra': ['No extra information']
    """
    owner = get("Me llamo sergio manuel morquecho soto mi correo es sergio@gmail.com me gusta la coca vivo alado de la casa de mi vecino y mi numero telefonico es +526863671318",pattern='name,addres,phone_number,email')
    print(json.dumps(pet, indent=2))
    print(json.dumps(owner, indent=2))
