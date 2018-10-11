This is a guide to the frequency analysis program in this repository.

**SCROLLEDTEXT BOXES**

The top box will be referred to as *entry* and the bottom as *answer*
Text can be entered into both text boxes, although it is pointless to do it into the bottom one.
After typing, click the 'Monographs' button. If you edit the text, click 'Decrypt Using Current' to update it.
Currently, you can't use the 'Digraphs' and 'Trigraphs' buttons. I will add these if I can be bothered.


**SWITCHING LETTERS**

Letters can be entered into the two boxes. The 'switch' button will enable when both have a letter.
IMPORTANT: the letters entered will correspond to letters in the deciphered text/column 2 in the alphabet listbox.
They only allow a single, lowercase letter - if you type in a capital letter it will convert it to lowercase.
This only allows letters. It will delete the character if it is not a letter.
It will delete all letters except for the last one, so of you type a letter after one already there, it will keep the last one.
When you switch, the 'decrypt using current' button will be invoked and both letters will be switched.


**ENTERING A WORD**

A word may be entered. It is not case-sensetive.
All words that could be enciphered to this that appear in the entry scrolledtext are listed.
It is in alphabetical order and retains the case when displayed.
Simply click on the word that you want to use and it will switch all of the appropriate letters.
The word you enter should be an english word to find possible matches.


**STRING/REGULAR EXPRESSION MATCHING**

The instruction will say 'Enter a string to match' or 'Enter a regexp to match'.
The checkbox below saying 'Use regular expressions?' will switch between these two.
Enter a string into the entry box to find all matches within the text.
The radiobutton saying 'In Entry' (default) or 'In Answer' is where it finds matches in.
If you select one, it will look for matches in that scrolledtext box and find their enciphered/deciphered counterparts in the other.
It is recommended that you have both scrolledtext boxes filled with text, with the bottom one of the same length as the top.
The matches will be highlighted in yellow.
If the you are using a regular expression, it will be highlighted in red if there is a syntax error.
Note that the regular expressions are run on each line - ^ and $ will find the start and end of each line respectively.
Also note that a new line is whenever the enter key has been pressed and not necessarily when it 'overflows' to the next line.
The number of matches are recorded and shown.
For regular expression documentation, see https://docs.python.org/2/library/re.html
Otherwise, you can just search for a direct match in the text without any knowledge of regular expressions.
