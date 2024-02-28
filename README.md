  # QuidLid: AI Lead Qualifier
#### Video Demo:  <URL HERE>
#### Description:
Using the power of AI, API's and file I/O this python project aims to make more
efficient and less time-consuming the b2b-lead-qualifying process for marketing/sales
agents or website-vetting in general. This script takes as input three keywords and a csv with website links that,
using Gemini's API, will be vetted using the given keywords to check if they are indeed
a good lead or not. In the `testing.csv` file you can check how the input file should be structured.
Should any of the three keywords be present in the website, Gemini will qualify the lead as a good one.
Should none of those words appear, the lead will be qualified as bad.

#### Requirements
Apart from the requirements in the txt file, it is also necessary to create a Google Cloud Project,
enabling the AI's API and generating a valid `API_KEY` to be placed in a `.env` file. _Otherwise the
script won't work_. Please check the [Gemini API Overview](https://ai.google.dev/docs/gemini_api_overview)
Eventually you will create said key at [Get API key](https://aistudio.google.com/app/apikey). "Translating" the `curl`
command found in said page into python will make it more easier to understand the way the `make_request` function works

#### About the Main Program
One of the main limitations is that Gemini cannot just read all the links you need it to vet at once (asking it to read
more than 5 in a single prompt will likely make the AI refuse to check any of the links you give to it). In order to work
around this limitation, most of the program works within a `for` loop which is executed depending on how many lines the input
csv has. After getting the three keywords and validating the csv file does exist, the `create_prompt()` function returns
a `str` which would be the prompt crafted wit the keywords and the first five links of the csv and an `int` which is used to
keep track of how many lines were read and avoid repetition when the next `for` loop starts.

Before the loop ends, the `make_request()` function takes in the prompt and `API_KEY` as arguments to be later used in the POST
Http request method to generate a response. The `response.statuscode` is checked for as it is possible for Gemini's servers
to fail even if they worked correctly in a previous `for` loop.

After the request is made, the `write_output_file()` places the results in a csv file, labeling good leads with `TRUE` and
bad leads with `FALSE`. It's important for the function to open the file in `a` mode so the previous results are not overwritten.
The loop continues until there are no more links to check in the input csv file.

Another final limitation that is worth mentioning is that Gemini, even when working correctly, might be unable to access some websites.
Apart from hoping the AI eventually evolves more, the prompt asks it to label any website it could not read as `FALSE`. Please remember
not to use personal or sensitive data when creating prompts with Gemini.

#### About the testing files
The `testing.csv` file shows an example of what your input csv should look like. In the first space you might have an email, name or company name.
What's really important is that the links are placed correctly, as those are to be used to create the prompts.

The `outputtesting.csv` file shows an example of what the output should look like.

#### About the Unit Test
The `test_...` functions are mostly used to check how the program should behave given invalid input data (incorrect csv filename or invalid `API_KEY`)
An example of a correctly generated prompt is also provided
