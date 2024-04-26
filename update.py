#!/usr/bin/env python3
from urllib.request import urlopen
from gzip import GzipFile


def gather_data(version="9", dist="focal"):
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
        if len(d["BinPack"]) == 0:
            continue  # no binary packages, packaging error probably

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
    source_packages_9 = gather_data(version=9, dist="jammy")
    source_packages_8 = gather_data(version=8, dist="focal")
    source_packages_7 = gather_data(version=7, dist="focal")
    source_packages_6 = gather_data(version=6, dist="bionic")
    source_packages_5 = gather_data(version=5, dist="bionic")
    source_packages_4 = gather_data(version=4, dist="bionic")
    source_packages_dev = gather_data(version="dev", dist="focal")
    source_packages_3 = gather_data(version=3, dist="xenial")


    print("""---
---

{%  include header.html %}
    <div class="container">
        <div class="row justify-content-md-center">
    
            <div class="col col-lg-8 bg-light border border-white">
    
                <nav>
                    <div class="nav nav-tabs" id="nav-tab" role="tablist">
                        <a class="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#KERN-9" role="tab" aria-controls="nav-home" aria-selected="true">KERN-9</a>
                        <a class="nav-item nav-link" id="nav-home-tab" data-toggle="tab" href="#KERN-8" role="tab" aria-controls="nav-home" aria-selected="true">KERN-8</a>
                        <a class="nav-item nav-link" id="nav-home-tab" data-toggle="tab" href="#KERN-7" role="tab" aria-controls="nav-home" aria-selected="true">KERN-7</a>
                        <a class="nav-item nav-link" id="nav-home-tab" data-toggle="tab" href="#KERN-6" role="tab" aria-controls="nav-home" aria-selected="true">KERN-6</a>
                        <a class="nav-item nav-link" id="nav-home-tab" data-toggle="tab" href="#KERN-5" role="tab" aria-controls="nav-home" aria-selected="true">KERN-5</a>
                        <a class="nav-item nav-link" id="nav-profile-tab" data-toggle="tab" href="#KERN-dev" role="tab" aria-controls="nav-profile" aria-selected="false">KERN-dev</a>
                        <a class="nav-item nav-link" id="nav-home-tab" data-toggle="tab" href="#KERN-4" role="tab" aria-controls="nav-home" aria-selected="true">KERN-4</a>
                        <a class="nav-item nav-link" id="nav-contact-tab" data-toggle="tab" href="#KERN-3" role="tab" aria-controls="nav-contact" aria-selected="false">KERN-3</a>
                    </div>
                </nav>
                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="KERN-9" role="tabpanel" aria-labelledby="nav-home-tab">
                        <h3 class="display-4">KERN-9</h3>
                        <h3>Ubuntu 22.04, Jammy</h3>
            
                        <hr>
    """)

    print_list(source_packages_9)

    print("""
                </div>
                <div class="tab-pane fade" id="KERN-8" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-8</h3>
                    <h3>Ubuntu 20.04, Focal</h3>
                    <hr>

    """)

    print_list(source_packages_8)
    
    print("""
                </div>
                <div class="tab-pane fade" id="KERN-7" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-7</h3>
                    <h3>Ubuntu 20.04, Focal</h3>
                    <hr>

    """)

    print_list(source_packages_7)


    print("""
                </div>
                <div class="tab-pane fade" id="KERN-6" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-6</h3>
                    <h3>Ubuntu 18.04, Bionic</h3>
                    <hr>

    """)

    print_list(source_packages_6)

    print("""
                </div>
                <div class="tab-pane fade" id="KERN-5" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-5</h3>
                    <h3>Ubuntu 18.04, Bionic</h3>
                    <hr>

    """)

    print_list(source_packages_5)

    print("""
                </div>
                <div class="tab-pane fade" id="KERN-dev" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-dev</h3>
                    <h3>Ubuntu 18.04, Bionic</h3>
                    <hr>

    """)

    print_list(source_packages_dev)

    print("""
                </div>
                <div class="tab-pane fade" id="KERN-4" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-4</h3>
                    <h3>Ubuntu 18.04, Bionic</h3>
                    <hr>

    """)

    print_list(source_packages_4)


    print("""
                </div>
                <div class="tab-pane fade" id="KERN-3" role="tabpanel" aria-labelledby="nav-profile-tab">
                    <h3 class="display-4">KERN-3</h3>
                    <h3>Ubuntu 16.04, Xenial</h3>
                    <hr>
                    <p>
    """)
    print_list(source_packages_3)

    print("""
                </div>
        </div>
    </div>
    </div>


{%  include footer.html %}
    """)
