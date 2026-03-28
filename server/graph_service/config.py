from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    openai_api_key: str
    openai_base_url: str | None = Field(None)
    model_name: str | None = Field(None)
    embedding_model_name: str | None = Field(None)

    # Graph backend selection: "neo4j" or "falkordb"
    graph_db_provider: Literal['neo4j', 'falkordb'] = Field('neo4j')

    # Neo4j settings (required when graph_db_provider == "neo4j")
    neo4j_uri: str | None = Field(None)
    neo4j_user: str | None = Field(None)
    neo4j_password: str | None = Field(None)

    # FalkorDB settings (required when graph_db_provider == "falkordb")
    falkordb_host: str = Field('localhost')
    falkordb_port: int = Field(6379)
    falkordb_username: str | None = Field(None)
    falkordb_password: str | None = Field(None)
    falkordb_database: str = Field('graphiti')

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings():
    return Settings()  # type: ignore[call-arg]


ZepEnvDep = Annotated[Settings, Depends(get_settings)]
