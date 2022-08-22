
from dataclasses import field, dataclass
import random
import string
from .FirebaseEntity import FirebaseEntity, DocumentReference

GAME_CODE_LENGTH = 5
def generate_game_code() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(GAME_CODE_LENGTH))

@dataclass
class Game(FirebaseEntity):
    id: str = None
    game_code: str = field(init=False, default=generate_game_code())
    __COLLECTION_NAME: str = "games"

    def __post__init__(self) -> None:
        self.id = self.game_code

    def get_document_reference(self) -> DocumentReference:
        return DocumentReference(collection_path=self.__COLLECTION_NAME)

    

