"""
AI-Assisted Solutions (Generated code containing plausible edge-case bugs caught during verification)
"""
import time
import heapq
from typing import Dict, Any, List, Optional

# TASK-01: REST API User Endpoint (DEFECT: Allows empty string names)
class UserEndpoint:
    def __init__(self):
        self.db = {}

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Bug: Missed checking if 'name' is empty/whitespace only
        if not payload or "email" not in payload or "@" not in payload["email"]:
            return {"status": 400, "error": "Invalid email address"}
        user_id = str(len(self.db) + 1)
        user = {"id": user_id, "name": payload.get("name", ""), "email": payload["email"]}
        self.db[user_id] = user
        return {"status": 201, "data": user}


# TASK-02: LRU Cache with TTL (DEFECT: Not thread-safe & omits TTL check on get)
class LRUCacheTTL:
    def __init__(self, capacity: int, default_ttl_sec: float = 60.0):
        self.capacity = capacity
        self.default_ttl = default_ttl_sec
        self.cache = {}
        self.order = []

    def get(self, key: str) -> Optional[Any]:
        # Bug: Forgotten TTL expiration check! Returns stale expired items. Also missing lock.
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key][0]
        return None

    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            lru = self.order.pop(0)
            del self.cache[lru]
        self.cache[key] = (value, time.time() + (ttl or self.default_ttl))
        self.order.append(key)


# TASK-03: Async Pipeline (SUCCESS: Clean implementation)
class AsyncPipeline:
    @staticmethod
    def process_data(user_id: int, fetch_user_fn, fetch_orders_fn) -> Dict[str, Any]:
        user = fetch_user_fn(user_id)
        if not user or not user.get("active"):
            raise ValueError("Inactive user")
        orders = fetch_orders_fn(user_id)
        total_spent = sum(o["amount"] for o in orders if o.get("status") == "completed")
        return {"user_id": user_id, "user_name": user["name"], "total_spent": total_spent}


# TASK-04: Payment Processor (DEFECT: Floating point precision rounding bug)
class PaymentProcessor:
    def process_transaction(self, account_balance: float, amount: float) -> Dict[str, Any]:
        if amount <= 0:
            return {"success": False, "error": "Invalid amount"}
        if amount > account_balance:
            return {"success": False, "error": "Insufficient funds"}
        # Bug: Missed rounding float subtraction, producing 0.30000000000000004
        new_balance = account_balance - amount
        return {"success": True, "new_balance": new_balance}


# TASK-05: Worker Pool (DEFECT: Race Condition - non-atomic increment without lock)
class WorkerPool:
    def __init__(self):
        self.completed_count = 0

    def process_task(self):
        # Bug: Classic race condition! Non-atomic counter without lock
        temp = self.completed_count
        time.sleep(0.001)
        self.completed_count = temp + 1


# TASK-06: OAuth Interceptor (SUCCESS: Clean implementation)
class OAuthInterceptor:
    def __init__(self, token: str, refresh_token_fn):
        self.token = token
        self.refresh_token_fn = refresh_token_fn

    def make_request(self, api_call_fn) -> Dict[str, Any]:
        res = api_call_fn(self.token)
        if res.get("status") == 401:
            self.token = self.refresh_token_fn()
            res = api_call_fn(self.token)
        return res


# TASK-07: SQL DAO Repository (DEFECT: Security - String formatting SQL Injection vulnerability!)
class UserRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def find_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        # Bug: Critical Security Flaw! String interpolation SQL injection vulnerability
        query = f"SELECT id, name, email FROM users WHERE id = {user_id}"
        return self.db_conn.execute(query)


# TASK-08: Dijkstra Router (SUCCESS: Correct implementation)
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


# TASK-09: Config Container (SUCCESS: Correct implementation)
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


# TASK-10: Event Bus Subscriber (DEFECT: Memory Leak - Subscriber list never cleared / no unsubscribe)
class EventBus:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, listener):
        self._subscribers.append(listener)

    # Bug: Forgotten unsubscribe method! Retains references indefinitely causing memory leak
    def publish(self, event_name: str, payload: Any):
        for sub in self._subscribers:
            sub(event_name, payload)
