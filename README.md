# Jobs Data Analysis: An Evaluation of Job Offers with a Focus on Czech Digital Entrepreneurship

This repository contains the code used for the paper titled *An Evaluation of the Job Offers with a Focus on Czech Digital Entrepreneurship*. The study evaluates job offers posted by Czech start-ups on the StartUpJobs.cz website, focusing on required skills, offered benefits, and comparing trends in the Czech job market with international trends, especially in the realm of digital entrepreneurship.

## Table of Contents
- [Project Overview](#project-overview)
- [Data](#data)
- [Methods](#methods)
- [Results](#results)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project aims to evaluate the technological structure of Czech start-ups through job advertisements. The focus is on identifying the most demanded skills, technologies, and benefits provided by start-up companies in the digital sector. The code in this repository processes and analyzes job advertisements collected from the StartUpJobs.cz website. The findings of the study are useful for educational institutions, IT professionals, and HR professionals.

The main objectives of the study are:
- To identify the key skills and technologies required by Czech start-ups.
- To analyze the benefits offered to potential employees.
- To compare the structure of Czech job offers with international trends.
  
## Data

The data used in this analysis was collected on **August 27, 2022**, from the **StartUpJobs.cz** website. A total of **953 job advertisements** were analyzed. Each advertisement included:
- Job title
- Location
- Employment type (e.g., full-time, part-time)
- Required skills
- Used technologies
- Offered benefits
- Contract type (employment, freelance)
- Expertise level (junior, medior, senior)

## Methods

The analysis was conducted using Python, with the following libraries:
- **Pandas**: For data manipulation and cleaning.
- **Matplotlib**: For data visualization.

The data processing steps included:
1. Data collection from StartUpJobs.cz.
2. Classification of job offers based on technological requirements and job titles.
3. Analysis of the benefits provided, such as remote work, flexible hours, etc.
4. Comparison with global trends using external sources such as the Stack Overflow Developer Survey.

## Results

Key findings from the study:
- **JavaScript** is the most demanded skill among Czech start-ups, followed by **React.js**, **Node.js**, and **TypeScript**.
- Soft skills like **communication** and **project management** are also frequently required.
- The majority of jobs are located in **Prague**, followed by **Brno** and **Ostrava**.
- Remote work is offered in **42%** of the advertisements, highlighting the shift towards flexible working environments.

These results suggest that professionals seeking to enter the Czech start-up scene, especially in digital entrepreneurship, should focus on acquiring **JavaScript** and related front-end technologies.

## Installation

To run the analysis, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/pesikj/jobs-data-analysis.git
    cd jobs-data-analysis
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the analysis:
```bash
python analyze_jobs.py
```
