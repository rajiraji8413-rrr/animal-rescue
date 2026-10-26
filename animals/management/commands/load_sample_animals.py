
import json
import urllib.request
from urllib.error import URLError, HTTPError

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from animals.models import Animal, Species, Breed, Location


SAMPLE_ANIMALS = [
    ("Max", "Dog", "Labrador", 3, "Male", "Trichy"),
    ("Bella", "Dog", "Beagle", 2, "Female", "Madurai"),
    ("Rocky", "Dog", "Indian Pariah", 4, "Male", "Chennai"),
    ("Daisy", "Dog", "Golden Retriever", 1, "Female", "Salem"),
    ("Charlie", "Dog", "German Shepherd", 5, "Male", "Coimbatore"),
    ("Luna", "Cat", "Indian Domestic", 1, "Female", "Trichy"),
    ("Milo", "Cat", "Persian", 2, "Male", "Chennai"),
    ("Coco", "Cat", "Siamese", 3, "Female", "Madurai"),
    ("Leo", "Cat", "Indian Domestic", 2, "Male", "Salem"),
    ("Simba", "Cat", "Persian", 1, "Male", "Coimbatore"),
    ("Buddy", "Dog", "Beagle", 2, "Male", "Trichy"),
    ("Ruby", "Dog", "Indian Pariah", 3, "Female", "Madurai"),
    ("Oreo", "Cat", "Indian Domestic", 1, "Male", "Chennai"),
    ("Bruno 3", "Dog", "Labrador", 4, "Male", "Salem"),
    ("Ginger", "Cat", "Siamese", 2, "Female", "Coimbatore"),
    ("Shadow", "Dog", "German Shepherd", 3, "Male", "Trichy"),
    ("Pepper", "Cat", "Indian Domestic", 1, "Female", "Madurai"),
    ("Daisy 2", "Dog", "Golden Retriever", 2, "Female", "Chennai"),
    ("Simba 2", "Cat", "Persian", 3, "Male", "Salem"),
    ("Lucky", "Dog", "Indian Pariah", 1, "Male", "Coimbatore"),
]


DESCRIPTIONS = {
    "Dog": (
        "Meet {name}, a friendly dog looking for a caring forever home. "
        "Enjoys walks, playtime and companionship. Needs nutritious food, "
        "positive training and regular veterinary care."
    ),
    "Cat": (
        "Meet {name}, a lovely cat looking for a safe and caring home. "
        "Enjoys toys, comfortable resting places and gentle attention. "
        "Needs nutritious food, a clean litter tray and veterinary care."
    ),
}


def download_image(species):
    """Download one random dog or cat image from a public API."""

    if species == "Dog":
        api_url = "https://dog.ceo/api/breeds/image/random"

        request = urllib.request.Request(
            api_url,
            headers={"User-Agent": "AnimalRescueDemo/1.0"},
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        if result.get("status") != "success":
            raise ValueError("Dog image API returned no image.")

        image_url = result["message"]

    else:
        api_url = "https://api.thecatapi.com/v1/images/search"

        request = urllib.request.Request(
            api_url,
            headers={"User-Agent": "AnimalRescueDemo/1.0"},
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        if not result or not result[0].get("url"):
            raise ValueError("Cat image API returned no image.")

        image_url = result[0]["url"]

    image_request = urllib.request.Request(
        image_url,
        headers={"User-Agent": "AnimalRescueDemo/1.0"},
    )

    with urllib.request.urlopen(
        image_request, timeout=30
    ) as response:
        image_bytes = response.read()

    if not image_bytes:
        raise ValueError("Downloaded image is empty.")

    return image_bytes


class Command(BaseCommand):
    help = "Add sample animals and download missing animal images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-images",
            action="store_true",
            help="Create animals without downloading images",
        )

    def handle(self, *args, **options):
        added = 0
        skipped = 0
        images_added = 0
        images_skipped = 0
        image_failures = 0

        for (
            name,
            species_name,
            breed_name,
            age,
            gender,
            location_name,
        ) in SAMPLE_ANIMALS:

            # Create species, breed and location if needed.
            species, _ = Species.objects.get_or_create(
                name=species_name
            )

            breed, _ = Breed.objects.get_or_create(
                species=species,
                name=breed_name,
            )

            location, _ = Location.objects.get_or_create(
                name=location_name
            )

            # Find an existing sample animal or create it.
            animal = Animal.objects.filter(
                name=name,
                location=location,
            ).first()

            if animal is None:
                with transaction.atomic():
                    animal = Animal.objects.create(
                        name=name,
                        species=species,
                        breed=breed,
                        age=age,
                        gender=gender,
                        description=DESCRIPTIONS[
                            species_name
                        ].format(name=name),
                        location=location,
                        status="Available",
                    )

                added += 1
                self.stdout.write(f"Created animal: {name}")

            else:
                skipped += 1
                self.stdout.write(f"Animal already exists: {name}")

            # Do not overwrite an existing image.
            if animal.image:
                images_skipped += 1
                self.stdout.write(f"Photo already exists: {name}")
                continue

            if options["no_images"]:
                continue

            # Download a photo for new or existing animals.
            try:
                image_bytes = download_image(species_name)

                filename = (
                    name.lower().replace(" ", "_") + ".jpg"
                )

                animal.image.save(
                    filename,
                    ContentFile(image_bytes),
                    save=True,
                )

                images_added += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Photo downloaded for: {name}"
                    )
                )

            except (
                URLError,
                HTTPError,
                TimeoutError,
                ValueError,
                OSError,
            ) as error:
                image_failures += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"Could not download photo for {name}: {error}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("IMPORT COMPLETED"))
        self.stdout.write(f"New animals created: {added}")
        self.stdout.write(f"Animals already existing: {skipped}")
        self.stdout.write(f"Photos downloaded: {images_added}")
        self.stdout.write(f"Photos already present: {images_skipped}")
        self.stdout.write(f"Photo download failures: {image_failures}")
