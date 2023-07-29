from . import *

import os as _os

class Resources(ResourcesDirectory):
    def __init__(self, directory):
        defaultFiles = {}
        defaultFiles[ "index.html" ] = """
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

body {
    display: block;
    position: fixed;
    width: 100%;
    left: 0px;
    right: 0px;
    top: 0px;
}

.code {
    display: block;
    position: relative;
    left: 10px;
    padding: 3px;
    margin: 2px;
    color: var(--colorAccent)
}

"""

        super().__init__(directory, defaultFiles)
    
