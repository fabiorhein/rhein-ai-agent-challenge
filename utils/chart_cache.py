"""
Cache simples para gráficos.
"""
import hashlib
import time
import plotly.graph_objects as go

_cache = {}

def exec_with_cache(code, df):
    key = hashlib.md5(f"{code}_{df.shape}".encode()).hexdigest()
    if key in _cache:
        return _cache[key]

    try:
        local_scope = {"df": df, "go": go, "px": __import__('plotly.express')}
        exec(code, local_scope)
        if 'fig' in local_scope:
            _cache[key] = local_scope['fig']
            return local_scope['fig']
    except:
        pass
    return None
