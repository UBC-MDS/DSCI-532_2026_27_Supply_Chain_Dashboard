# Supply Chain Dashboard Proposal

## Section 1: Motivation and Purpose

> **Our role:** Data Science Consultancy Firm
> **Target audience:** Supply Chain Managers for Beauty Retailers
>
> In many industries, such as the Beauty retail industry, it is important to monitor the flow of goods and services going in and out of organizations. When a supply chain is inefficient, there are quality control issues, overstocking/understocking, excessive costs etc. Monitoring these factors would allow companies to optimize their management resulting in more efficiency such as minimizing costs and maximizing profits. To make this possible, we propose to build a data visualization app that allows supply chain managers to identify revenue generated based on product categories, number of products sold, customer demographics etc. These different factors would allow retailers, specifically Beauty Retailers to make meaningful business decisions based on which products perform well and also identifying areas where they can improve upon or cut costs with the motivation to generate more profit and improve customer satisfaction.

## Section 2: Description of the Data

> We will be visualizing a dataset of 100 records from a Fashion and Beauty startup with 24 different variables that contain the following supply chain information, which we hypothesize could be helpful for improving supply chain efficiency. This dataset contains a mix of numeric and categorical variables, allowing us to create a wide variety of visualizations depending on the information we want to convey per visualization. The categories include:
>
> - Categories (`Product type`, `Customer Demographics`, `Location`, `Supplier Name`)
> - Prices and Expenses (`Price`, `Costs`, `Revenue Generated` etc.)
> - Product Movement (`Availability`, `Number of Products sold`, `Stock levels`)
> - Quality Control (`Inspection Results`, `Defect rates`)
>
> Using variables such as the ones mentioned can also be used to derive new columns, for example we can get the `Cost per unit` by dividing `Costs` by `Number of Products sold`. We can also group by different categories, for example we can look at `Defect rates` based on `Location`.

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

![Dashboard](sketch.png "App Sketch")

> ...