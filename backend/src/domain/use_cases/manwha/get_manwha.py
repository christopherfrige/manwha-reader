from sqlalchemy import String, cast

from src.domain.entities.alternative_name import AlternativeName
from src.domain.entities.artist import Artist
from src.domain.entities.author import Author
from src.domain.entities.chapter import Chapter
from src.domain.entities.genre import Genre
from src.domain.entities.manwha import (
    Manwha,
    ManwhaArtist,
    ManwhaAuthor,
    ManwhaGenre,
)
from src.domain.schemas.alternative_name import AlternativeNameSchema
from src.domain.schemas.artist import ArtistSchema
from src.domain.schemas.author import AuthorSchema
from src.domain.schemas.chapter import ChapterSchema
from src.domain.schemas.genre import GenreSchema
from src.domain.schemas.manwha import GetManwhaResponse
from src.infrastructure.persistence.unit_of_work import UnitOfWork


class GetManwhaUseCase:
    def execute(self, db: UnitOfWork, manwha_id: int) -> GetManwhaResponse:
        with db.get_session() as session:
            self.manwha_id = manwha_id
            self.session = session

            manwha = self._manwha()
            return GetManwhaResponse(
                name=manwha.name,
                thumbnail=manwha.thumbnail,
                release=manwha.release,
                chapters=self._chapters(),
                authors=self._additional_data(
                    Author, ManwhaAuthor, ManwhaAuthor.author_id, AuthorSchema
                ),
                artists=self._additional_data(
                    Artist, ManwhaArtist, ManwhaArtist.artist_id, ArtistSchema
                ),
                genres=self._additional_data(Genre, ManwhaGenre, ManwhaGenre.genre_id, GenreSchema),
                alternative_names=self._alternative_names(),
            )

    def _manwha(self):
        manwha = (
            self.session.query(Manwha.id, Manwha.name, Manwha.thumbnail, Manwha.release)
            .filter(Manwha.id == self.manwha_id)
            .first()
        )

        if not manwha:
            return

        return manwha._mapping

    def _chapters(self):
        chapters = (
            self.session.query(
                Chapter.id,
                Chapter.chapter_number,
                cast(Chapter.updated_at, String).label("updated_at"),
            )
            .filter(Chapter.manwha_id == self.manwha_id, Chapter.downloaded)
            .order_by(Chapter.chapter_number.desc())
            .all()
        )

        if not chapters:
            return []

        return [ChapterSchema(**chapter._mapping) for chapter in chapters]

    def _alternative_names(self):
        alternative_names = (
            self.session.query(
                AlternativeName.id,
                AlternativeName.name,
            )
            .filter(AlternativeName.manwha_id == self.manwha_id)
            .all()
        )

        if not alternative_names:
            return []

        return [AlternativeNameSchema(**name._mapping) for name in alternative_names]

    def _additional_data(self, entity, join_entity, join_key, schema):
        entries = (
            self.session.query(
                entity.id,
                entity.name,
            )
            .join(join_entity, join_key == entity.id)
            .filter(join_entity.manwha_id == self.manwha_id)
            .all()
        )

        if not entries:
            return []

        return [schema(**entry._mapping) for entry in entries]
