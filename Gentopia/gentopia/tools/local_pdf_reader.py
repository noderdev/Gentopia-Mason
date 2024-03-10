from typing import AnyStr
from gentopia.tools.basetool import *
import PyPDF2
import io

class LocalPdfReaderArgs(BaseModel):
    pathToPDF: str = Field(..., description="the link to read the pdf")


class LocalPdfReader(BaseTool):
    """read local pdf"""

    name = "local_pdf_reader"
    description = (
        "read local pdf"
    )

    args_schema: Optional[Type[BaseModel]] = LocalPdfReaderArgs
    
    def _run(self, pathToPDF: AnyStr) -> str:
        text = ""
        with open(pathToPDF, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = LocalPdfReader()._run("https://arxiv.org/pdf/2308.04030.pdf")