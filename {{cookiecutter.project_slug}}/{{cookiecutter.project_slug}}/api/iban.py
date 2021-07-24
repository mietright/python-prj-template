# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ibanchecker.validateiban import ValidateNameIban
from ibanchecker.fetchdocument import download
from ibanchecker.config import GCONFIG

router = APIRouter(prefix="/api/v1", tags=["iban"])

logger = logging.getLogger(__name__)


class Item(BaseModel):
    name: str = Field(...)
    iban: str = Field(...)
    document: str = Field(...)


class Validity(BaseModel):
    valid: bool = Field(...)
    details: dict = {}
    document: str = Field(...)


@router.post("/check", response_model=Validity)
async def check_validity(item: Item) -> Validity:
    logger.info("check")
    name = item.name
    iban = item.iban
    source_path = item.document
    dest_dir = GCONFIG.ibanchecker["download_dir"]
    dest_path = await download(source_path, dest_dir)
    checker = ValidateNameIban(name, iban, dest_path)
    checker.run()
    return Validity(
        valid=checker.valid,
        details=checker.status,
        document=item.document,
    )
