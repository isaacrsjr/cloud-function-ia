# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from utils_config import APP_BUILDER_PROJECT_ID, APP_BUILDER_LOCATION
from utils_config import SEARCH_ENGINE, SERVING_CONFIG_ID
from google.cloud import discoveryengine_v1beta as genappbuilder
from utils_crawler import generate_reference

client = genappbuilder.SearchServiceClient()
serving_config = client.serving_config_path(
    project=APP_BUILDER_PROJECT_ID,
    location=APP_BUILDER_LOCATION,
    data_store=SEARCH_ENGINE,
    serving_config=SERVING_CONFIG_ID,
)

def search(search_query: str, max_size: int=5) -> list:
    request = genappbuilder.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=max_size, # número de documentos procurados
        content_search_spec={
            "snippet_spec": {
                "max_snippet_count": 5 # Quantidade máxima de parágrafos extraídos (até 5)
            },
            "extractive_content_spec": {
                "max_extractive_segment_count": 10 # Quantidade máxima de segmentos extrativos (até 10)
            }
        }
    )
    response = client.search(request)
    n_results = 1

    references = []
    results = list(response.results)

    for result in results:
        references.append(generate_reference(result, n_results))
        n_results += 1
        if n_results > max_size:
            break

    return references