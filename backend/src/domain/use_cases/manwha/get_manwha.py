from src.domain.entities.manwha import Manwha, ManwhaChapter, ManwhaAlternativeName, ManwhaArtist, ManwhaAuthor, ManwhaGenre
from src.domain.entities.chapter import Chapter
from src.domain.entities.author import Author
from src.domain.entities.artist import Artist
from src.domain.entities.genre import Genre
from src.domain.entities.alternative_name import AlternativeName
from src.domain.schemas.manwha import GetManwhaResponse
from src.domain.schemas.artist import ArtistSchema
from src.domain.schemas.author import AuthorSchema
from src.domain.schemas.genre import GenreSchema
from src.domain.schemas.alternative_name import AlternativeNameSchema
from src.domain.schemas.chapter import ChapterSchema
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
                chapters=self._chapters(),
                authors=self._additional_data(Author, ManwhaAuthor, ManwhaAuthor.author_id, AuthorSchema),
                artists=self._additional_data(Artist, ManwhaArtist, ManwhaArtist.artist_id, ArtistSchema),
                genres=self._additional_data(Genre, ManwhaGenre, ManwhaGenre.genre_id, GenreSchema),
                alternative_names=self._additional_data(AlternativeName, ManwhaAlternativeName, ManwhaAlternativeName.alternative_name_id, AlternativeNameSchema)
            )
            
    def _manwha(self):
        manwha = self.session.query(
            Manwha.id,
            Manwha.name,
            Manwha.thumbnail,
        ).filter(Manwha.id == self.manwha_id).first()
            
        if not manwha:
            return

        return manwha._mapping

    def _chapters(self):
        chapters = self.session.query(
            Chapter.id,
            Chapter.chapter_number,
        ).join(ManwhaChapter, ManwhaChapter.chapter_id == Chapter.id
        ).filter(ManwhaChapter.manwha_id == self.manwha_id).all()
            
        if not chapters:
            return []

        return [ChapterSchema(**chapter._mapping) for chapter in chapters]

    def _additional_data(self, entity, join_entity, join_key, schema):
        entries = self.session.query(
            entity.id,
            entity.name,
        ).join(join_entity, join_key == entity.id
        ).filter(join_entity.manwha_id == self.manwha_id).all()
            
        if not entries:
            return []

        return [schema(**entry._mapping) for entry in entries]
