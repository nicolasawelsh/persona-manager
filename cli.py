import argparse
from persona import Person
from persona import Session

def create_persona(args):
    persona = Person()
    persona.save()
    print("Persona created successfully.")

def view_personas(args):
    personas = Person.get_all()
    if personas:
        for persona in personas:
            persona.print_person()
    else:
        print("No personas found.")

def delete_personas(args):
    if args.id:
        Person.delete_by_id(args.id)
        print(f"Persona with ID {args.id} deleted successfully.")
    else:
        Person.delete_all()
        print("All personas deleted successfully.")

def modify_persona(args):
    personas = Person.get_all()
    if personas:
        for persona in personas:
            if persona.id == args.id:
                # Detach the persona from the current session
                session = Session.object_session(persona)
                session.expunge(persona)

                if args.gender:
                    persona.gender = args.gender
                if args.address:
                    persona.address = args.address
                if args.phone:
                    persona.phone = args.phone
                if args.birthday:
                    persona.birthday = args.birthday
                if args.username:
                    persona.username = args.username
                if args.password:
                    persona.password = args.password
                if args.email:
                    persona.email = args.email

                persona.save()
                print("Persona modified successfully.")
                return
        print("Persona not found.")
    else:
        print("No personas found.")


def main():
    parser = argparse.ArgumentParser(description="Persona Manager CLI")
    subparsers = parser.add_subparsers()

    # Create Persona
    create_parser = subparsers.add_parser("create", help="Create a new persona")
    create_parser.set_defaults(func=create_persona)

    # View Personas
    view_parser = subparsers.add_parser("view", help="View all personas")
    view_parser.set_defaults(func=view_personas)

    # Delete Personas
    delete_parser = subparsers.add_parser("delete", help="Delete a persona by ID")
    delete_parser.add_argument("id", type=int, help="ID of the persona to delete")
    delete_parser.set_defaults(func=delete_personas)

    # Modify Persona
    modify_parser = subparsers.add_parser("modify", help="Modify an existing persona")
    modify_parser.add_argument("id", type=int, help="ID of the persona to modify")
    modify_parser.add_argument("--gender", help="Update gender")
    modify_parser.add_argument("--address", help="Update address")
    modify_parser.add_argument("--phone", help="Update phone number")
    modify_parser.add_argument("--birthday", help="Update birthday")
    modify_parser.add_argument("--username", help="Update username")
    modify_parser.add_argument("--password", help="Update password")
    modify_parser.add_argument("--email", help="Update email")
    modify_parser.set_defaults(func=modify_persona)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
