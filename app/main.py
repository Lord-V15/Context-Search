"""
/* main.py - helper library */

/* Copyright (c) 2021, Vibhansh Gupta*/
/*
modification history
--------------------
01a,18jul21,lord written.
"""

from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json
import search
from search import urls

app = FastAPI()
app.include_router(search.urls.router)
