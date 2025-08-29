# Regex Guide
This document is a guide for understanding the usage of regex (regular expressions) in this project, specifically, in text_processor.py. 

## Multiple lines 
^ = start of a line (with re.MULTILINE)
$ = end of a line (with re.MULTILINE)
This is useful for processing large text chunks line-by-line. 

## Metacharacters
### 1. \s is a metacharacter that matches any whitespace character. 
It can match: 
- A space (' ')
- A tab ('\t')
- A new line ('\n')
- A carriage return ('\r')
- Any Unicode whitespace characters (like non-breaking spaces, etc)
Example usage: 
re.match(r'\s', ' ')   # Match, because ' ' is a space
re.match(r'\s', '\n')   # Match, because '\n' is a newline
re.match(r'\s', '\t')   # Match, because '\t' is a tab


### 2. \s+ means "one or more" whitespace characters
\s+ matches one or more whitespace characters in a row (note the plus '+').
It could be a single space or mulitple spaces, tabs, newlines, etc. 
Example usage: 
re.match(r'\s+', '   ')   # Match, because there are 3 spaces
re.match(r'\s+', '\n\t')  # Match, because there's a newline and tab
re.match(r'\s+', ' \t\n') # Match, because there's one space, a tab, and a newline

### 3. \s* means "zero or more" whitespace characters.
This includes: 
- No whitespace at all (i.e., the empty string)
- A single space
- Multiple spaces
- Multiple tabs, newlines, etc. 

## A note on character classes 
The square brackets in regex [] contains a list of stuff that you want to match. 
Example: [ \t]{2,} means to match 2 or more consecutive characters, and each 
character must be either a space or a tab. Note the intentional space. 




