from pydantic import Field
from pydantic_settings import BaseSettings


class ElasticsearchConfig(BaseSettings):
    host: str = Field(default='http://localhost:9200', alias='ELASTICSEARCH_HOST')
    index: str = Field(default='taxi_data_api', alias='ELASTICSEARCH_INDEX')


elasticsearch_config = ElasticsearchConfig()
