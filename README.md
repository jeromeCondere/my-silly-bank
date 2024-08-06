# My silly bank

## The main object

This project is about using machine learning (ML) and data engineering tools to create a simplified version of a bank system. The focus here is on building a transaction system. Keep in mind, this isn’t intended to be a real-world, production-ready banking solution—just a basic, conceptual approach.

## Why I am doing that?
It is very simple, when looking at the way LLMs are used on various resources tutorial that I have found, people seems to think that whenever there's a problem involving text they should go with the LLMs, so I'll argue differently here. While LLMs are indeed powerful, in certain business contexts, they may not always be the most practical or efficient solution, for several reasons:  

1. High Development Cost: Developing LLMs can be expensive, requiring multiple experts and significant computational resources.
2. Time-Consuming Development: Building and fine-tuning these models takes time.
3. Model Obsolescence: During development, more efficient models could be released, raising the question of whether to continue with an outdated model.
4. Negative ROI: The return on investment from running these models in production might not justify the initial development cost.
5. Simpler Alternatives: In some cases, there are more cost-effective, simpler solutions that can achieve the desired results.

## What is the approach
I'm going to assume that I'm in the worst case scenario. Let's say that I am an individual, I don't have tens or hundreds of thousands of dollars to invest in the development of a ML end-to-end solution, I just want to be able **to get as close as I can** from a business-like solution.


## The chapters
So I am going to present several use cases scenario for my silly bank   
**Chapter 1**
The scenario: I just want to develop a chatbot for my bank so clients can query information via text. I know this is not the ideal use case for LLMs, but it's a basic starting point to explore the productionization part.  
Go in the end-to-end-llama3 to see the project. 
**Chapter 2 (WIP)**
The scenario: I want to build a system that allows investigators to query the bank’s information system to identify fraudulent transaction patterns in customer histories. This chapter is still a work in progress.
**Chapter 3 (WIP)**
The scenario: Similar to Chapter 2, but in addition to detecting fraud patterns, I also want my system to be able to generate data visualizations to help analysts interpret the results. This chapter is also still a work in progress.