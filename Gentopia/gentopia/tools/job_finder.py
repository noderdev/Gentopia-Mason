from typing import AnyStr
from gentopia.tools.basetool import *
import http.client
import json

class JobFinderArgs(BaseModel):
    jobTitle: str = Field(..., description="Job Title to search")
    jobLocation: str = Field(..., description="Job Location")


class JobFinder(BaseTool):
    """Find jobs"""

    name = "job_finder"
    description = (
        "Call jooble job search api"
    )

    args_schema: Optional[Type[BaseModel]] = JobFinderArgs
    
    def _run(self, jobTitle,jobLocation : AnyStr) -> str:
        host = 'jooble.org'
        key = '653d6882-3885-485c-a7bc-e68e7d9e08c3' 

        connection = http.client.HTTPConnection(host)
        headers = {"Content-type": "application/json"}
        body = '{ "keywords": "' + jobTitle + '" , "location": "' + jobLocation + '"}'
        connection.request('POST','/api/' + key, body, headers)
        response = connection.getresponse()
        response_data = response.read()
        parsed_response = json.loads(response_data)

        # Threshold set to 5 jobs response from API
        counter = 5
        job_descriptions = ""
        for job in parsed_response['jobs']:
            if job['snippet']:
                job_descriptions += job['snippet'] + "\n"
                counter = counter-1

            if counter == 0:
                break
        
        return job_descriptions

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    ans = JobFinder()._run("software engineer", "United States")