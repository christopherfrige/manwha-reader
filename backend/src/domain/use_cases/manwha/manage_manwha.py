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
from sqlalchemy.orm import Session


class ManageManwhaUseCase:
    def __init__(self, session: Session):
        self.manwha_repository = ManwhaRepository(session)
        self.genre_repository = GenreRepository(session)
        self.artist_repository = ArtistRepository(session)
        self.author_repository = AuthorRepository(session)
        self.alternative_name_repository = AlternativeNameRepository(session)
        self.manwha_genre_repository = ManwhaGenreRepository(session)
        self.manwha_artist_repository = ManwhaArtistRepository(session)
        self.manwha_author_repository = ManwhaAuthorRepository(session)
        self.manwha_alternative_name_repository = ManwhaAlternativeNameRepository(session)

    def execute(self, manwha_data) -> int:
        self.manwha_data = manwha_data

        is_manwha_registered = self.is_manwha_registered()
        if is_manwha_registered:
            return is_manwha_registered

        self.manwha_id = self.create_manwha()
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
        return self.manwha_repository.add(
            Manwha(name=self.manwha_data["manwha_name"], thumbnail=self.manwha_data["thumbnail"])
        )

    def manage_genres(self) -> int:
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

    def manage_artists(self) -> int:
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

    def manage_authors(self) -> int:
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

    def manage_alternative_names(self) -> int:
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
