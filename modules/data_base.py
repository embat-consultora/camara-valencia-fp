import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get(tableName):
    response = supabase.table(tableName).select('*').execute()
    return response.data

def getEqual(tableName, variable, value):
    response = supabase.table(tableName).select('*').eq(variable, value).execute()
    return response.data
def add(tableName, data):
    response = supabase.table(tableName).insert(data).execute()
    return response
def update(tableName, data,searchFor, searchValue):
    response = supabase.table(tableName).update(data).eq(searchFor, searchValue).execute()
    return response
def delete(tableName,searchFor, searchValue):
    response = supabase.table(tableName).delete().eq(searchFor, searchValue).execute()
    return response

def getOrdered(tableName, searchFor, searchValue, orderByColumn):
    response = supabase.table(tableName).select('*').eq(searchFor, searchValue).order(orderByColumn).execute()
    return response.data

def upsert(tableName, data):
    response = supabase.table(tableName).upsert(data).execute()
    return response
def saveAuthToken(data):
    return supabase.table('auth_tokens').insert(data).execute()

def getAuthToken(email):
    response = supabase.table('auth_tokens').select('*').eq('email', email).execute()
    if response.data:
        return response.data[0]  # ✅ Devolvemos el primer resultado como dict
    return None