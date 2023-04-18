# ai-assisted-osm-mapping-stats
Find our the global scale and evolution of AI-assisted mapping in OpenStreetMap

## Introduction

In the analysis we focus on AI-assisted mapping. 
## Workflow [Contribution guidelines for this project](docs/CONTRIBUTING.md)


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