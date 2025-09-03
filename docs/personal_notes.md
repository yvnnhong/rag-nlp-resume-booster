# My personal notes (to be deleted later -- temporary file)
## This is the draft version of dev_notes.md. 
### 1. Current to-do: Fix potential word deduplication backfiring 
in text_processor.py, the removal of duplicate words may backfire, since many ATS systems prioritize resumes (score these resumes higher) if they repeat important keywords in the job description
-todo: add a feature that lets the user drop in the job description, and then we can score 
their resume against that specific job description
(use counter or collections.defaultdict to track frequencies???)
Note: move everything in here into dev_notes.md 

### 2. Current to-do: add actual vs expected metrics for test validation
In all of the test files, hardcode expected values to compare against the results of the tests,
so the user/me doesn't have to manually verify whether or not the code in question passed the tests. If hardcoded value = tested value, then True. Else, False. Give a final number e.x. XX/15 if there were 15 tests to see how many "actually" passed (the actual passing number will be the number of Trues's)

## Unresolved problems 
# Problem 2: 
This line in text_processor.py: 
```
if clean_word in self.resume_stopwords and not self._is_technical_term(clean_word): 
    continue
```
it's currently too restrictive and will skip over many many important keywords.
Keep it now but we have to change it later -- perhaps integrate with the feature of 
pasting in the job description and then we can see how well the user's resume matches 
the job description. 