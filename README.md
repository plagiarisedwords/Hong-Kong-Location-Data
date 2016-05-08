#Introduction to Hong Kong Location Data

###What are the challenges?

Hong Kong doesn't have a post code system and addresses can be written in either English or Chinese. Numbering of buildings is often determined by a lot system that is based on historic auctions rather than through a consistent system of numbering. In addition, division of addresses into areas is often unofficial with no official definition for example of where Central ends and Sheung Wan begins.

Therefore, analysis of location data in Hong Kong often requires the ability to transform unstructured string data into structured data or geographical co-ordinates.

###How can it be solved? (Theory)
Given its unstructured nature and limited size of Hong Kong, the problem lends itself to being solved using information retrieval methods. This however, requires a relatively complete dataset of Hong Kong addresses.

###How can it be solved? (Practice)
A practical solution spans multiple topics

* [Web Scraping](https://github.com/plagiarisedwords/Hong-Kong-Location-Data/wiki/Web-Scraping) - screen scraping code, finding good data sources, review of copyright / terms of use to ensure use is appropriate

* Data aggregation / cleaning - how address data and geographic data from multiple sources can be de-duplicated, structured and linked together

* [Indexing](https://github.com/plagiarisedwords/Hong-Kong-Location-Data/wiki/Indexing) - implementing search indexing "lite" for python / pandas, developing custom tokenisation / stop words for Hong Kong address data

* Geocoding - finding the geographic co-ordinates for a given address, conversion between different co-ordinate systems and reverse geocoding

* Routing - finding best route from two different geographic points by foot, car or public transport


