import sys
from src.database import engine
from src.models import Device
from sqlalchemy.orm import Session

def unreg_device(name: str):

    with Session(engine) as session:
        device = session.get(Device, name)

        if not device:
            raise ValueError(f"Device {name} does not exist in database.")
        
        session.delete(device)
        session.commit()

        print(f"Succesfully removed device '{name}' from database.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.unregister_device <name>")
        sys.exit(1)
    
    unreg_device(sys.argv[1])