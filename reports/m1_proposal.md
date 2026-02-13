# Proposal Examples

...

## Section 1: Motivation and Purpose

> **Our role:** ...
> **Target audience:** ...
>
> ...

## Section 2: Description of the Data

> ...
>
> ...
> ...
> ...
>
> ...

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario
> ...
>
> ...
>
> ...

### User Stories

> **User Story 1:**
> As a **policy maker**, I want to **filter appointments by specific demographics (e.g., age, gender)** in order to **determine if specific population groups are disproportionately missing appointments**.
>
> **User Story 2:**
> As a **policy maker**, I want to **compare no-show rates between patients with and without specific conditions (e.g., hypertension)** in order to **identify if medical conditions are high-risk factors**.
>
> **User Story 3:**
> As a **policy maker**, I want to **visualize no-shows across days of the week** in order to **decide if specific days need scheduling interventions**.

### Jobs to Be Done

> **JTBD 1:**
> **Situation:** When I am reviewing monthly attendance reports...
> **Motivation:** ...I want to separate routine absences from systemic issues...
> **Outcome:** ...so I can allocate intervention budget to the right patient groups.
>
> **JTBD 2:**
> **Situation:** When investigating a spike in no-shows...
> **Motivation:** ...I want to see if specific physical disabilities correlate with absenteeism...
> **Outcome:** ...so I can propose targeted transportation support services.
>
> **JTBD 3:**
> **Situation:** When planning clinic hours...
> **Motivation:** ...I want to see if appointments on Mondays or Fridays are missed more often...
> **Outcome:** ...so I can optimize the scheduling grid.

## Section 4: Exploratory Data Analysis

> *To address User Story 1 (Demographics), we analyzed the no-show rate across different age groups.*
>
> **Analysis:** The bar chart in `notebooks/eda_analysis.ipynb` reveals that patients in the 20-30 age bracket have a 15% higher no-show rate than the average.
>
> **Reflection:** This finding supports the need for a targeted filter in the dashboard. By allowing the policy maker to isolate "Young Adults," they can investigate if this high trend holds true across different clinic locations, helping them decide if age-specific text message reminders are needed.

## Section 5: App Sketch & Description
Below is a sketch of what the dashboard could look like with a first draft of the metrics we want to include:

![Sketch](../img/sketch.png "App Sketch")