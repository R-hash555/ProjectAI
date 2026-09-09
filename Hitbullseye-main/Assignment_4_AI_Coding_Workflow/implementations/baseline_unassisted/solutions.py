"""
Baseline Unassisted Solutions (Hand-crafted, thoroughly verified code)
"""
import time
import threading
import heapq
import json
from typing import Dict, Any, List, Optional

# TASK-01: REST API User Endpoint & Validation Middleware
class UserEndpoint:
    def __init__(self):
        self.db = {}

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not payload or "email" not in payload or "@" not in payload["email"]:
            return {"status": 400, "error": "Invalid email address"}
        if "name" not in payload or not payload["name"].strip():
            return {"status": 400, "error": "Name is required"}
        user_id = str(len(self.db) + 1)
        user = {"id": user_id, "name": payload["name"].strip(), "email": payload["email"].strip()}
        self.db[user_id] = user
        return {"status": 201, "data": user}


# TASK-02: LRU Cache with TTL & Eviction
class LRUCacheTTL:
    def __init__(self, capacity: int, default_ttl_sec: float = 60.0):
        self.capacity = capacity
        self.default_ttl = default_ttl_sec
        self.cache = {}  # key -> (value, expiry_time)
        self.order = []  # LRU keys order
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            val, expiry = self.cache[key]
            if time.time() > expiry:
                del self.cache[key]
                self.order.remove(key)
                return None
            self.order.remove(key)
            self.order.append(key)
            return val

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        with self.lock:
            ttl_sec = ttl if ttl is not None else self.default_ttl
            expiry = time.time() + ttl_sec
            if key in self.cache:
                self.order.remove(key)
            elif len(self.cache) >= self.capacity:
                # Evict LRU key
                lru_key = self.order.pop(0)
                del self.cache[lru_key]
            self.cache[key] = (value, expiry)
            self.order.append(key)


# TASK-03: Refactoring Callback Spaghetti to Async Pipeline
class AsyncPipeline:
    @staticmethod
    def process_data(user_id: int, fetch_user_fn, fetch_orders_fn) -> Dict[str, Any]:
        user = fetch_user_fn(user_id)
        if not user or not user.get("active"):
            raise ValueError("Inactive user")
        orders = fetch_orders_fn(user_id)
        total_spent = sum(o["amount"] for o in orders if o.get("status") == "completed")
        return {"user_id": user_id, "user_name": user["name"], "total_spent": total_spent}


# TASK-04: Unit Test Suite Target (Payment Processing)
class PaymentProcessor:
    def process_transaction(self, account_balance: float, amount: float) -> Dict[str, Any]:
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}
        if amount > account_balance:
            return {"success": False, "error": "Insufficient funds"}
        new_balance = round(account_balance - amount, 2)
        return {"success": True, "new_balance": new_balance}


# TASK-05: Debugging Race Condition in Shared Worker Pool
class WorkerPool:
    def __init__(self):
        self.completed_count = 0
        self.lock = threading.Lock()

    def process_task(self):
        # Correct thread-safe counter update
        with self.lock:
            temp = self.completed_count
            time.sleep(0.001)  # Context switch simulation
            self.completed_count = temp + 1


# TASK-06: OAuth2 Token Refresher & Interceptor
class OAuthInterceptor:
    def __init__(self, token: str, refresh_token_fn):
        self.token = token
        self.refresh_token_fn = refresh_token_fn

    def make_request(self, api_call_fn) -> Dict[str, Any]:
        res = api_call_fn(self.token)
        if res.get("status") == 401:
            # Refresh token and retry
            self.token = self.refresh_token_fn()
            res = api_call_fn(self.token)
        return res


# TASK-07: SQL DAO Repository
class UserRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        # Uses parameterized queries to avoid SQL injection
        query = "SELECT id, name, email FROM users WHERE id = ?"
        return self.db_conn.execute(query, (user_id,))


# TASK-08: Dijkstra Shortest Path Algorithm
class DijkstraRouter:
    @staticmethod
    def shortest_path(graph: Dict[str, List[tuple]], start: str, end: str) -> Optional[int]:
        pq = [(0, start)]
        distances = {start: 0}
        visited = set()

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_node in visited:
                continue
            visited.add(current_node)
            if current_node == end:
                return current_dist

            for neighbor, weight in graph.get(current_node, []):
                distance = current_dist + weight
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        return None


# TASK-09: Decoupling Monolithic Config to DI Provider
class ConfigContainer:
    def __init__(self, config_dict: Dict[str, Any]):
        self._config = config_dict

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        val = self._config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val


# TASK-10: Event Bus Subscriber (Memory Leak Fix)
class EventBus:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, listener):
        self._subscribers.append(listener)

    def unsubscribe(self, listener):
        if listener in self._subscribers:
            self._subscribers.remove(listener)

    def publish(self, event_name: str, payload: Any):
        for sub in list(self._subscribers):
            sub(event_name, payload)
