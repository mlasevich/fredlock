"""
Configuration
"""
from dataclasses import dataclass, field, asdict
from typing import List

REDIS_PREFIX = "redis_"


@dataclass
class Config:  # pylint: disable=R0902
    """ Configuration for fredlock """
    name: str = None
    command: List[str] = field(default_factory=list)

    # Redis Config
    redis_url: str = None
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    redis_ssl: bool = False
    redis_password: str = None
    redis_unix_socket_path: str = None

    delay_after_acquire: int = 0
    delay_before_release: int = 0
    auto_release_time: float = 1
    wait_timeout: float = 5.0

    def configure(self):
        """ Compute/validate remaining configuration"""
        self.name = self.lock_name

    @property
    def lock_name(self):
        """ Generate lock name """
        if self.name:
            return self.name
        if self.command:
            return f"{self.command[0]}.lock"
        return "fredlock.lock"

    def update(self, **items):
        """ Update item from a dict """
        for key, value in items.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def redis_config(self):
        """
            Generate Redis config by
            extracting app config parameters starting with
            redis_
        """
        return {key[len(REDIS_PREFIX):]: value
                for key, value in asdict(self).items()
                if key.startswith(REDIS_PREFIX)}
