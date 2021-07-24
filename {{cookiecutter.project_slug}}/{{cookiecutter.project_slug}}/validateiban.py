import re
from pathlib import PurePath
from typing import List
import logging

import ocrmypdf
import textract

logger = logging.getLogger(__name__)


class ValidateNameIban:
    def __init__(self, name: str, iban: str, document_path: str) -> None:
        self.name: str = name
        self.iban: str = iban
        self.status: dict = {
            "name": False,
            "iban": False,
        }  # @TODO: Replace with an pydantic object
        self.document_path: str = document_path
        self.lines: List = []
        self.text: str = ""
        self._evaluated: bool = False

    def _build_re(self, val: str) -> re.Pattern:
        val = val.replace(" ", "")
        reg = ""
        for char in val:
            reg += "%s *" % char

        return re.compile(reg, re.IGNORECASE)

    def find_name(self, name: str) -> bool:
        """
        Search for all variation of name in the document
        - Mr. Doe
        - John Doe
        - J. Doe
        ...
        """
        pattern = self._build_re(name)
        match = pattern.search(self.text)
        return match is not None

    def find_iban(self, iban: str) -> bool:
        """
        Search for all variation of iban, with space, no space
        - DE7294 4243 04324
        - DE 7294 424304324
        - D E 7 2 9 4 4 2 4 3 0 4 32 4
        ...
        """
        pattern = self._build_re(iban)
        match = pattern.search(self.text)
        return match is not None

    @property
    def valid(self) -> bool:
        if not self._evaluated:
            self.run()
        return self.status["iban"] and self.status["name"]

    def ocr(self, document_path: str) -> bytes:
        logger.debug("ocr")
        path = PurePath(document_path)
        outputpath = str(
            path.joinpath(
                path.parent,
                str(path.name).split(path.suffix, maxsplit=1)[0] + ".ocr.pdf",
            )
        )
        ocrmypdf.ocr(document_path, outputpath, force_ocr=True)
        return textract.process(outputpath, language="deu")

    def run(self):
        return self._run(self.name, self.iban, self.document_path)

    def _run(self, name: str, iban: str, document_path: str) -> bool:
        self.text = self.ocr(document_path).decode("utf-8")
        self.status["iban"] = self.find_iban(iban)
        self.status["name"] = self.find_name(name)
        self._evaluated = True
        return self.valid
