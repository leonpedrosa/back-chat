import redis
from chat.settings import URL_REDIS, PORT_REDIS

url = f'redis://{URL_REDIS}:{PORT_REDIS}/0'

r = redis.from_url(url)

KEY = 'online_users'

def mark_online(user_id, ttl=60):
    """Marca o usuário como online com tempo de expiração"""
    r.setex(f"user_online:{user_id}", ttl, "1")

def mark_offline(user_id):
    """Remove a chave the Redis manualmente (opcional)"""
    r.delete(f"user_online:{user_id}")

def is_user_online(user_id):
    """Verifica se o usuário ainda está online"""
    return True if r.exists(f"user_online:{user_id}") == 1 else False

def get_all_online_ids():
    """Busca todos os usuários com chave ativa (online)"""
    keys = r.keys("user_online:*")
    ids = [int(k.decode().split(":")[1]) for k in keys]
    return set(ids)