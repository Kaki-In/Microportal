from . import *

import os as _os

class MailResources(ResourcesDirectory):
    def __init__(self, directory):
        defaultFiles = {}
        defaultFiles[ "index.html" ] = """\
<html>
    <head>
        <meta charset='utf-8'>
        <style>
{STYLE}
        </style>
    </head>
	
    <body>
        <h1> {TITLE} </h1>
        
        {CONTENT}
    </body>
</html>
"""
        defaultFiles[ "style.css" ] = """
:root {
    --primaryColor: #12b7ff;
    --secondaryColor: #89dbff;
    --colorAccent: #095b7f;
}

h1 {
    color: var(--primaryColor);
}

#verification-code {
    display: inline-block;
    font-family: 'REM', sans-serif;
    position: relative;
    left: 10px;
    margin: 2px;
    color: var(--colorAccent);
    background: #ccc;
    padding: 10px;
    border-radius: 5px;
    font-weight: bold;
}

"""

        super().__init__(directory, defaultFiles)
    
