import random
from django.contrib.auth.models import User
from contacts.models import Contact, Organization

# Get any existing user and organization to assign as owner/org
default_user = User.objects.first()
default_org = Organization.objects.first()

pokemon_jobs = [
    ("Pikachu", "Electrician"),
    ("Charizard", "Fire Safety Officer"),
    ("Bulbasaur", "Botanist"),
    ("Squirtle", "Water Technician"),
    ("Jigglypuff", "Vocal Coach"),
    ("Meowth", "Finance Analyst"),
    ("Gengar", "Night Guard"),
    ("Machamp", "Fitness Trainer"),
    ("Alakazam", "Data Scientist"),
    ("Snorlax", "Sleep Consultant"),
    ("Eevee", "Adaptability Coach"),
    ("Mewtwo", "Geneticist"),
    ("Lucario", "Martial Arts Instructor"),
    ("Gardevoir", "Counselor"),
    ("Gyarados", "Oceanographer"),
    ("Dragonite", "Pilot"),
    ("Blastoise", "Water Cannon Engineer"),
    ("Venusaur", "Botanist"),
    ("Arcanine", "Firefighter"),
    ("Zapdos", "Electrical Engineer"),
    ("Articuno", "Cryogenics Specialist"),
    ("Moltres", "Wildfire Analyst"),
    ("Ditto", "Impersonator"),
    ("Psyduck", "Neurologist"),
    ("Onix", "Geotechnical Engineer"),
    ("Lapras", "Ferry Captain"),
    ("Magneton", "Magnetics Expert"),
    ("Hitmonlee", "Kickboxing Coach"),
    ("Hitmonchan", "Boxing Coach"),
    ("Scyther", "Landscaper"),
    ("Mr. Mime", "MIME Artist"),
    ("Jolteon", "EV Specialist"),
    ("Vaporeon", "Aquatic Designer"),
    ("Flareon", "Thermal Systems Engineer"),
    ("Umbreon", "Night Supervisor"),
    ("Espeon", "Psychic Consultant"),
    ("Sylveon", "Therapist"),
    ("Togepi", "Daycare Assistant"),
    ("Tyranitar", "Demolition Expert"),
    ("Zoroark", "Undercover Agent"),
    ("Greninja", "Ninja Trainer"),
    ("Infernape", "Fire Dancer"),
    ("Torterra", "Conservationist"),
    ("Empoleon", "Marine Biologist"),
    ("Gallade", "Swordsmanship Coach"),
    ("Noivern", "Sound Engineer"),
    ("Aegislash", "Antique Curator"),
    ("Togekiss", "Flight Attendant"),
    ("Chandelure", "Lighting Designer"),
    ("Hawlucha", "Wrestler"),
]

domains = ["pokejobs.com", "palettetown.org", "kanto.co", "trainer.io"]
last_names = ["Smith", "Johnson", "Lee", "Brown", "Taylor", "Walker"]

for i in range(100):
    first, title = random.choice(pokemon_jobs)
    last = random.choice(last_names)
    email = f"{first.lower()}.{last.lower()}.{i}@{random.choice(domains)}"
    phone = f"+1{random.randint(2000000000, 9999999999)}"  # Matches your regex
    org = default_org if default_org else None
    user = default_user if default_user else None

    # Skip if email already exists
    if Contact.objects.filter(email=email).exists():
        continue

    Contact.objects.create(
        first_name=first,
        last_name=last,
        job_title=title,
        phone_number=phone,
        email=email,
        organization=org,
        owner=user,
    )

print("✅ 100 Pokémon-based contacts added (or skipped if email existed).")
