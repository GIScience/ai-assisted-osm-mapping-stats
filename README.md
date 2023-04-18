# ai-assisted-osm-mapping-stats
Find our the global scale and evolution of AI-assisted mapping in OpenStreetMap

## Introduction

AI-assisted mapping has become an increasingly important tool in humanitarian mapping efforts. With the help of AI, satellite images can be analyzed and interpreted to identify areas affected by natural disasters or conflicts, and to map out the locations of critical infrastructure, such as hospitals and schools.

In the analysis we focused on buildings and roads that were mapped from AI dataset...

Q1: How many buildings were mapped with AI? Where have the most buildings been mapped?

Q2: How many meters/kilimeters of roads were mapped with AI? Where have the most kilometers of roads been mapped?

## Workflow 
<!--[Contribution guidelines for this project](docs/CONTRIBUTING.md)-->
First of all, we downloaded the necessary data for certain regions and relevant time periods in json format via the Ohsome API. We then edited the data to create a DataFrame. We could use the obtained shape of the data to draw graphs. Based on the results from the graphs, we created maps with more detailed results.

```mermaid

flowchart LR
    subgraph Stage 1
    A[1. Download the data via OHSOME API\n and export them]-- Load the data\n and prepare them \nto the desired \nshape/DataFrame -->B
    B[2. Plot the obtained data]-- Focus on the specific\n continents/states -->C
    C[3. Create the maps]
    
    click A "https://github.com/GIScience/ai-assisted-osm-mapping-stats/tree/main/downloaded-data" _blank
    click B "https://github.com/GIScience/ai-assisted-osm-mapping-stats/tree/main/plots" _blank
    click C "https://github.com/GIScience/ai-assisted-osm-mapping-stats/tree/main/maps" _blank

    end
```

## Results

Time period: 2018–2023; data per years:
- Continents:
    - During the period the highest growth of manually mapped buildings was at Europe, Asia, Africa and North America.
    - During the period the highest growth of Microsoft AI buildings was at Africa and North-Central America continents.
- States:
    - Africa:
        - During the period the highest growth of manually mapped buildings was in Tanzania, Nigeria and Uganda.
        - During the period the highest growth of Microsoft AI buildings was in Nigeria, Kenya and Tanzania.
    - North-Central America:
        - During the period the highest growth of manually mapped buildings was in the USA and Canada.
        - During the period the highest growth of Microsoft AI buildings was in the USA and Canada.
