import os
import json
import sys
import requests

repo = sys.argv[1]

query = """
{
  repository(owner:"%s", name:"%s") {
    packages(first: 100) {
      nodes {
        latestVersion {
          version
        }
      }
    }
  }
}
""" % (repo.split("/")[0], repo.split("/")[1])

headers = {"Authorization": "Bearer %s" % os.environ["GH_TOKEN"]}
response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

package_versions = [node["latestVersion"]["version"] for node in json.loads(response.text)["data"]["repository"]["packages"]["nodes"]]

package_versions.sort(key=lambda s: list(map(int, s.split('.'))))

print(package_versions[-1])
