import time
import asyncio
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import HTTPException, status, Request

# ==============================================================================
# Rate Limiting & Brute-Force Defense Architecture
# ==============================================================================

class SlidingWindowRateLimiter:
    def __init__(self):
        # map key -> list of timestamps
        self._requests: Dict[str, List[float]] = defaultdict(list)
        # map key -> (failed_count, lockout_until_timestamp)
        self._failed_attempts: Dict[str, Tuple[int, float]] = defaultdict(lambda: (0, 0.0))
        self._lock = asyncio.Lock()

    def get_client_ip(self, request: Request) -> str:
        """Extract client IP securely considering reverse proxies."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # First IP in X-Forwarded-For is the original client IP
            client_ip = forwarded.split(",")[0].strip()
            if client_ip:
                return client_ip
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        if request.client and request.client.host:
            return request.client.host
        return "127.0.0.1"

    async def check_login_rate_limit(self, client_ip: str, identifier: str) -> None:
        """
        Enforce Brute-Force lockout and progressive delays:
        - 1-2 failed attempts: instant response
        - 3-4 failed attempts: progressive delay (1s, 2s)
        - 5+ failed attempts: lockout for 15 minutes
        """
        now = time.time()
        combined_key = f"{client_ip}:{identifier}"
        
        async with self._lock:
            # Check IP lockout or Identifier lockout
            for key in [client_ip, identifier, combined_key]:
                count, lockout_until = self._failed_attempts[key]
                if lockout_until > now:
                    remaining_seconds = int(lockout_until - now)
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"تم حظر محاولات الدخول مؤقتاً لحماية الحساب من هجمات التخمين. يرجى الانتظار {remaining_seconds} ثانية ثم المحاولة مجدداً.",
                        headers={"Retry-After": str(remaining_seconds)}
                    )

            # Progressive Delay Check
            ip_count, _ = self._failed_attempts[client_ip]
            id_count, _ = self._failed_attempts[identifier]
            max_failed = max(ip_count, id_count)
            
            delay = 0.0
            if max_failed == 3:
                delay = 1.0
            elif max_failed >= 4:
                delay = 2.0

        if delay > 0:
            await asyncio.sleep(delay)

    async def record_failed_login(self, client_ip: str, identifier: str, max_attempts: int = 5, lockout_seconds: int = 900) -> int:
        """
        Record a failed login attempt and apply lockout when threshold is reached.
        """
        now = time.time()
        combined_key = f"{client_ip}:{identifier}"
        
        async with self._lock:
            for key in [client_ip, identifier, combined_key]:
                count, _ = self._failed_attempts[key]
                new_count = count + 1
                lockout_until = 0.0
                if new_count >= max_attempts:
                    lockout_until = now + lockout_seconds
                self._failed_attempts[key] = (new_count, lockout_until)

            ip_count, _ = self._failed_attempts[client_ip]
            return ip_count

    async def record_successful_login(self, client_ip: str, identifier: str) -> None:
        """Reset failed counters on successful authentication."""
        combined_key = f"{client_ip}:{identifier}"
        async with self._lock:
            self._failed_attempts.pop(client_ip, None)
            self._failed_attempts.pop(identifier, None)
            self._failed_attempts.pop(combined_key, None)

    async def check_general_rate_limit(self, client_ip: str, limit: int = 120, window_seconds: int = 60) -> None:
        """General sliding-window rate limiter per IP."""
        now = time.time()
        cutoff = now - window_seconds
        
        async with self._lock:
            # Purge expired timestamps
            timestamps = [ts for ts in self._requests[client_ip] if ts > cutoff]
            if len(timestamps) >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="تجاوزت الحد المسموح به من الطلبات، يرجى المحاولة بعد قليل.",
                    headers={"Retry-After": str(window_seconds)}
                )
            timestamps.append(now)
            self._requests[client_ip] = timestamps

limiter = SlidingWindowRateLimiter()
