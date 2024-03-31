from src.domain.repository.manwha import (
    ManwhaRepository,
    ManwhaGenreRepository,
    ManwhaArtistRepository,
    ManwhaAlternativeNameRepository,
    ManwhaAuthorRepository,
)
from src.domain.repository.genre import GenreRepository
from src.domain.repository.artist import ArtistRepository
from src.domain.repository.author import AuthorRepository
from src.domain.repository.alternative_name import AlternativeNameRepository
from src.domain.entities.manwha import (
    Manwha,
    ManwhaGenre,
    ManwhaArtist,
    ManwhaAlternativeName,
    ManwhaAuthor,
)
from src.domain.entities.genre import Genre
from src.domain.entities.artist import Artist
from src.domain.entities.author import Author
from src.domain.entities.alternative_name import AlternativeName
from src.domain.use_cases.common.download_image import DownloadImageUseCase
from src.infrastructure.services.s3 import S3Service
from src.infrastructure.config import SETTINGS
from sqlalchemy.orm import Session
import shutil


class ManageManwhaUseCase:
    def __init__(self, session: Session, storage: S3Service):
        self.manwha_repository = ManwhaRepository(session)
        self.genre_repository = GenreRepository(session)
        self.artist_repository = ArtistRepository(session)
        self.author_repository = AuthorRepository(session)
        self.alternative_name_repository = AlternativeNameRepository(session)
        self.manwha_genre_repository = ManwhaGenreRepository(session)
        self.manwha_artist_repository = ManwhaArtistRepository(session)
        self.manwha_author_repository = ManwhaAuthorRepository(session)
        self.manwha_alternative_name_repository = ManwhaAlternativeNameRepository(session)
        self.download_image = DownloadImageUseCase()
        self.storage = storage

    def execute(self, manwha_data) -> int:
        self.manwha_data = manwha_data

        is_manwha_registered = self.is_manwha_registered()
        if is_manwha_registered:
            return is_manwha_registered

        self.manwha_id = self.create_manwha()
        self.manage_thumbnail()
        self.manage_genres()
        self.manage_artists()
        self.manage_authors()
        self.manage_alternative_names()

        return self.manwha_id

    def is_manwha_registered(self) -> int | None:
        manwha = self.manwha_repository.get("name", self.manwha_data["manwha_name"])
        if manwha:
            return manwha[0].id

    def create_manwha(self) -> int:
        release = self.manwha_data["release"]
        return self.manwha_repository.add(
            Manwha(
                name=self.manwha_data["manwha_name"],
                summary=self.manwha_data["summary"],
                release=release[0] if release else None,
            )
        )

    def manage_thumbnail(self):
        image_url = self.manwha_data["thumbnail"]
        image_name = "thumbnail"
        image_type = image_url.split(".")[-1]

        self.download_image.execute(
            local_dir=SETTINGS.thumbnail_local_folder,
            image_name=image_name,
            image_type=image_type,
            image_url=image_url,
        )

        storage_path = f"manwha/{self.manwha_id}/{image_name}.{image_type}"

        self.storage.upload_object(
            local_path=f"{SETTINGS.thumbnail_local_folder}/{image_name}.{image_type}",
            storage_path=storage_path,
        )

        self.manwha_repository.update(
            "id", self.manwha_id, {"thumbnail": f"{self.storage.bucket_url}/{storage_path}"}
        )

        shutil.rmtree(SETTINGS.thumbnail_local_folder)

    def manage_genres(self):
        for genre_name in self.manwha_data["genres"]:
            genre = self.genre_repository.get("name", genre_name)
            if genre:
                self.manwha_genre_repository.add(
                    ManwhaGenre(manwha_id=self.manwha_id, genre_id=genre[0].id)
                )
                continue

            genre_id = self.genre_repository.add(Genre(name=genre_name))

            self.manwha_genre_repository.add(
                ManwhaGenre(manwha_id=self.manwha_id, genre_id=genre_id)
            )

    def manage_artists(self):
        for artist_name in self.manwha_data["artists"]:
            artist = self.artist_repository.get("name", artist_name)
            if artist:
                self.manwha_artist_repository.add(
                    ManwhaArtist(manwha_id=self.manwha_id, artist_id=artist[0].id)
                )
                continue

            artist_id = self.artist_repository.add(Artist(name=artist_name))

            self.manwha_artist_repository.add(
                ManwhaArtist(manwha_id=self.manwha_id, artist_id=artist_id)
            )

    def manage_authors(self):
        for author_name in self.manwha_data["authors"]:
            author = self.author_repository.get("name", author_name)
            if author:
                self.manwha_author_repository.add(
                    ManwhaAuthor(manwha_id=self.manwha_id, author_id=author[0].id)
                )
                continue

            author_id = self.author_repository.add(Author(name=author_name))

            self.manwha_author_repository.add(
                ManwhaAuthor(manwha_id=self.manwha_id, author_id=author_id)
            )

    def manage_alternative_names(self):
        for alternative_name in self.manwha_data["alternative_names"]:
            alternative_name_db = self.alternative_name_repository.get("name", alternative_name)
            if alternative_name_db:
                self.manwha_alternative_name_repository.add(
                    ManwhaAlternativeName(
                        manwha_id=self.manwha_id, alternative_name_id=alternative_name_db[0].id
                    )
                )
                continue

            artist_id = self.alternative_name_repository.add(
                AlternativeName(name=alternative_name)
            )

            self.manwha_alternative_name_repository.add(
                ManwhaAlternativeName(manwha_id=self.manwha_id, alternative_name_id=artist_id)
            )
