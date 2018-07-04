from urllib.request import urlopen
from gzip import GzipFile

def gather_data(version=4, dist="bionic"):
    sources = f"http://ppa.launchpad.net/kernsuite/kern-{version}/ubuntu/dists/{dist}/main/source/Sources.gz"
    packages = f"http://ppa.launchpad.net/kernsuite/kern-{version}/ubuntu/dists/{dist}/main/binary-amd64/Packages.gz"

    sources_response = GzipFile(fileobj=urlopen(sources))
    packages_response = GzipFile(fileobj=urlopen(packages))

    source_packages = {}
    binary_packages = []

    for raw in sources_response.read().decode().split("\n\n"):
        extracted = {"BinPack": []}
        for detail in raw.split("\n"):
            splitted = detail.split(": ")
            if len(splitted) == 2:
                key, value = splitted
                if key in ("Package", "Version", "Homepage"):
                    extracted[key] = value
        if "Package" in extracted:
            source_packages[extracted["Package"]] = extracted

    for raw in packages_response.read().decode().split("\n\n"):
        extracted = {}
        for detail in raw.split("\n"):
            splitted = detail.split(": ")
            if len(splitted) == 2:
                key, value = splitted
                if key in ("Package", "Source", "Description"):
                    extracted[key] = value
        if extracted:
            binary_packages.append(extracted)


    for bp in binary_packages:
        if "Source" in bp:
            source_name = bp["Source"]
        else:
            source_name = bp["Package"]

        source_packages[source_name]["BinPack"].append(bp["Package"])
        source_packages[source_name]["Description"] = bp["Description"]
    
    return source_packages


def print_list(source_packages):
    for d in sorted(source_packages.values(), key=lambda x: x['Package']):
        binpack = ", ".join(d["BinPack"])
        print("""
<div class="container-fluid">
    <div class="row justify-content-md-center">
        <div class='col-3 bg-light border border-white'>
            <a href='{homepage}'><h5>{package}</h5></a>
        </div>
        <div class='col-9 bg-light border border-white'>
            <b>{description}</b>
        </div>
        <div class='col-9 offset-3 bg-light border border-white'>
            binary packages: <i>{binpack}</i>
        </div>
    </div>
</div>
<p>
        """.format(homepage=d["Homepage"], package=d["Package"], description=d["Description"], binpack=binpack))


if __name__ == "__main__":
    source_packages4 = gather_data(version=4, dist="bionic")
    source_packages3 = gather_data(version=3, dist="xenial")


    print("""---
---

{%  include header.html %}

<div class="container">
    <div class="row justify-content-md-center">

        <div class="col col-lg-8 bg-light border border-white">

            <h1 class="page-title">Packages in KERN</h1>

            <hr>
    """)

    print("""
            <h3>KERN-4 (Ubuntu 18.04, Bionic)</h3>

            <p>Please note that some packages (like Casacore) are now in the Ubuntu
            repository, so not listed here.
    """)
    print_list(source_packages4)


    print("""
            <h3>KERN-3 (Ubuntu 16.04, Xenial)</h3>

            <p>
    """)
    print_list(source_packages3)


    print("""


{%  include footer.html %}
    """)